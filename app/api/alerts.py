from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.crud.alerts import get_alert_count_by_date_range, get_alert_type_counts_by_date_range
from app.schemas.alerts import Alert, AlertCreate, AlertUpdate, AlertDailyCount, AlertRangeQuery
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

@router.get("/user/{user_id}", response_model=List[Alert])
def get_alerts_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud_alerts.get_alerts_by_user_id(db, user_id)

@router.post("/count-by-date", response_model=List[AlertDailyCount])
def count_alerts_by_date_range(query: AlertRangeQuery, db: Session = Depends(get_db)):
    if query.start_date > query.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before or equal to end date")
    return get_alert_count_by_date_range(db, query.user_id, query.start_date, query.end_date)


@router.post("/count-by-type", response_model=dict)
def count_alerts_by_type_range(query: AlertRangeQuery, db: Session = Depends(get_db)):
    if query.start_date > query.end_date:
        raise HTTPException(status_code=400, detail="开始日期不能晚于结束日期")
    return get_alert_type_counts_by_date_range(db, query.user_id, query.start_date, query.end_date)
