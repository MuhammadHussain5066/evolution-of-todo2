from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True   # pydantic v2 (orm_mode ka replacement)
