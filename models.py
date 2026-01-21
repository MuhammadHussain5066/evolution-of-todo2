from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional["User"] = Relationship(back_populates="tasks")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str

    tasks: list["Task"] = Relationship(back_populates="owner")


