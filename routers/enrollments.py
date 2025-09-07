from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])
get_db = database.get_db

# ------------------ Enroll Student ------------------
@router.post("/", response_model=schemas.EnrollmentOut)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Check student exists
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check course exists
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if already enrolled
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

    new_enrollment = models.Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

# ------------------ List All Enrollments ------------------
@router.get("/", response_model=list[schemas.EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()

# ------------------ Get Enrollment by ID ------------------
@router.get("/{enroll_id}", response_model=schemas.EnrollmentOut)
def get_enrollment(enroll_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enroll_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

# ------------------ Delete Enrollment ------------------
@router.delete("/{enroll_id}")
def delete_enrollment(enroll_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enroll_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"detail": "Enrollment deleted successfully"}

@router.get("/student/{student_id}", response_model=list[schemas.EnrollmentOut])
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(models.Enrollment).filter(models.Enrollment.student_id == student_id).all()
    return enrollments
