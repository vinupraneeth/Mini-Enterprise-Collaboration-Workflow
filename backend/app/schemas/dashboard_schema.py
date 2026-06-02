from pydantic import BaseModel


class AiSummaryResponse(BaseModel):

    pending_tasks: int

    high_priority_tasks: int

    delayed_tasks: int

    insights: list[str]
