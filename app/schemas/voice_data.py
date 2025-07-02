from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VoiceDataBase(BaseModel):
    content: str
    keywords: Optional[str]
    emotion: Optional[str]
    event: Optional[str]
    timestamp: datetime

class VoiceDataCreate(VoiceDataBase):
    user_id: int

class VoiceDataUpdate(BaseModel):
    content: Optional[str]
    keywords: Optional[str]
    emotion: Optional[str]
    event: Optional[str]
    timestamp: Optional[datetime]

class VoiceData(VoiceDataBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True