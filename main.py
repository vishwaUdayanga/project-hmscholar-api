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
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import utils
import request_models
import response_models

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
    email:str
    password:str

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

## Logins

@app.post("/login-to-lms")
def login_to_lms(request: request_models.Login, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == request.user_name).first()
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == request.user_name).first()
    admin = db.query(models.Admin).filter(models.Admin.admin_email == request.user_name).first()

    if student:
        if not utils.verify_password(request.password, student.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": student.email, "password": student.password, "type": "student"})
        return {"access_token": access_token, "token_type": "bearer", "student_id": student.student_id, "type": "student"}
    elif lecturer:
        if not utils.verify_password(request.password, lecturer.lecturer_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": lecturer.lecturer_email, "password": lecturer.lecturer_password, "type": "lecturer"})
        return {"access_token": access_token, "token_type": "bearer", "lecturer_id": lecturer.lecturer_id, "type": "lecturer"}
    elif admin:
        print(admin.admin_password)
        if not utils.verify_password(request.password, admin.admin_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": admin.admin_email, "password": admin.admin_password, "type": "admin"})
        return {"access_token": access_token, "token_type": "bearer", "admin_id": admin.admin_id, "type": "admin"}
    

@app.post("/login-to-portal")
def login_to_portal(request: request_models.Login, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == request.user_name).first()
    admin = db.query(models.Admin).filter(models.Admin.admin_email == request.user_name).first()

    if student:
        if not utils.verify_password(request.password, student.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": student.email, "password": student.password, "type": "student"})
        return {"access_token": access_token, "token_type": "bearer", "student_id": student.student_id, "type": "student"}
    elif admin:
        if not utils.verify_password(request.password, admin.admin_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": admin.admin_email, "password": admin.admin_password, "type": "admin"})
        return {"access_token": access_token, "token_type": "bearer", "admin_id": admin.admin_id, "type": "admin"}

@app.post("/validate-login-to-lms")
def validate_login_to_lms(request: request_models.Login, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == request.user_name).first()
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == request.user_name).first()
    admin = db.query(models.Admin).filter(models.Admin.admin_email == request.user_name).first()

    if student:
        if not student.password == request.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"message": "Validation successful", "type": "student"}
    elif lecturer:
        if not lecturer.lecturer_password == request.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"message": "Validation successful", "type": "lecturer"}
    elif admin:
        if not admin.admin_password == request.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"message": "Validation successful", "type": "admin"}
 
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
    course_image: str | None
    semester: int
    lecturer_name: str

class LecturerResponse(BaseModel):
    id: UUID
    name: str

class CourseNameResponse(BaseModel):
    course_name: str

class SectionResponse(BaseModel):
    section_id: UUID
    section_name: str
    section_description: str

class Section(BaseModel):
    section_name: str
    section_description: str
    course_id: UUID

class SectionResponseWithCourse(BaseModel):
    section_id: UUID
    section_name: str
    section_description: str
    course_id: UUID

class SectionEdit(BaseModel):
    section_name: str
    section_description: str

class Course_announcement(BaseModel):
    announcement_title: str
    announcement_description: str
    course_id: UUID

class Course_announcement_edit(BaseModel):
    announcement_title: str
    announcement_description: str

class Course_announcement_response(BaseModel):
    announcement_id: UUID
    announcement_title: str
    announcement_description: str
    course_id: UUID

class Student_profile_response(BaseModel):
    id:UUID
    email:str
    password:str

class StudentEditEmail(BaseModel):
    new_email: str

class StudentEditPassword(BaseModel):
    old_password:str
    new_password: str

    

#Lecturer end points

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
        .join(models.Lecturer, models.Lecturer.lecturer_id == models.Lecturer_assigned_for.lecturer_id)
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
                course_image=assignment.Course.course_image,
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

@app.get("/lecturer/by-email/details/{email}")
def get_lecturer_details(email: str, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == email).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return lecturer

@app.get("/courses/{course_id}")
def get_course_name(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.course_name

@app.get("/course/settings/{course_id}")
def get_course_settings(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/edit-course/{course_id}")
def edit_course(course_id: UUID, new_course: request_models.CourseSettings, db: db_dependency):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.course_name = new_course.course_name
    course.enrollment_key = new_course.enrollment_key
    course.course_description = new_course.course_description
    course.course_image = new_course.course_image
    db.commit()
    db.refresh(course)

    return "Course updated successfully"

@app.post("/add_section")
def add_section(new_section: request_models.Section, db: db_dependency):
    db_section = models.Section(**new_section.dict())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

@app.post("/add_course_material")
def add_course_material(new_material: request_models.Course_Material, db: db_dependency):
    db_material = models.Course_material(**new_material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
    

@app.get("/sections/{course_id}")
def get_sections(course_id: UUID, db: Session = Depends(get_db)):
    sections = db.query(models.Section).filter(models.Section.course_id == course_id).all()
    if not sections:
        raise HTTPException(status_code=404, detail="Sections not found for this course")
    
    response = []
    for section in sections:
        materials = db.query(models.Course_material).filter(models.Course_material.section_id == section.section_id).all()
        quizzes = db.query(models.Quiz).filter(models.Quiz.section_id == section.section_id).all()
        material_response = [{"material_id": mat.material_id , "material_name": mat.material_name, "material_path": mat.material_path} for mat in materials]
        quiz_response = [{"quiz_id": quiz.quiz_id, "quiz_name": quiz.quiz_name} for quiz in quizzes]

        response.append({
            "section_id": section.section_id,
            "section_name": section.section_name,
            "section_description": section.section_description,
            "materials": material_response,
            "quizzes": quiz_response
        })

    return response

@app.get("/sections-for-quiz/{course_id}")
def get_sections_for_quiz(course_id: UUID, db: Session = Depends(get_db)):
    sections = db.query(models.Section).filter(models.Section.course_id == course_id).all()
    if not sections:
        raise HTTPException(status_code=404, detail="Sections not found for this course")
    
    response = []
    for section in sections:
        response.append({
            "section_id": section.section_id,
            "section_name": section.section_name,
        })

    return response

@app.post("/create-quiz")
def create_quiz(new_quiz: request_models.Quiz, db: db_dependency):
    quiz = models.Quiz(
        quiz_name=new_quiz.quiz_name,
        quiz_duration=new_quiz.quiz_duration,
        quiz_total_marks=new_quiz.quiz_total_marks,
        quiz_description=new_quiz.quiz_description,
        quiz_password=new_quiz.quiz_password,
        quiz_no_of_questions=new_quiz.quiz_number_of_questions,
        section_id=new_quiz.section_id
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for question in new_quiz.questions:
        db_question = models.Question(
            question=question.questionText,
            marks=question.questionMarks,
            question_type=question.questionType,
            quiz_id=quiz.quiz_id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        if question.questionType == 'mcq':
            correct_answer = models.Answer(
                answer=question.correctAnswer,
                is_correct=True,
                question_id=db_question.question_id,
            )
            db.add(correct_answer)
            db.commit()
            db.refresh(correct_answer)
            for i in range(3):
                answer_text = None
                if i == 0:
                    answer_text = question.answer2
                elif i == 1:
                    answer_text = question.answer3
                elif i == 2:
                    answer_text = question.answer4
                
                if answer_text is not None:
                    answer = models.Answer(
                        answer=answer_text,
                        is_correct=False,
                        question_id=db_question.question_id,
                    )
                    db.add(answer)
                    db.commit()
                    db.refresh(answer)
    
    return quiz

@app.get("/get-quiz/{quiz_id}")
def get_quiz(quiz_id: UUID, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    response = []
    for question in questions:
        answers = db.query(models.Answer).filter(models.Answer.question_id == question.question_id).all()
        
        correct_answer = None
        answer2 = None
        answer3 = None
        answer4 = None

        mcq_answers = []
        for answer in answers:
            if answer.is_correct:
                correct_answer = answer.answer
            else:
                mcq_answers.append(answer.answer)
        if len(mcq_answers) >= 1:
            answer2 = mcq_answers[0]
        if len(mcq_answers) >= 2:
            answer3 = mcq_answers[1]
        if len(mcq_answers) >= 3:
            answer4 = mcq_answers[2]

            response.append({
                "questionText": question.question,
                "questionMarks": question.marks,
                "questionType": question.question_type,
                "correctAnswer": correct_answer,
                "answer2": answer2,
                "answer3": answer3,
                "answer4": answer4,
            })
        else:
            response.append({
                "questionText": question.question,
                "questionMarks": question.marks,
                "questionType": question.question_type,
            })
    
    course_id = db.query(models.Section).filter(models.Section.section_id == quiz.section_id).first().course_id

    return {
        "quiz_id": quiz.quiz_id,
        "course_id": course_id,
        "quiz_name": quiz.quiz_name,
        "quiz_duration": quiz.quiz_duration,
        "quiz_total_marks": quiz.quiz_total_marks,
        "quiz_description": quiz.quiz_description,
        "quiz_password": quiz.quiz_password,
        "quiz_number_of_questions": quiz.quiz_no_of_questions,
        "section_id": quiz.section_id,
        "questions": response
    }


@app.put("/edit-quiz/{quiz_id}")
def edit_quiz(quiz_id: UUID, new_quiz: request_models.Quiz, db: db_dependency):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz.quiz_name = new_quiz.quiz_name
    quiz.quiz_duration = new_quiz.quiz_duration
    quiz.quiz_total_marks = new_quiz.quiz_total_marks
    quiz.quiz_description = new_quiz.quiz_description
    quiz.quiz_password = new_quiz.quiz_password
    quiz.quiz_no_of_questions = new_quiz.quiz_number_of_questions
    db.commit()
    db.refresh(quiz)

    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    for question in questions:
        db.query(models.Answer).filter(models.Answer.question_id == question.question_id).delete()
        db.commit()
        db.delete(question)
    db.commit()

    for question in new_quiz.questions:
        db_question = models.Question(
            question=question.questionText,
            marks=question.questionMarks,
            question_type=question.questionType,
            quiz_id=quiz.quiz_id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        if question.questionType == 'mcq':
            correct_answer = models.Answer(
                answer=question.correctAnswer,
                is_correct=True,
                question_id=db_question.question_id,
            )
            db.add(correct_answer)
            db.commit()
            db.refresh(correct_answer)
            for i in range(3):
                answer_text = None
                if i == 0:
                    answer_text = question.answer2
                elif i == 1:
                    answer_text = question.answer3
                elif i == 2:
                    answer_text = question.answer4
                
                if answer_text is not None:
                    answer = models.Answer(
                        answer=answer_text,
                        is_correct=False,
                        question_id=db_question.question_id,
                    )
                    db.add(answer)
                    db.commit()
                    db.refresh(answer)
    
    return quiz

@app.delete("/delete-quiz/{quiz_id}")
def delete_quiz(quiz_id: UUID, db: db_dependency):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}

@app.get("/get-quizzes/{course_id}")
def get_quizzes(course_id: UUID, db: Session = Depends(get_db)):
    result = (
        db.query(models.Quiz, models.Section)
        .join(models.Section, models.Section.section_id == models.Quiz.section_id)
        .filter(models.Section.course_id == course_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Quizzes not found for this course")
    
    response = []
    for quiz, section in result:
        response.append({
            "quiz_id": quiz.quiz_id,
            "quiz_name": quiz.quiz_name,
            "section_name": section.section_name
        })
    
    return response

@app.get("/get-student-attempts/{quiz_id}")
def get_student_attempts(quiz_id: UUID, db: Session = Depends(get_db)):
    result = (
        db.query(models.StudentAttempts, models.Student)
        .join(models.Student, models.Student.student_id == models.StudentAttempts.student_id)
        .filter(models.StudentAttempts.quiz_id == quiz_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Attempts not found for this quiz")
    
    response = []
    for attempt, student in result:
        response.append({
            "student_id": student.student_id,
            "email": student.email,
            "quiz_id": attempt.quiz_id,
            "mcq_marks": attempt.mcq_marks,
            "written_marks": attempt.written_marks
        })
    
    return response

@app.get("/get-written-answers/{student_id}/{quiz_id}")
def get_written_answers(student_id: UUID, quiz_id: UUID, db: Session = Depends(get_db)):
    result = (
        db.query(models.StudentWrittenAnswers, models.Question)
        .join(models.Question, models.Question.question_id == models.StudentWrittenAnswers.question_id)
        .filter(models.StudentWrittenAnswers.student_id == student_id)
        .filter(models.StudentWrittenAnswers.quiz_id == quiz_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Answers not found for this student")
    
    response = []
    for answer, question in result:
        response.append({
            "question_id": question.question_id,
            "question": question.question,
            "answer": answer.answer,
            "marks": answer.marks
        })

    return response

@app.put("/edit-written-answers/{student_id}/{quiz_id}")
def edit_written_answers(student_id: UUID, quiz_id: UUID, request_body: request_models.UpdateWrittenAnswersRequest, db: db_dependency):
    full_marks = 0
    for answer in request_body.written_answers:
        db.query(models.StudentWrittenAnswers).filter(models.StudentWrittenAnswers.student_id == student_id).filter(models.StudentWrittenAnswers.quiz_id == quiz_id).filter(models.StudentWrittenAnswers.question_id == answer.question_id).update({"marks": answer.marks})
        full_marks += answer.marks
        db.commit()
    
    db.query(models.StudentAttempts).filter(models.StudentAttempts.student_id == student_id).filter(models.StudentAttempts.quiz_id == quiz_id).update({"written_marks": full_marks})
    db.commit()
    
    return {"message": "Answers updated successfully"}


@app.put('/edit-lecturer-image/{lecturer_id}')
def edit_lecturer_image(lecturer_id: UUID, new_image: request_models.EditLecturerImage, db: db_dependency):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    
    lecturer.lecturer_image = new_image.lecturer_image
    db.commit()
    db.refresh(lecturer)

    return lecturer

@app.put("/edit-lecturer/{lecturer_id}")
def edit_lecturer(lecturer_id: UUID, new_lecturer: request_models.LecturerEdit, db: db_dependency):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    
    lecturer.lecturer_name = new_lecturer.lecturer_name
    lecturer.lecturer_nic = new_lecturer.lecturer_nic
    lecturer.lecturer_phone = new_lecturer.lecturer_phone
    lecturer.lecturer_email = new_lecturer.lecturer_email
    db.commit()
    db.refresh(lecturer)

    return lecturer

@app.get("/lecturer/get-all-students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    
    response = []
    for student in students:
        response.append({
            "student_id": student.student_id,
            "email": student.email,
        })
    
    return response


@app.get("/get-enrolled-students/{course_id}")
def get_enrolled_students(course_id: UUID, db: Session = Depends(get_db)):
    result = (
        db.query(models.Student_enrolled_course, models.Student)
        .join(models.Student, models.Student.student_id == models.Student_enrolled_course.student_id)
        .filter(models.Student_enrolled_course.course_id == course_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Students not found for this course")
    
    response = []
    for enrollment, student in result:
        response.append({
            "student_id": student.student_id,
            "email": student.email,
        })
    
    return response

@app.post("/enroll-student/{student_id}/{course_id}")
def enroll_student(student_id: UUID, course_id: UUID, db: db_dependency):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollment = models.Student_enrolled_course(student_id=student_id, course_id=course_id, semester_id='75cdc5e4-a507-4eef-8778-875b52331a91')
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@app.delete("/delete-student-enrollment/{student_id}/{course_id}")
def delete_student_enrollment(student_id: UUID, course_id: UUID, db: db_dependency):
    enrollment = db.query(models.Student_enrolled_course).filter(models.Student_enrolled_course.student_id == student_id).filter(models.Student_enrolled_course.course_id == course_id).first()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}




@app.get("/one-section/{section_id}") 
def get_section(section_id: UUID, db: Session = Depends(get_db)):
    section = db.query(models.Section).filter(models.Section.section_id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return SectionResponseWithCourse(
        section_id=section.section_id,
        section_name=section.section_name,
        section_description=section.section_description,
        course_id=section.course_id
    )

@app.put("/edit-section/{section_id}")
def edit_section(section_id: UUID, new_section: request_models.SectionEdit, db: db_dependency):
    section = db.query(models.Section).filter(models.Section.section_id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    
    section.section_name = new_section.section_name
    section.section_description = new_section.section_description
    db.commit()
    db.refresh(section)

    return section

@app.delete("/delete-section/{section_id}")
def delete_section(section_id: UUID, db: db_dependency):
    section = db.query(models.Section).filter(models.Section.section_id == section_id).first()
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    
    db.delete(section)
    db.commit()
    return {"message": "Section deleted successfully"}

@app.post("/course/add_announcement")
def add_announcement(new_announcement: Course_announcement, db: db_dependency):
    db_announcement = models.Course_announcement(**new_announcement.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

@app.get("/course/announcements/{course_id}")
def get_announcements(course_id: UUID, db: Session = Depends(get_db)):
    announcements = db.query(models.Course_announcement).filter(models.Course_announcement.course_id == course_id).all()
    if not announcements:
        raise HTTPException(status_code=404, detail="Announcements not found for this course")
    
    response = []
    for announcement in announcements:
        response.append(
            Course_announcement_response(
                announcement_id=announcement.announcement_id,
                announcement_title=announcement.announcement_title,
                announcement_description=announcement.announcement_description,
                course_id=announcement.course_id
            )
        )

    return response

@app.get("/course/one-announcement/{announcement_id}")
def get_announcement(announcement_id: UUID, db: Session = Depends(get_db)):
    announcement = db.query(models.Course_announcement).filter(models.Course_announcement.announcement_id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return Course_announcement_response(
        announcement_id=announcement.announcement_id,
        announcement_title=announcement.announcement_title,
        announcement_description=announcement.announcement_description,
        course_id=announcement.course_id
    )

@app.put("/course/edit-announcement/{announcement_id}")
def edit_announcement(announcement_id: UUID, new_announcement: Course_announcement_edit, db: db_dependency):
    announcement = db.query(models.Course_announcement).filter(models.Course_announcement.announcement_id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    announcement.announcement_title = new_announcement.announcement_title
    announcement.announcement_description = new_announcement.announcement_description
    db.commit()
    db.refresh(announcement)

    return announcement

@app.delete("/course/delete-announcement/{announcement_id}")
def delete_announcement(announcement_id: UUID, db: db_dependency):
    announcement = db.query(models.Course_announcement).filter(models.Course_announcement.announcement_id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted successfully"}

@app.get("/get-material/{material_id}")
def get_material(material_id: UUID, db: Session = Depends(get_db)):
    material = db.query(models.Course_material).filter(models.Course_material.material_id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return response_models.MaterialResponse(
        material_name=material.material_name,
        material_path=material.material_path
    )

@app.put("/edit-material/{material_id}")
def edit_material(material_id: UUID, new_material: request_models.EditCourseMaterial, db: db_dependency):
    material = db.query(models.Course_material).filter(models.Course_material.material_id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    material.material_name = new_material.material_name
    material.material_path = new_material.material_path
    db.commit()
    db.refresh(material)

    return material

@app.delete("/delete-material/{material_id}")
def delete_material(material_id: UUID, db: db_dependency):
    material = db.query(models.Course_material).filter(models.Course_material.material_id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}

#Admin classes

class LecturersResponse(BaseModel):
    lecturer_id: UUID
    lecturer_name: str
    lecturer_nic: str
    lecturer_phone: str
    lecturer_email: str

class LecturerGetResponse(BaseModel):
    lecturer_id: UUID
    lecturer_name: str
    lecturer_nic: str
    lecturer_phone: str
    lecturer_email: str
    lecturer_password: str

class LecturerEditResponse(BaseModel):
    lecturer_name: str
    lecturer_nic: str
    lecturer_phone: str
    lecturer_email: str
    lecturer_password: str

class AdminCourses(BaseModel):
    course_id: UUID
    course_name: str
    enrollment_key: str
    course_description: str

class CourseRequest(BaseModel):
    course_name: str
    enrollment_key: str
    course_description: str

class StudentRequest(BaseModel):
    student_id: UUID
    email: str

class CreateStudent(BaseModel):
    email: str
    password: str
    

#Admin endpoints

@app.post("/admin/create_lecturer")
def create_lecturer(lecturer: Lecturer, db: Session = Depends(get_db)):
    hash_password = utils.get_password_hash(lecturer.lecturer_password)
    lecturer_data = lecturer.dict(exclude={"lecturer_password"})
    lecturer = models.Lecturer(**lecturer_data, lecturer_password=hash_password)
    db.add(lecturer)
    db.commit()
    db.refresh(lecturer)
    return lecturer


@app.post("/admin/create_admin")
def create_admin(admin: Admin, db: Session = Depends(get_db)):
    hash_password = utils.get_password_hash(admin.admin_password)
    admin_data = admin.dict(exclude={"admin_password"})
    admin = models.Admin(**admin_data, admin_password=hash_password)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@app.get("/admin/lecturers", response_model=List[LecturersResponse])
def get_lecturers(db: Session = Depends(get_db)):
    lecturers = db.query(models.Lecturer).all()
    response = []
    for lecturer in lecturers:
        response.append(LecturersResponse(
            lecturer_id=lecturer.lecturer_id,
            lecturer_name=lecturer.lecturer_name,
            lecturer_nic=lecturer.lecturer_nic,
            lecturer_phone=lecturer.lecturer_phone,
            lecturer_email=lecturer.lecturer_email
        ))
    return response

@app.get("/admin/lecturer/{lecturer_id}")
def get_lecturer(lecturer_id: UUID, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return LecturerGetResponse(
        lecturer_id=lecturer.lecturer_id,
        lecturer_name=lecturer.lecturer_name,
        lecturer_nic=lecturer.lecturer_nic,
        lecturer_phone=lecturer.lecturer_phone,
        lecturer_email=lecturer.lecturer_email,
        lecturer_password=lecturer.lecturer_password
    )

@app.put("/admin/edit_lecturer/{lecturer_id}")
def edit_lecturer(lecturer_id: UUID, new_lecturer: LecturerEditResponse, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    
    lecturer.lecturer_name = new_lecturer.lecturer_name
    lecturer.lecturer_nic = new_lecturer.lecturer_nic
    lecturer.lecturer_phone = new_lecturer.lecturer_phone
    lecturer.lecturer_email = new_lecturer.lecturer_email
    lecturer.lecturer_password = new_lecturer.lecturer_password
    db.commit()
    db.refresh(lecturer)

    return lecturer

@app.delete("/admin/delete_lecturer/{lecturer_id}")
def delete_lecturer(lecturer_id: UUID, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    db.delete(lecturer)
    db.commit()
    return {"message": "Lecturer deleted successfully"}

@app.get("/admin/courses", response_model=List[AdminCourses])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    response = []
    for course in courses:
        response.append(AdminCourses(
            course_id=course.course_id,
            course_name=course.course_name,
            enrollment_key=course.enrollment_key,
            course_description=course.course_description
        ))
    return response

@app.get("/admin/course/{course_id}")
def get_course(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return AdminCourses(
        course_id=course.course_id,
        course_name=course.course_name,
        enrollment_key=course.enrollment_key,
        course_description=course.course_description
    )

@app.delete("/admin/delete_course/{course_id}")
def delete_course(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

@app.post("/admin/create_course")
def create_course(course: CourseRequest, db: Session = Depends(get_db)):
    course = models.Course(**course.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@app.put("/admin/edit_course/{course_id}")
def edit_course(course_id: UUID, new_course: CourseRequest, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.course_name = new_course.course_name
    course.enrollment_key = new_course.enrollment_key
    course.course_description = new_course.course_description
    db.commit()
    db.refresh(course)

    return course

@app.get("/admin/students", response_model=List[StudentRequest])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    response = []
    for student in students:
        response.append(StudentRequest(
            student_id=student.student_id,
            email=student.email
        ))
    return response

@app.delete("/admin/delete_student/{student_id}")
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.post("/admin/create_student")
def create_student(student: request_models.Student, db: Session = Depends(get_db)):
    hash_password = utils.get_password_hash(student.password)
    student_data = student.dict(exclude={"password"})
    student = models.Student(**student_data, password=hash_password)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/admin/student/{student_id}")
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return CreateStudent(
        email=student.email,
        password=student.password
    )

@app.put("/admin/edit_student/{student_id}")
def edit_student(student_id: UUID, new_student: CreateStudent, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.email = new_student.email
    student.password = new_student.password
    db.commit()
    db.refresh(student)

    return student

@app.get("/admin/assigned_lecturers/{course_id}")
def get_assigned_lecturers(course_id: UUID, db: Session = Depends(get_db)):
    assigned_lecturers = (
        db.query(models.Lecturer_assigned_for, models.Lecturer)
        .join(models.Lecturer, models.Lecturer.lecturer_id == models.Lecturer_assigned_for.lecturer_id)
        .filter(models.Lecturer_assigned_for.course_id == course_id)
        .all()
    )

    if not assigned_lecturers:
        raise HTTPException(status_code=404, detail="Lecturers not found for this course")
    
    response = []
    for assignment, lecturer in assigned_lecturers:
        response.append({
            "lecturer_id": lecturer.lecturer_id,
            "lecturer_name": lecturer.lecturer_name
        })
    
    return response

@app.get("/admin/get-all-lecturers")
def get_all_lecturers(db: Session = Depends(get_db)):
    lecturers = db.query(models.Lecturer).all()
    if not lecturers:
        raise HTTPException(status_code=404, detail="No lecturers found")
    
    response = []
    for lecturer in lecturers:
        response.append({
            "lecturer_id": lecturer.lecturer_id,
            "lecturer_name": lecturer.lecturer_name
        })
    
    return response

@app.post("/admin/assign_lecturer/{course_id}/{lecturer_id}")
def assign_lecturer(course_id: UUID, lecturer_id: UUID, db: Session = Depends(get_db)):
    assignment = models.Lecturer_assigned_for(course_id=course_id, semester_id='75cdc5e4-a507-4eef-8778-875b52331a91', program_id='600d59e6-05af-4d02-95a2-c1851d487ff5', lecturer_id=lecturer_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@app.delete("/admin/delete_lecturer_assignment/{course_id}/{lecturer_id}")
def delete_lecturer_assignment(course_id: UUID, lecturer_id: UUID, db: Session = Depends(get_db)):
    assignment = db.query(models.Lecturer_assigned_for).filter(models.Lecturer_assigned_for.course_id == course_id).filter(models.Lecturer_assigned_for.lecturer_id == lecturer_id).first()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}



#Student endpoints

@app.get("/student/profile/{email}")
def get_profile(email: str, db: Session = Depends(get_db)):
    student_profile = db.query(models.Student).filter(models.Student.email == email).first()
    if not student_profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student_profile

@app.get("/student/profile/{student_id}")
def get_profile(email: str, db: Session = Depends(get_db)):
    student_profile = db.query(models.Student).filter(models.Student.email == email).first()
    if not student_profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student_profile

@app.put("/student/edit-email/{student_id}")
def edit_student(student_id: UUID, new_student: StudentEditEmail, db: Session = Depends(get_db)):
    Student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if Student is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    Student.email = new_student.new_email
    db.commit()
    db.refresh(Student)

    return Student

@app.put("/student/edit-password/{student_id}")
def edit_student(student_id: UUID, new_student: StudentEditPassword, db: Session = Depends(get_db)):
    Student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if Student is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if Student.password == new_student.old_password:
        Student.password = new_student.new_password
    else:
        raise HTTPException(status_code=404, detail="Announcement not found")        
    db.commit()
    db.refresh(Student)

    return Student

#student portal
#new student
@app.get("/student-portal/programs", response_model=List[request_models.StPorProgram])
def get_program_details(db: db_dependency):
    db_program =db.query(models.Program).all()
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    available_programs = [
        request_models.StPorProgram(
            program_id = program.program_id,
            program_name = program.program_name,
            program_description = program.program_description,
            duration = program.duration,
            program_image = program.university_image,
        )
        for program in db_program
    ]
    return available_programs

@app.get("/student-portal/program-details/{program_id}")
def get_program_details(program_id: UUID, db: db_dependency):
    program_details = (
        db.query(models.Course_semester_program, models.Program, models.Semester, models.Course)
        .join(models.Program, models.Program.program_id == models.Course_semester_program.program_id)
        .join(models.Semester, models.Semester.semester_id == models.Course_semester_program.semester_id)
        .join(models.Course, models.Course.course_id == models.Course_semester_program.course_id)
        .filter(models.Program.program_id == program_id)
        .all()
    )

    response = []
    for detail in program_details:
        response.append(
            response_models.ProgramDetails(
                course_id = detail.Course.course_id,
                program_name = detail.Program.program_name,
                program_description = detail.Program.program_description,
                university_name = detail.Program.university_name,
                university_image = detail.Program.university_image,
                course_name = detail.Course.course_name,
                course_description = detail.Course.course_description,
                course_image = detail.Course.course_image,
                year = detail.Semester.year,
                semester = detail.Semester.semester
            )
        )
    return response

@app.post("/enroll_new_student")
def enroll_new_student(new_student: request_models.NewStudent, db: db_dependency):

    db_new_student = models.New_student(**new_student.dict())
    db.add(db_new_student)
    db.commit()

    return {"Message":"Student enrolled successfully"}

@app.get("/user-details-for-student-portal/{email}")
def get_student_details(email: str, db: db_dependency):
    result = (
        db.query(models.New_student, models.Student)
        .join(models.Student, models.Student.newStudent_id == models.New_student.newStudent_id)
        .filter(models.Student.email == email)
        .first()
    )
    admin = db.query(models.Admin).filter(models.Admin.admin_email == email).first()
    lecturer = db.query(models.Lecturer).filter(models.Lecturer.lecturer_email == email).first()

    if result:
        new_student, student = result
        name = new_student.name
        image_path = student.image_path
        return response_models.PortalUserDetails(name=name, image_path=image_path)
    elif admin:
        name = admin.admin_name
        image_path = admin.image_path
        return response_models.PortalUserDetails(name=name, image_path=image_path)
    elif lecturer:
        name = lecturer.lecturer_name
        image_path = lecturer.lecturer_image
        return response_models.PortalUserDetails(name=name, image_path=image_path)

@app.post("/register_current_student_to_semester")
def register_current_student_to_semester(new_student: request_models.RegisterStudent, db: db_dependency):
    db_student = models.Payment(**new_student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/student-details/{email}")
def get_student_details(email: str, db: db_dependency):
    result = (
        db.query(models.New_student, models.Student)
        .join(models.Student, models.Student.newStudent_id == models.New_student.newStudent_id)
        .filter(models.Student.email == email)
        .first()
    )

    if result:
        new_student, student = result
        return response_models.StudentDetails(
            student_id=student.student_id,
            name=new_student.name,
            email=student.email,
        )


@app.get("/is_in_payment/{student_id}")
def is_in_payment(student_id: UUID, db: db_dependency):
    result = db.query(models.Payment).filter(models.Payment.student_id == student_id).first()
    ## return the payment details
    if result:
        return response_models.PaymentDetails(
            payment_id=result.payment_id,
            confirmed=result.confirmed
        )
    return {"Message": "Student not in payment"}
        


##student portal admin

@app.get("/new-student-enrollments/{program_id}")
def get_new_student_enrollments(program_id: UUID, db: db_dependency):
    result = (
        db.query(models.New_student)
        .filter(models.New_student.program_id == program_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="New student enrollments not found")
    
    response = []
    for student in result:
        response.append(
            response_models.NewStudents(
                newStudent_id=student.newStudent_id,
                name=student.name,
                address=student.address,
                email=student.email,
                OL_path=student.OL_path,
                AL_path=student.AL_path,
                payment_path=student.payment_path,
                date=student.date.strftime("%Y-%m-%d"),
                confirmed=student.confirmed
            )
        )

    return response

@app.put("/confirm-new-student/{new_student_id}")
def confirm_new_student(new_student_id: UUID, db: db_dependency):
    student = db.query(models.New_student).filter(models.New_student.newStudent_id == new_student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    password = utils.get_password_hash(student.email)

    if not student.confirmed:
        db_student = models.Student(
            email = student.email,
            password = password,
            semester_id = '75cdc5e4-a507-4eef-8778-875b52331a91',
            newStudent_id = student.newStudent_id
        )
        db.add(db_student)
        db.commit()
    
    if student.confirmed:
        db.query(models.Student).filter(models.Student.newStudent_id == new_student_id).delete()
        db.commit()
    
    student.confirmed = not student.confirmed
    db.commit()
    db.refresh(student)

    return {"Message": "Student confirmed successfully"}


@app.get("/current-student-payments")
def get_current_student_payments(db: db_dependency):
    result = (
        db.query(models.Payment, models.Student)
        .join(models.Student, models.Student.student_id == models.Payment.student_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Payments not found")
    
    response = []
    for payment, student in result:
        response.append(
            response_models.CurrentStudentPayment(
                payment_id=payment.payment_id,
                email=student.email,
                date = payment.date.strftime("%Y-%m-%d"),
                receipt_path=payment.receipt_path,
                confirmed=payment.confirmed
            )
        )
    
    return response

@app.put("/confirm-current-student-payment/{payment_id}")
def confirm_current_student_payment(payment_id: UUID, db: db_dependency):
    payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if not payment.confirmed:
        db_program_semester_student = models.Program_semester_student(
            program_id = '600d59e6-05af-4d02-95a2-c1851d487ff5',
            semester_id = '321e7ded-204a-465f-b327-d59a27c802b4',
            student_id = payment.student_id
        )
        db.add(db_program_semester_student)
        db.commit()

        db.query(models.Student).filter(models.Student.student_id == payment.student_id).update({"semester_id": '321e7ded-204a-465f-b327-d59a27c802b4'})
        db.commit()
    
    if payment.confirmed:
        db.query(models.Program_semester_student).filter(models.Program_semester_student.student_id == payment.student_id).delete()
        db.commit()

        db.query(models.Student).filter(models.Student.student_id == payment.student_id).update({"semester_id": '75cdc5e4-a507-4eef-8778-875b52331a91'})
        db.commit()
    
    payment.confirmed = not payment.confirmed
    db.commit()
    db.refresh(payment)

    return {"Message": "Payment confirmed successfully"}

    

