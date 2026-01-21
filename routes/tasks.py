from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

# ✅ Correct imports
from db import get_session
from models import Task, User
from dependencies.auth import get_current_user  # JWT verification

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --------------------------
# Pydantic Schemas
# --------------------------
class TaskCreate(BaseModel):
    title: str
    description: str = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# --------------------------
# Routes
# --------------------------

# 🔹 Get all tasks for current user
@router.get("/", response_model=List[Task])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Task).where(Task.user_id == current_user.id)
    )
    tasks = result.scalars().all()
    return tasks

# 🔹 Create a new task
@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
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

# 🔹 Update a task
@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    existing_task = result.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None:
        existing_task.title = task.title
    if task.description is not None:
        existing_task.description = task.description
    if task.completed is not None:
        existing_task.completed = task.completed

    session.add(existing_task)
    await session.commit()
    await session.refresh(existing_task)
    return existing_task

# 🔹 Delete a task
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task_to_delete = result.scalar_one_or_none()
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task_to_delete)
    await session.commit()
    return {"detail": "Task deleted successfully"}

