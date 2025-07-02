from sqlalchemy.orm import Session
from app.models.alerts import Alert
from app.schemas.alerts import AlertCreate, AlertUpdate
from typing import List, Optional, Any


def get_alert(db: Session, alert_id: int) -> Optional[Alert]:
    return db.query(Alert).filter(Alert.id == alert_id).first()

def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> list[type[Alert]]:
    return db.query(Alert).offset(skip).limit(limit).all()

def create_alert(db: Session, alert: AlertCreate) -> Alert:
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_alert(db: Session, alert_id: int, alert: AlertUpdate) -> Optional[Alert]:
    db_alert = get_alert(db, alert_id)
    if not db_alert:
        return None
    update_data = alert.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_alert, key, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def delete_alert(db: Session, alert_id: int) -> bool:
    db_alert = get_alert(db, alert_id)
    if not db_alert:
        return False
    db.delete(db_alert)
    db.commit()
    return True
