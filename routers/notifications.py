# routers/notifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ---------------- Create Notification (Admin only) ----------------
@router.post("/", response_model=schemas.NotificationOut)
def create_notification(notification: schemas.NotificationOut, db: Session = Depends(get_db)):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


# ---------------- Get All Notifications (PUBLIC) ----------------
@router.get("/", response_model=list[schemas.NotificationOut])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(models.Notification).all()
