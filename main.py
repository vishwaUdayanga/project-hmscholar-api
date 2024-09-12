from uuid import UUID
from datetime import date
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
# from passlib.context import CryptContext
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Admin(BaseModel):
    admin_name: str
    admin_nic:str
    admin_phone:str
    admin_password:str
    admin_email:str

class Semester(BaseModel):
    year: int
    status:int
    semester:int

class Course(BaseModel):
    course_name: str
    enrollment_key:str
    course_description:str

class Program(BaseModel):
    duration: str
    program_name:str

class Affiliated_University(BaseModel):
    affiliated_with:str

class Payment(BaseModel):
    date:date
    type:str
    bank:str
    branch:str
    receipt_path:str
    amount:float
    status:str

class New_student(BaseModel):
    name:str
    address:str
    gender:str
    email:str
    OL_path:str
    AL_path:str
    date:date


class Student(BaseModel):
    student_id:UUID
    password:UUID

class Course_semester_program(BaseModel):
    course_id:UUID
    program_id:UUID
    semester_id:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root():
    return {"Base URL"}
 
@app.post("/admin/login/")
def admin_login(admin_login: Admin, db: db_dependency):
    db_admin = db.query(models.Admin).filter(models.Admin.admin_email == admin_login.admin_email).first()
    if not db_admin or db_admin.admin_password != admin_login.admin_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "admin_name": db_admin.admin_name}

@app.post("/add_admin/")
def create_admin(new_admin: Admin, db: db_dependency):
    db_admin = models.Admin(**new_admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

@app.post("/add_program/")
def create_program(new_program: Program, db: db_dependency):
    db_program = models.Program(**new_program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)

@app.post("/add_semester/")
def create_semester(new_semester: Semester, db: db_dependency):
    db_semester = models.Semester(**new_semester.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)

@app.get("/students/{student_id}")
def get_student_details(student_id:str, db: db_dependency):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.post("/create_course/")
def create_course(new_course: Course, db: db_dependency):
    db_course = models.Course(**new_course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
@app.post("/add_course_semester_program/{program_id}/{semester_id}/{course_id}")
def create_CourseSemesterProgram(program_id:UUID,semester_id:str,course_id:str,db: db_dependency):
    program = db.query(models.Program).filter(models.Program.program_id == program_id).first()
    semester = db.query(models.Semester).filter(models.Semester.semester_id == semester_id).first()
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # Create and add the new record
    db_SCP = models.Course_semester_program(course_id=course.course_id,program_id=program.program_id,semester_id=semester.semester_id)

    db.add(db_SCP)
    db.commit()
    db.refresh(db_SCP)

    return db_SCP

@app.post("/register_student/{program_id}")
def register_new_student(program_id:UUID,new_student: New_student, payment: Payment, db: db_dependency):
    program = db.query(models.Program).filter(models.Program.program_id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # Create new student record
    db_new_student = models.New_student(payment_id = db_payment.payment_id,program_id=program.program_id,**new_student.dict())
    db.add(db_new_student)
    db.commit()
    db.refresh(db_new_student)
    

@app.get("/admin/new_students")
def get_student_details(db: db_dependency):
    db_new_student = db.query(models.New_student).all()
    if db_new_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_new_student


#Lecturer

#Lecturer utils

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

#classes

class Lecturer(BaseModel):
    lecturer_name: str
    lecturer_nic: str
    lecturer_phone: str
    lecturer_email: str
    lecturer_password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LecturerAssignedFor(BaseModel):
    course_id: UUID
    semester_id: UUID
    program_id: UUID
    lecturer_id: UUID

class CourseResponse(BaseModel):
    course_id: UUID
    course_name: str
    year: int
    enrollment_key: str
    semester: int
    lecturer_name: str

class LecturerResponse(BaseModel):
    id: UUID
    name: str

class CourseNameResponse(BaseModel):
    course_name: str

#Lecturer end points

@app.post("/lecturer/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == request.email).first()

    if not lecturer or not request.password == lecturer.lecturer_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": lecturer.lecturer_email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/add_courses")
def create_admin(new_admin: Course, db: db_dependency):
    db_course = models.Course(**new_admin.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

@app.post("/add_programs")
def create_admin(new_admin: Program, db: db_dependency):
    db_program = models.Program(**new_admin.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)

@app.post("/add_semesters")
def create_admin(new_admin: Semester, db: db_dependency):
    db_semester = models.Semester(**new_admin.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)

@app.post("/add_lecturer_assigned_for")
def create_admin(new_admin: LecturerAssignedFor, db: db_dependency):
    db_lecturer_assigned_for = models.Lecturer_assigned_for(**new_admin.dict())
    db.add(db_lecturer_assigned_for)
    db.commit()
    db.refresh(db_lecturer_assigned_for)

@app.get("/lecturer/{lecturer_id}/courses", response_model=List[CourseResponse])
def get_assigned_courses(lecturer_id: UUID, db: Session = Depends(get_db)):
    assigned_courses = (
        db.query(models.Lecturer_assigned_for, models.Lecturer, models.Course, models.Semester)
        .join(models.Course, models.Course.course_id == models.Lecturer_assigned_for.course_id)
        .join(models.Semester, models.Semester.semester_id == models.Lecturer_assigned_for.semester_id)
        .filter(models.Lecturer_assigned_for.lecturer_id == lecturer_id)
        .all()
    )

    if not assigned_courses:
        raise HTTPException(status_code=404, detail="Courses not found for this lecturer")
    
    response = []
    for assignment in assigned_courses: 
        response.append(
            CourseResponse(
                course_id=assignment.Course.course_id,
                course_name=assignment.Course.course_name,
                year=assignment.Semester.year,
                enrollment_key=assignment.Course.enrollment_key,
                semester=assignment.Semester.semester,
                lecturer_name=assignment.Lecturer.lecturer_name
            )
        )

    return response

@app.get("/lecturer/by-email/{email}", response_model=LecturerResponse)
def get_lecturer_by_email(email: str, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == email).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return LecturerResponse(id=lecturer.lecturer_id, name=lecturer.lecturer_name)

@app.get("/courses/{course_id}")
def get_course_name(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.course_name

#Admin endpoints

@app.post("/admin/create_lecturer")
def create_lecturer(lecturer: Lecturer, db: Session = Depends(get_db)):
    lecturer = models.Lecturer(**lecturer.dict())
    db.add(lecturer)
    db.commit()
    db.refresh(lecturer)
    return lecturer