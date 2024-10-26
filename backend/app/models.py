from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Message(BaseModel):
    id: int
    text: str
    timestamp: datetime
    report_id: Optional[int] = None


class Report(BaseModel):
    id: int
    name: str
    credit_cost: float

