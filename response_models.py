from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class MaterialResponse(BaseModel):
    material_name: str
    material_path: str

class ProgramDetails(BaseModel):
    program_name: str
    program_description: Optional[str] = None
    university_name: str
    university_image: Optional[str] = None
    course_name: str
    course_description: Optional[str] = None
    course_image: Optional[str] = None
    year: int
    semester: int

class PortalUserDetails(BaseModel):
    name: str
    image_path: Optional[str] = None

class StudentDetails(BaseModel):
    student_id: UUID
    name: str
    email: str

class NewStudents(BaseModel):
    newStudent_id: UUID
    name: str
    address: str
    email: str
    OL_path: str
    AL_path: str
    payment_path: str
    date: str
    confirmed: bool

class CurrentStudentPayment(BaseModel):
    payment_id: UUID
    email: str
    date: str
    receipt_path: str
    confirmed: bool

class PaymentDetails(BaseModel):
    payment_id: UUID
    confirmed: bool


