from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db import get_session
from models import Task, User
from dependencies.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --------------------------
# Pydantic Schemas
# --------------------------

class TaskCreate(BaseModel):
    title: str
    description: str = ""

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --------------------------
# Routes
# --------------------------

@router.get("/", response_model=List[TaskOut])
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Task).where(Task.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=TaskOut)
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task
