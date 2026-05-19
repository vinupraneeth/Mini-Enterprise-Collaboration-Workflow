from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskCreate(BaseModel):

    title: str
    description: Optional[str] = None
    assigned_to: int


class TaskResponse(BaseModel):

    id: int
    title: str
    description: Optional[str]
    status: str
    
    assigned_to: int

    created_by: int
    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True


class TaskStatusEnum(str, Enum):

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskStatusUpdate(BaseModel):

    status: TaskStatusEnum