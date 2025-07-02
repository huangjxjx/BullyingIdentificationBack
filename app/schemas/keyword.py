from pydantic import BaseModel
from typing import Optional

class KeywordBase(BaseModel):
    user_id: int
    keyword: str

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(BaseModel):
    keyword: Optional[str] = None

class Keyword(KeywordBase):
    id: int

    class Config:
        from_attributes = True
