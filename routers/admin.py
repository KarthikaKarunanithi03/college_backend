# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import get_password_hash, get_current_admin, create_access_token
from passlib.context import CryptContext
from ..schemas import FacultyAssignmentRequest
from fastapi import Body
import logging


router = APIRouter(prefix="/admin", tags=["Admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create admin
@router.post("/", response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(admin.password)
    new_admin = models.Admin(
        name=admin.name, email=admin.email, password=hashed_password
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# Get all students
@router.get("/students", response_model=list[schemas.StudentOut])
def get_all_students(
    db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)
):
    return db.query(models.Student).all()


# Get all faculty
@router.get("/faculty", response_model=list[schemas.FacultyOut])
def get_all_faculty(
    db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)
):
    return db.query(models.Faculty).all()


@router.post("/login")
def admin_login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    db_admin = (
        db.query(models.Admin).filter(models.Admin.email == request.email).first()
    )
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

@router.post("/assign-faculty")
def assign_faculty(
    assignment: schemas.FacultyAssignmentRequest = Body(...),   # ✅ Explicitly expect JSON body
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    try:
        # Fetch student and faculty
        student = db.query(models.Student).filter(models.Student.id == assignment.student_id).first()
        faculty = db.query(models.Faculty).filter(models.Faculty.id == assignment.faculty_id).first()

        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {assignment.student_id} not found",
            )
        if not faculty:
            raise HTTPException(
                status_code=404,
                detail=f"Faculty with ID {assignment.faculty_id} not found",
            )

        # Check if assignment already exists
        existing = (
            db.query(models.StudentFacultyAssignment)
            .filter(
                models.StudentFacultyAssignment.student_id == assignment.student_id,
                models.StudentFacultyAssignment.faculty_id == assignment.faculty_id,
            )
            .first()
        )

        if existing:
            return {
                "success": False,
                "message": f"Faculty '{faculty.name}' is already assigned to Student '{student.name}'",
            }

        # Create new assignment
        new_assignment = models.StudentFacultyAssignment(
            student_id=assignment.student_id, faculty_id=assignment.faculty_id
        )
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)

        return {
            "success": True,
            "message": f"Faculty '{faculty.name}' successfully assigned to Student '{student.name}'",
            "assignment_id": new_assignment.id,
            "student_id": student.id,
            "faculty_id": faculty.id,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error assigning faculty: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

@router.get("/student-assignments")
def get_student_assignments(db: Session = Depends(get_db)):
    assignments = (
        db.query(models.StudentFacultyAssignment)
        .join(models.Student, models.StudentFacultyAssignment.student_id == models.Student.id)
        .join(models.Faculty, models.StudentFacultyAssignment.faculty_id == models.Faculty.id)
        .all()
    )

    result = [
        {
            "assignment_id": a.id,
            "student_id": a.student_id,
            "student_name": a.student.name,
            "faculty_id": a.faculty_id,
            "faculty_name": a.faculty.name,
            
        }
        for a in assignments
    ]
    return result
