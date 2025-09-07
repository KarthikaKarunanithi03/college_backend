# routers/exams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/exams", tags=["Exams"])

# ---------------- Create Exam ----------------
@router.post("/", response_model=schemas.ExamOut)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    # ✅ Ensure course exists before creating exam
    db_course = db.query(models.Course).filter(models.Course.id == exam.course_id).first()
    if not db_course:
        raise HTTPException(status_code=400, detail="Course does not exist")

    db_exam = models.Exam(
        course_id=exam.course_id,
        name=exam.name,
        date=exam.date,
        
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


# ---------------- Get All Exams ----------------
@router.get("/", response_model=List[schemas.ExamOut])
def get_exams(db: Session = Depends(get_db)):
    exams = db.query(models.Exam).all()
    return exams


# ---------------- Get Exam by ID ----------------
@router.get("/{exam_id}", response_model=schemas.ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


# ---------------- Update Exam ----------------
@router.put("/{exam_id}", response_model=schemas.ExamOut)
def update_exam(exam_id: int, updated_exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam.course_id = updated_exam.course_id
    exam.name = updated_exam.name
    exam.date = updated_exam.date
    exam.total_marks = updated_exam.total_marks

    db.commit()
    db.refresh(exam)
    return exam


# ---------------- Delete Exam ----------------
@router.delete("/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    db.delete(exam)
    db.commit()
    return {"detail": "Exam deleted successfully"}
