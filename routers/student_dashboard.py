# app/routers/admin_dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app import models, schemas
from utils import get_password_hash, get_current_admin, create_access_token
from passlib.context import CryptContext

router = APIRouter(prefix="/student", tags=["Admin Dashboard"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------ Admin Creation ------------------
@router.post("/", response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(admin.password)
    new_admin = models.Admin(name=admin.name, email=admin.email, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

# ------------------ Admin Login ------------------
@router.post("/login")
def admin_login(request: schemas.LoginBase, db: Session = Depends(get_db)):
    db_admin = db.query(models.Admin).filter(models.Admin.email == request.email).first()
    if not db_admin or not pwd_context.verify(request.password, db_admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": f"admin:{db_admin.id}"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": db_admin.id,
        "name": db_admin.name,
        "email": db_admin.email,
    }

# ------------------ Get All Students ------------------
@router.get("/students", response_model=List[schemas.StudentOut])
def get_all_students(
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    return db.query(models.Student).all()

# ------------------ Get All Faculty ------------------
@router.get("/faculty", response_model=List[schemas.FacultyOut])
def get_all_faculty(
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    return db.query(models.Faculty).all()

# ------------------ Assign Faculty to Student ------------------
@router.post("/assign-faculty")
def assign_faculty_to_student(
    student_id: int,
    faculty_id: int,
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

    if not student or not faculty:
        raise HTTPException(status_code=404, detail="Student or Faculty not found")

    student.faculty_id = faculty.id  # assuming Student model has faculty_id
    db.commit()
    return {"message": f"Faculty {faculty.name} assigned to Student {student.name}"}

# ------------------ Add Notification ------------------
@router.post("/notifications", response_model=schemas.NotificationOut)
def add_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    new_notification = models.Notification(
        title=notification.title,
        message=notification.message
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification
