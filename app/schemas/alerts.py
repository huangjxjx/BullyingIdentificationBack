from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class AlertBase(BaseModel):
    user_id: int
    type: str
    level: Optional[str] = None
    description: Optional[str] = None
    timestamp: datetime  # ✅ 改为 timestamp
    status: Optional[str] = "未处理"

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    type: Optional[str] = None
    level: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None  # ✅ 改为 timestamp
    status: Optional[str] = None

class Alert(AlertBase):
    id: int

class AlertDailyCount(BaseModel):
    date: date
    count: int

class AlertRangeQuery(BaseModel):
    user_id: int
    start_date: date
    end_date: date

    class Config:
        from_attributes = True  # orm_mode 替代
