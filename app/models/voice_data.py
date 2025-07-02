
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class VoiceData(Base):
    __tablename__ = "voice_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    keywords = Column(String(255))
    emotion = Column(String(50))
    event = Column(String(100))
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="voice_data")
