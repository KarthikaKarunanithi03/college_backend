# routers/admin_notifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from utils import get_current_admin
from typing import List

router = APIRouter(prefix="/admin-not", tags=["Admin Notifications"])

# Get all notifications
@router.get("/notifications", response_model=List[schemas.NotificationOut])
def get_notifications(db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    return db.query(models.Notification).order_by(models.Notification.created_at.desc()).all()


# Create a notification
@router.post("/notifications", response_model=schemas.NotificationOut)
def create_notification(notification: schemas.NotificationCreate,
                        db: Session = Depends(get_db),
                        admin: models.Admin = Depends(get_current_admin)):
    db_notification = models.Notification(title=notification.title, message=notification.message)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

# Update a notification
@router.put("/notifications/{notification_id}", response_model=schemas.NotificationOut)
def update_notification(notification_id: int, notification: schemas.NotificationCreate,
                        db: Session = Depends(get_db),
                        admin: models.Admin = Depends(get_current_admin)):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db_notification.title = notification.title
    db_notification.message = notification.message
    db.commit()
    db.refresh(db_notification)
    return db_notification

# Delete a notification
@router.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db),
                        admin: models.Admin = Depends(get_current_admin)):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return {"detail": "Notification deleted successfully"}
