from sqlalchemy.orm import Session
from app.models.rfid_data import RFIDData
from app.schemas.rfid_data import RFIDDataCreate, RFIDDataUpdate


def create_rfid_data(db: Session, data: RFIDDataCreate):
    db_data = RFIDData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_rfid_data(db: Session, data_id: int):
    return db.query(RFIDData).filter(RFIDData.id == data_id).first()


def get_rfid_data_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RFIDData).offset(skip).limit(limit).all()


def update_rfid_data(db: Session, data_id: int, update: RFIDDataUpdate):
    db_data = get_rfid_data(db, data_id)
    if not db_data:
        return None
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data, key, value)
    db.commit()
    db.refresh(db_data)
    return db_data


def delete_rfid_data(db: Session, data_id: int):
    db_data = get_rfid_data(db, data_id)
    if not db_data:
        return None
    db.delete(db_data)
    db.commit()
    return db_data