from sqlalchemy.orm import Session
from app.models.voice_data import VoiceData
from app.schemas.voice_data import VoiceDataCreate, VoiceDataUpdate
from typing import Optional, List, Any


def get_voice_data(db: Session, data_id: int) -> Optional[VoiceData]:
    return db.query(VoiceData).filter(VoiceData.id == data_id).first()

def get_voice_data_list(db: Session, skip: int = 0, limit: int = 100) -> list[type[VoiceData]]:
    return db.query(VoiceData).offset(skip).limit(limit).all()

def create_voice_data(db: Session, data: VoiceDataCreate) -> VoiceData:
    db_data = VoiceData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def update_voice_data(db: Session, data_id: int, data: VoiceDataUpdate) -> Optional[VoiceData]:
    db_data = get_voice_data(db, data_id)
    if not db_data:
        return None
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data, key, value)
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_voice_data(db: Session, data_id: int) -> bool:
    db_data = get_voice_data(db, data_id)
    if not db_data:
        return False
    db.delete(db_data)
    db.commit()
    return True
