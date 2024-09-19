from pydantic import BaseModel
from uuid import UUID

class Section(BaseModel):
    section_name: str
    section_description: str
    course_id: UUID

class Course_Material(BaseModel):
    material_name: str
    material_path: str
    section_id: UUID