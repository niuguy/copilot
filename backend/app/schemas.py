from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UsageItem(BaseModel):
    id: int
    timestamp: datetime
    report_name: Optional[str] = None
    credits: float


class ChartDataItem(BaseModel):
    date: str
    credits: float


class UsageResponse(BaseModel):
    usage: List[UsageItem]
    total_credits: float


class UsageChartResponse(BaseModel):
    usage: List[UsageItem]
    total_credits: float
    chart_data: List[ChartDataItem]
