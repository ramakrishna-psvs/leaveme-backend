from pydantic import BaseModel
from datetime import date


class LeaveCreate(BaseModel):
    reason: str
    start_date: date
    end_date: date


class LeaveResponse(BaseModel):
    id: int
    reason: str
    start_date: date
    end_date: date
    status: str
    user_id: int

    class Config:
        from_attributes = True
