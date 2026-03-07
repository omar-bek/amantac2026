"""
Authentication router
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app import models
from app.models.audit_log import AuditActionType
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import bcrypt

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    # Bcrypt has a 72 byte limit, truncate if necessary
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    # Use bcrypt directly to avoid passlib issues
    try:
        # hashed_password is already a string, don't encode it
        if isinstance(hashed_password, bytes):
            return bcrypt.checkpw(password_bytes, hashed_password)
        else:
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except Exception as e:
        # Fallback to passlib if bcrypt format is different
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            print(f"Password verification error: {e}")
            return False

def get_password_hash(password):
    # Bcrypt has a 72 byte limit, truncate if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    # Use bcrypt directly to avoid passlib issues
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل بالفعل")
        
        # Check if phone is already used (if provided)
        if user_data.phone:
            phone_user = db.query(models.User).filter(models.User.phone == user_data.phone).first()
            if phone_user:
                raise HTTPException(status_code=400, detail="رقم الهاتف مسجل بالفعل")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = models.User(
            email=user_data.email,
            phone=user_data.phone if user_data.phone else None,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"خطأ في التسجيل: {str(e)}")

@router.post("/login")
def login(credentials: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == credentials.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        try:
            password_valid = verify_password(credentials.password, user.hashed_password)
        except Exception as e:
            print(f"Password verification error: {e}")
            import traceback
            traceback.print_exc()
            password_valid = False
        
        if not password_valid:
            # Log failed login attempt
            try:
                from app.routers.audit import log_audit_event
                ip_address = request.client.host if request else None
                user_agent = request.headers.get("user-agent") if request else None
                log_audit_event(
                    db=db,
                    user_id=user.id,
                    action_type=AuditActionType.ACCESS_DENIED,
                    resource_type="authentication",
                    description=f"Failed login attempt for {credentials.email}",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    extra_data=None
                )
            except Exception as e:
                print(f"Error logging failed login: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        # Create access token
        try:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "user_id": user.id, "role": user.role.value},
                expires_delta=access_token_expires
            )
        except Exception as e:
            print(f"Error creating access token: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error creating access token: {str(e)}")
        
        # Log successful login (optional - don't fail if it errors)
        try:
            from app.routers.audit import log_audit_event
            ip_address = request.client.host if request else None
            user_agent = request.headers.get("user-agent") if request else None
            log_audit_event(
                db=db,
                user_id=user.id,
                action_type=AuditActionType.LOGIN,
                resource_type="authentication",
                description=f"User {user.email} logged in successfully",
                ip_address=ip_address,
                user_agent=user_agent,
                extra_data=None
            )
        except Exception as e:
            print(f"Warning: Could not log audit event: {e}")
        
        # Convert user to UserResponse schema to ensure proper serialization
        # Pydantic v2 uses model_validate, v1 uses from_orm
        try:
            user_response = schemas.UserResponse.model_validate(user)
        except (AttributeError, TypeError):
            # Fallback for Pydantic v1
            user_response = schemas.UserResponse.from_orm(user)
        return {"access_token": access_token, "token_type": "bearer", "user": user_response}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in login: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user

