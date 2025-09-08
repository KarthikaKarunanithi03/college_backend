from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import students, faculty, departments, courses, enrollments, auth, student_dashboard, admin, notifications, results,exams,admin_notifications
from utils import get_current_user

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter()
app = FastAPI(title="College Management System")

# ----------------- CORS Setup -----------------
origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE
    allow_headers=["*"],        # allow all headers
)

# ----------------- Routers -----------------
app.include_router(students.router)
app.include_router(faculty.router)
app.include_router(departments.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(auth.router)
app.include_router(student_dashboard.router)
app.include_router(admin.router)
app.include_router(notifications.router)
app.include_router(results.router)
app.include_router(exams.router)
app.include_router(admin_notifications.router)


# ----------------- Root -----------------
@app.get("/")
def root():
    return {"message": "Welcome to College Management API"}

# ----------------- Test Protected Route -----------------
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['user_type']} with ID {current_user['user_id']}"}
