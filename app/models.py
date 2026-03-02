from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CheckRequest(BaseModel):
    url: str
    timeout: int = 5

class CheckResult(BaseModel):
    url: str
    status: str
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    checked_at: datetime

class HealthResponse(BaseModel):
    status: str 
    version: str