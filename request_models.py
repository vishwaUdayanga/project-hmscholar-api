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
    
class StudentCourseResponse(BaseModel):
    course_id: UUID
    course_name: str
    year: int
    enrollment_key: str
    semester: int

class StudentProfile(BaseModel):
  student_id:UUID
  email: str
  name: str
  program:str
  password: str
  student_image:str

class AdminAnnouncements(BaseModel):
    admin_id:UUID
    admin_name: str
    title:str
    description: str
    admin_image:str


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



