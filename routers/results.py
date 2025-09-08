# app/routers/results.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/results",
    tags=["Results"]
)

# ------------------ Create Result ------------------
@router.post("/", response_model=schemas.ResultOut)
def create_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    # Check if student exists
    student = db.query(models.Student).filter(models.Student.id == result.student_id).first()
    if not student:
        raise HTTPException(status_code=400, detail="Student does not exist")

    # Check if exam exists
    exam = db.query(models.Exam).filter(models.Exam.id == result.exam_id).first()
    if not exam:
        raise HTTPException(status_code=400, detail="Exam does not exist")

    db_result = models.Result(
        exam_id=result.exam_id,
        student_id=result.student_id,
        marks_obtained=result.marks_obtained
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

# ------------------ Get All Results ------------------
@router.get("/", response_model=List[schemas.ResultOut])
def get_results(db: Session = Depends(get_db)):
    results = db.query(models.Result).all()
    return results

# ------------------ Get Result by ID ------------------
@router.get("/{result_id}", response_model=schemas.ResultOut)
def get_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

# ------------------ Update Result ------------------
@router.put("/{result_id}", response_model=schemas.ResultOut)
def update_result(result_id: int, updated_result: schemas.ResultCreate, db: Session = Depends(get_db)):
    db_result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not db_result:
        raise HTTPException(status_code=404, detail="Result not found")

    db_result.exam_id = updated_result.exam_id
    db_result.student_id = updated_result.student_id
    db_result.marks_obtained = updated_result.marks_obtained

    db.commit()
    db.refresh(db_result)
    return db_result

# ------------------ Delete Result ------------------
@router.delete("/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    db_result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not db_result:
        raise HTTPException(status_code=404, detail="Result not found")

    db.delete(db_result)
    db.commit()
    return {"detail": "Result deleted successfully"}

# ------------------ Get Results by Student ------------------
@router.get("/student/{student_id}", response_model=List[schemas.ResultOut])
def get_results_by_student(student_id: int, db: Session = Depends(get_db)):
    results = db.query(models.Result).filter(models.Result.student_id == student_id).all()
    return results
