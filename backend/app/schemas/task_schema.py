from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class TaskCreate(BaseModel):

    title: str

    description: Optional[str] = None

    priority: str = "medium"

    due_date: Optional[datetime] = None

    assigned_to: int


class TaskUpdate(BaseModel):

    title: str

    description: Optional[str] = None

    priority: str

    status: str

    due_date: Optional[datetime] = None

    assigned_to: int


class TaskStatusUpdate(BaseModel):

    status: str


class TaskAssign(BaseModel):

    assigned_to: int


class TaskResponse(BaseModel):

    id: int

    title: str

    description: Optional[str]

    status: str

    priority: str

    due_date: Optional[datetime]

    assigned_to: int

    created_by: int

    class Config:

        from_attributes = True