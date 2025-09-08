from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/courses", tags=["Courses"])
get_db = database.get_db

# ------------------ Create Course ------------------
@router.post("/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Check if department exists
    dept = db.query(models.Department).filter(models.Department.id == course.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    new_course = models.Course(name=course.name, department_id=course.department_id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# ------------------ List All Courses ------------------
@router.get("/", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

# ------------------ Get Course by ID ------------------
@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ------------------ Update Course ------------------
@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, updated: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check department exists
    dept = db.query(models.Department).filter(models.Department.id == updated.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    course.name = updated.name
    course.department_id = updated.department_id
    db.commit()
    db.refresh(course)
    return course

# ------------------ Delete Course ------------------
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted successfully"}
