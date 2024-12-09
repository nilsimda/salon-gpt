import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


# Agent
class Agent(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
        use_enum_values = True


class ListAgentsResponse(BaseModel):
    agents: list[Agent]


class AgentTaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    date_done: str
    exception_snippet: Optional[str] = None
    name: str
    retries: int
