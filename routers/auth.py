from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database, utils
from utils import verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])
get_db = database.get_db

# ------------------ Student Login ------------------
@router.post("/student/login", response_model=schemas.Token)
def student_login(login: schemas.LoginBase, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == login.email).first()
    if not student or not verify_password(login.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": f"student:{student.id}"})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------ Faculty Login ------------------
@router.post("/faculty/login", response_model=schemas.Token)
def faculty_login(login: schemas.LoginBase, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.email == login.email).first()
    if not faculty or not verify_password(login.password, faculty.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": f"faculty:{faculty.id}"})
    return {"access_token": access_token, "token_type": "bearer"}
