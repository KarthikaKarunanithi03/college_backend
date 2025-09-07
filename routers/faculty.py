from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..utils import hash_password
from ..utils import get_current_faculty
from typing import List

router = APIRouter(prefix="/faculty", tags=["Faculty"])

# Dependency
get_db = database.get_db


# ------------------ Create Faculty ------------------
@router.post("/", response_model=schemas.FacultyOut)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.email == faculty.email).first()
    if db_faculty:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password before saving
    hashed_pwd = hash_password(faculty.password)
    new_faculty = models.Faculty(
        name=faculty.name,
        email=faculty.email,
        password=hashed_pwd
    )
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty
# ------------------ List All Faculty ------------------
@router.get("/", response_model=list[schemas.FacultyOut])
def list_faculty(db: Session = Depends(get_db)):
    return db.query(models.Faculty).all()

# ---------------- Get current logged-in faculty ----------------
@router.get("/me", response_model=schemas.FacultyOut)
def get_faculty_me(faculty: models.Faculty = Depends(get_current_faculty)):
    return faculty

# ---------------- Get all students ----------------
@router.get("/students", response_model=list[schemas.StudentWithCoursesAndResults])
def get_all_students(db: Session = Depends(get_db), faculty: models.Faculty = Depends(get_current_faculty)):
    students = db.query(models.Student).all()
    result = []
    for student in students:
        courses = [enroll.course for enroll in student.enrollments]
        results = student.results
        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "mobile": student.mobile,
            "courses": courses,
            "results": results,
        })
    return result

# ------------------ Get Faculty by ID ------------------
@router.get("/{faculty_id}", response_model=schemas.FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty

# ------------------ Update Faculty ------------------
@router.put("/{faculty_id}", response_model=schemas.FacultyOut)
def update_faculty(faculty_id: int, updated: schemas.FacultyCreate, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    faculty.name = updated.name
    faculty.email = updated.email
    db.commit()
    db.refresh(faculty)
    return faculty

# ------------------ Delete Faculty ------------------
@router.delete("/{faculty_id}")
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    db.delete(faculty)
    db.commit()
    return {"detail": "Faculty deleted successfully"}
#get all courses assigned to faculty
@router.get("/{faculty_id}/courses", response_model=List[schemas.CourseOut])
def get_faculty_courses(faculty_id: int, db: Session = Depends(get_db), faculty: models.Faculty = Depends(get_current_faculty)):
    if faculty.id != faculty_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these courses")
    
    courses = db.query(models.Course).filter(models.Course.faculty_id == faculty_id).all()
    return [schemas.CourseOut(
        id=course.id,
        name=course.name,
        department=course.department.name,
        faculty=faculty.name
    ) for course in courses]
