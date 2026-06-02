from pydantic import BaseModel

from datetime import datetime


class TaskCreate(BaseModel):

    title: str

    description: str

    priority: str

    due_date: datetime | None = None

    assigned_to: int


class TaskUpdate(BaseModel):

    title: str

    description: str

    priority: str

    due_date: datetime | None = None

    assigned_to: int


class TaskStatusUpdate(BaseModel):

    status: str

class TaskAssign(BaseModel):

    assigned_to: int

class TaskResponse(BaseModel):

    id: int

    title: str

    description: str

    status: str

    priority: str

    due_date: datetime | None = None

    assigned_to: int

    assigned_to_name: str | None = None

    created_by: int

    created_by_name: str | None = None

    created_at: datetime | None = None

    approval_status: str | None = None

    approval_remarks: str | None = None

    class Config:

        from_attributes = True


class TaskHistoryResponse(BaseModel):

    id: int
    task_id: int
    old_status: str
    new_status: str
    changed_by: int
    created_at: datetime

    class Config:
        from_attributes = True
