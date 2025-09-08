from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from  app import models, schemas, database
from utils import hash_password

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    # Hash the password before storing
    hashed_pwd = hash_password(student.password)
    db_student = models.Student(
        name=student.name,
        email=student.email,
        mobile=student.mobile,
        password=hashed_pwd
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
@router.get("/", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(database.get_db)):
    return db.query(models.Student).all()

@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}", response_model=schemas.StudentOut)
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student

@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, student_update: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = student_update.name
    student.email = student_update.email
    db.commit()
    db.refresh(student)
    return student


@router.get("/student/{student_id}", response_model=list[schemas.CourseOut])
def get_student_courses(student_id: int, db: Session = Depends(database.get_db)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()
    courses = [e.course for e in enrollments]
    return courses

@router.get("/{student_id}/courses", response_model=list[schemas.CourseOut])
def get_student_courses(student_id: int, db: Session = Depends(database.get_db)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()
    courses = [e.course for e in enrollments]
    return courses

