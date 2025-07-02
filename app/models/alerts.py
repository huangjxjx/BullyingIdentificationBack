from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))
    level = Column(String(20))
    description = Column(Text)
    timestamp = Column(DateTime)
    status = Column(String(20))

    user = relationship("User", back_populates="alerts")
