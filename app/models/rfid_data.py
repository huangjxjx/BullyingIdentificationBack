# app/models/rfid_data.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class RFIDData(Base):
    __tablename__ = "rfid_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event = Column(String(100))
    confidence = Column(Float)
    position_data = Column(Text)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="rfid_data")