"""
Notification Service
Handles sending notifications via various channels
"""

from sqlalchemy.orm import Session
from app.models import Notification, User
from app.models.notification import NotificationType, NotificationStatus
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing notifications"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: dict = None
    ) -> Notification:
        """
        Create a notification
        
        Args:
            user_id: Target user ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional data (optional)
            
        Returns:
            Created notification
        """
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data,
            status=NotificationStatus.PENDING
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        # Send notification (SMS, Email, Push, etc.)
        self._send_notification(notification)
        
        return notification
    
    def _send_notification(self, notification: Notification):
        """
        Send notification via appropriate channel
        
        This is a placeholder - implement actual sending logic:
        - SMS via SMS gateway
        - Email via email service
        - Push notification via FCM/APNS
        """
        try:
            user = self.db.query(User).filter(User.id == notification.user_id).first()
            if not user:
                return
            
            # Update status to sent
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
            self.db.commit()
            
            logger.info(f"Notification sent to user {user.email}: {notification.title}")
            
            # TODO: Implement actual sending
            # - Send SMS if user has phone
            # - Send Email
            # - Send Push notification if mobile app installed
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            notification.status = NotificationStatus.FAILED
            self.db.commit()
    
    def send_attendance_notification(
        self,
        student_id: int,
        attendance_type: str,
        location: str = None
    ):
        """Send attendance notification to parent"""
        from app.models import Student
        
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student or not student.parent_id:
            return
        
        attendance_messages = {
            "board_bus": "صعد الطالب الحافلة",
            "enter_school": "دخل الطالب المدرسة",
            "exit_school": "خرج الطالب من المدرسة",
            "arrive_home": "وصل الطالب إلى المنزل"
        }
        
        message = attendance_messages.get(attendance_type, "حدث حضور")
        if location:
            message += f" - {location}"
        
        self.create_notification(
            user_id=student.parent_id,
            notification_type=NotificationType.ATTENDANCE,
            title="تحديث حضور الطالب",
            message=message,
            data={"student_id": student_id, "attendance_type": attendance_type}
        )
    
    def send_pickup_notification(
        self,
        pickup_request_id: int,
        status: str
    ):
        """Send pickup request status notification"""
        from app.models import PickupRequest
        
        request = self.db.query(PickupRequest).filter(
            PickupRequest.id == pickup_request_id
        ).first()
        if not request:
            return
        
        status_messages = {
            "approved": "تم الموافقة على طلب الاستلام",
            "rejected": "تم رفض طلب الاستلام",
            "completed": "تم استلام الطالب بنجاح"
        }
        
        message = status_messages.get(status, "تحديث على طلب الاستلام")
        
        self.create_notification(
            user_id=request.parent_id,
            notification_type=NotificationType.PICKUP,
            title="تحديث طلب الاستلام",
            message=message,
            data={"pickup_request_id": pickup_request_id, "status": status}
        )





