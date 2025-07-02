from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

    class Config:
        from_attributes = True  # orm_mode 替代
