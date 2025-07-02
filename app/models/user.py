from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True)

    voice_data = relationship("VoiceData", back_populates="user")
    rfid_data = relationship("RFIDData", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    keywords = relationship("Keyword", back_populates="user")
