from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ------------------ Department ------------------
class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    class Config:
        from_attributes = True


# ------------------ Course ------------------
class CourseBase(BaseModel):
    name: str
    department_id: int

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    department: Optional[DepartmentOut] = None   # nested output
    class Config:
        from_attributes = True


# ------------------ Student ------------------
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    mobile: Optional[str] = None

class StudentCreate(StudentBase):
    password: str   # required at signup

class StudentOut(StudentBase):
    id: int
    class Config:
        from_attributes = True


# ------------------ Faculty ------------------
class FacultyBase(BaseModel):
    name: str
    email: EmailStr
   
class FacultyCreate(FacultyBase):
    password: str   # required at signup

class FacultyOut(FacultyBase):
    id: int
    class Config:
        from_attributes = True



# ------------------ Enrollment ------------------
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    student: Optional[StudentOut] = None
    course: Optional[CourseOut] = None
    class Config:
        from_attributes = True

class LoginBase(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class ProfileOut(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str] = None
    department: Optional[str] = None

    class Config:
        from_attributes = True

class CourseOut(BaseModel):
    id: int
    name: str
    department: str
    faculty: Optional[str]

    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    course_id: int
    name: str
    date: datetime
    

class ExamCreate(ExamBase):
    pass

class ExamOut(ExamBase):
    id: int

    class Config:
        from_attributes = True
class ResultBase(BaseModel):
    student_id: int
    exam_id: int
    marks_obtained: int

class ResultCreate(ResultBase):
    pass

class ResultOut(ResultBase):
    id: int
    class Config:
        from_attributes = True


class NotificationOut(BaseModel):
    title: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

# ------------------ Admin ------------------
# app/schemas.py
class AdminBase(BaseModel):
    name: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminOut(AdminBase):
    id: int
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class DepartmentOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class CourseOut(BaseModel):
    id: int
    name: str
    department: DepartmentOut
    class Config:
        from_attributes = True

class ResultOut(BaseModel):
    exam_id: int
    marks_obtained: int
    class Config:
        from_attributes = True

class StudentOutWithDetails(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[str] = None
    courses: List[CourseOut] = []
    results: List[ResultOut] = []
    class Config:
        from_attributes = True

class StudentWithCoursesAndResults(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: str | None = None
    courses: list[CourseOut] = []
    results: list[ResultOut] = []

    class Config:
        from_attributes = True

# ------------------ Notification ------------------
class NotificationCreate(BaseModel):
    title: str
    message: str

class NotificationOut(NotificationCreate):
    id: int
    created_at: datetime  # or datetime if you prefer
    class Config:
        from_attributes = True

class StudentWithFaculty(BaseModel):
    student_id: int
    student_name: str
    faculty_id: int
    faculty_name: str

    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    student_id: int
    faculty_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentOut(AssignmentBase):
    id: int
    class Config:
        from_attributes = True
class FacultyAssignmentOut(BaseModel):
    id: int
    student_id: int
    faculty_id: int

    class Config:
        from_attributes = True

class FacultyAssignmentRequest(BaseModel):
    student_id: int
    faculty_id: int
