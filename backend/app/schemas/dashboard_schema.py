from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class DelayRiskTask(BaseModel):

    task_id: int

    title: str

    priority: str

    status: str

    due_date: datetime | None = None

    assigned_to: int | None = None

    assigned_to_name: str | None = None

    risk_score: int

    reasons: list[str] = Field(
        default_factory=list
    )


class AssignmentCandidate(BaseModel):

    user_id: int

    name: str

    email: str

    active_tasks: int

    high_priority_tasks: int

    overdue_tasks: int

    completed_tasks: int

    score: int


class AssignmentRecommendation(AssignmentCandidate):

    reason: str


class AiSummaryResponse(BaseModel):

    pending_tasks: int

    high_priority_tasks: int

    delayed_tasks: int

    insights: list[str]

    delay_risks: list[DelayRiskTask] = Field(
        default_factory=list
    )


class SmartAssignmentResponse(BaseModel):

    recommendation: AssignmentRecommendation | None = None

    candidates: list[AssignmentCandidate] = Field(
        default_factory=list
    )
