# دليل الإعداد - Setup Guide

## المتطلبات الأساسية

### البرمجيات المطلوبة
- Python 3.9 أو أحدث
- PostgreSQL 13 أو أحدث
- Redis 6 أو أحدث (اختياري للتخزين المؤقت)
- Git

### على Windows
```bash
# تثبيت Python
# تحميل من https://www.python.org/downloads/

# تثبيت PostgreSQL
# تحميل من https://www.postgresql.org/download/windows/

# تثبيت Redis (اختياري)
# تحميل من https://github.com/microsoftarchive/redis/releases
```

### على Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip postgresql postgresql-contrib redis-server
```

### على macOS
```bash
brew install python3 postgresql redis
```

## إعداد المشروع

### 1. استنساخ المشروع
```bash
cd D:\emairate\Amantac
```

### 2. إنشاء بيئة افتراضية
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
cd backend
pip install -r ../requirements.txt
```

### 4. إعداد قاعدة البيانات

#### إنشاء قاعدة البيانات
```bash
# تسجيل الدخول إلى PostgreSQL
psql -U postgres

# إنشاء قاعدة البيانات
CREATE DATABASE amantac_db;
CREATE USER amantac_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE amantac_db TO amantac_user;
\q
```

#### إعداد ملف البيئة
```bash
cd backend
copy .env.example .env
# أو على Linux/macOS: cp .env.example .env
```

عدّل ملف `.env`:
```env
DATABASE_URL=postgresql://amantac_user:your_password@localhost:5432/amantac_db
SECRET_KEY=your-secret-key-change-in-production
REDIS_URL=redis://localhost:6379/0
```

### 5. تهيئة قاعدة البيانات
```bash
cd backend
python setup.py
```

سيتم إنشاء الجداول وإنشاء مستخدم إداري افتراضي:
- البريد الإلكتروني: `admin@amantac.com`
- كلمة المرور: `admin123`

**⚠️ مهم: غيّر كلمة المرور بعد أول تسجيل دخول!**

### 6. تشغيل الخادم
```bash
cd backend
python main.py
```

أو باستخدام uvicorn مباشرة:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. الوصول إلى API
- API: http://localhost:8000
- الوثائق التفاعلية (Swagger): http://localhost:8000/docs
- الوثائق البديلة (ReDoc): http://localhost:8000/redoc

## اختبار النظام

### 1. تسجيل مستخدم جديد
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "parent@example.com",
    "phone": "+1234567890",
    "full_name": "Parent Name",
    "role": "parent",
    "password": "password123"
  }'
```

### 2. تسجيل الدخول
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "parent@example.com",
    "password": "password123"
  }'
```

### 3. استخدام Token
```bash
# احفظ الـ token من استجابة تسجيل الدخول
TOKEN="your-token-here"

# استخدام الـ token في الطلبات
curl -X GET "http://localhost:8000/api/students/" \
  -H "Authorization: Bearer $TOKEN"
```

## إعداد الأجهزة (Hardware Setup)

### RFID Reader
1. توصيل قارئ RFID بالكمبيوتر (USB أو Serial)
2. تحديد المنفذ (Port) في الكود
3. تعديل `backend/app/hardware/rfid_reader.py` حسب نوع القارئ

### GPS Tracker
1. إعداد خدمة GPS tracking
2. إضافة API URL و API Key في `.env`
3. تعديل `backend/app/hardware/gps_tracker.py` حسب الخدمة المستخدمة

### Smartwatch Integration
- يحتاج إلى تطوير API خاص بالساعة الذكية
- أو استخدام Bluetooth Low Energy (BLE)

## استكشاف الأخطاء

### مشكلة الاتصال بقاعدة البيانات
```bash
# التحقق من تشغيل PostgreSQL
# Windows: Services -> PostgreSQL
# Linux: sudo systemctl status postgresql
# macOS: brew services list
```

### مشكلة المنافذ
```bash
# التحقق من استخدام المنفذ 8000
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -i :8000
```

### مشكلة الاستيراد
```bash
# التأكد من تفعيل البيئة الافتراضية
# التأكد من تثبيت جميع المتطلبات
pip install -r requirements.txt --upgrade
```

## الخطوات التالية

1. **تطوير Frontend**: إنشاء واجهة ويب باستخدام React أو Vue
2. **تطوير Mobile App**: إنشاء تطبيق موبايل باستخدام React Native أو Flutter
3. **تكامل الأجهزة**: ربط RFID readers و GPS trackers
4. **إعداد الإشعارات**: تكامل SMS و Email services
5. **النشر**: نشر النظام على خادم إنتاج

## الدعم

للحصول على المساعدة، راجع:
- `docs/API_DOCUMENTATION.md` - وثائق API
- `docs/ARCHITECTURE.md` - بنية النظام
- `README.md` - نظرة عامة على المشروع





