from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RFIDDataBase(BaseModel):
    user_id: int
    event: str
    confidence: Optional[float] = None
    position_data: Optional[str] = None
    timestamp: datetime

class RFIDDataCreate(RFIDDataBase):
    pass

class RFIDDataUpdate(BaseModel):
    event: Optional[str] = None
    confidence: Optional[float] = None
    position_data: Optional[str] = None
    timestamp: Optional[datetime] = None

class RFIDDataOut(RFIDDataBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
