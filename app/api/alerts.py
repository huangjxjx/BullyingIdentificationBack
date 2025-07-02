from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.alerts import Alert, AlertCreate, AlertUpdate
from app.crud import alerts as crud_alerts
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Alert)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    return crud_alerts.create_alert(db, alert)

@router.get("/{alert_id}", response_model=Alert)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = crud_alerts.get_alert(db, alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert

@router.get("/", response_model=List[Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_alerts.get_alerts(db, skip, limit)

@router.put("/{alert_id}", response_model=Alert)
def update_alert(alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db)):
    db_alert = crud_alerts.update_alert(db, alert_id, alert)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert

@router.delete("/{alert_id}", response_model=dict)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    success = crud_alerts.delete_alert(db, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted successfully"}
