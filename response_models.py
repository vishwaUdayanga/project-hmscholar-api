from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class MaterialResponse(BaseModel):
    material_name: str
    material_path: str