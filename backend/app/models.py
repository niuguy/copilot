from datetime import datetime
from typing import Optional

class Message:
    def __init__(self, id: int, text: str, timestamp: datetime, report_id: Optional[int] = None):
        self.id = id
        self.text = text
        self.timestamp = timestamp
        self.report_id = report_id

class Report:
    def __init__(self, id: int, name: str, credit_cost: float):
        self.id = id
        self.name = name
        self.credit_cost = credit_cost
