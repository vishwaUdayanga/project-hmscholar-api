from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class Admin(BaseModel):
    admin_id:str
    admin_name: bool
    admin_nic:str
    admin_phone:str
    admin_password:str
    admin_email:str

class Semester(BaseModel):
    semester_id:str
    year: int
    status:str
    semester:str

class Course(BaseModel):
    course_id:str
    course_name: str
    enrollment_key:str
    course_description:str

class Program(BaseModel):
    program_id:str
    duration: str
    program_name:str

class Affiliated_University(BaseModel):
    affiliated_with:str
    program_id:str

class Payment(BaseModel):
    payment_id:str
    date:str
    type:str
    bank:str
    branch:str
    receipt_path:str
    amount:float
    status:str
    student_number:str

class New_student(BaseModel):
    newStudent_id:str
    name:str
    address:str
    gender:str
    email:str
    OL_path:str
    AL_path:float
    payment_id:str
    program_id:str
    date:str

class Student(BaseModel):
    student_id:str
    password:str
    newStudent_id:str

class Course_semester_program(BaseModel):
    program_id:str
    course_id:str
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
