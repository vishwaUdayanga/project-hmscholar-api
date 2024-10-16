from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class Login(BaseModel):
    user_name: str
    password: str

class Section(BaseModel):
    section_name: str
    section_description: str
    course_id: UUID

class Course_Material(BaseModel):
    material_name: str
    material_path: str
    section_id: UUID

class EditCourseMaterial(BaseModel):
    material_name: str
    material_path: str

class Question(BaseModel):
    questionText: str
    questionMarks: int
    questionType: str
    answer2: Optional[str] = None
    answer3: Optional[str] = None
    answer4: Optional[str] = None
    correctAnswer: Optional[str] = None

class Quiz(BaseModel):
    quiz_name: str
    quiz_duration: int
    quiz_total_marks: int
    quiz_description: str
    quiz_password: str
    quiz_number_of_questions: int
    questions: List[Question]
    section_id: UUID

class Student(BaseModel):
    email:str
    password:str
    semester_id:UUID
    newStudent_id:UUID

class SectionEdit(BaseModel):
    section_name: str
    section_description: str

class EditLecturerImage(BaseModel):
    lecturer_image: str

class LecturerEdit(BaseModel):
    lecturer_name: str
    lecturer_nic: str
    lecturer_phone: str
    lecturer_email: str

class CourseSettings(BaseModel):
    course_name: str
    enrollment_key: str
    course_description: str
    course_image: Optional[str] = None

##portal
class StPorProgram(BaseModel):
    program_id: UUID
    program_name: str
    program_description: Optional[str] = None
    duration: str
    program_image: Optional[str] = None

class NewStudent(BaseModel):
    name: str
    address: str
    email: str
    OL_path: str
    AL_path: str
    payment_path: str
    program_id: UUID

class RegisterStudent(BaseModel):
    student_id: UUID
    receipt_path: str




