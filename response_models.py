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