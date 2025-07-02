from datetime import date, timedelta
from typing import Optional, List, cast

from sqlalchemy import func, Date
from sqlalchemy.orm import Session

from app.models.alerts import Alert
from app.schemas.alerts import AlertCreate, AlertUpdate, AlertDailyCount


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

def get_alerts_by_user_id(db: Session, user_id: int):
    return db.query(Alert).filter(Alert.user_id == user_id).order_by(Alert.timestamp.desc()).all()



def get_alert_count_by_date_range(db: Session, user_id: int, start_date: date, end_date: date) -> List[AlertDailyCount]:
    date_expr = func.date(Alert.timestamp)

    raw_results = (
        db.query(
            date_expr.label("alert_date"),
            func.count(Alert.id)
        )
        .filter(
            Alert.user_id == user_id,  # ✅ 根据用户过滤
            Alert.timestamp >= start_date,
            Alert.timestamp <= end_date
        )
        .group_by(date_expr)
        .order_by(date_expr)
        .all()
    )

    result_map = {row.alert_date: row[1] for row in raw_results}

    # 补全每一天的结果
    current_date = start_date
    full_results = []
    while current_date <= end_date:
        count = result_map.get(current_date, 0)
        full_results.append(AlertDailyCount(date=current_date, count=count))
        current_date += timedelta(days=1)

    return full_results


def get_alert_type_counts_by_date_range(db: Session, user_id: int, start_date: date, end_date: date) -> dict:
    results = (
        db.query(Alert.type, func.count(Alert.id))
        .filter(
            Alert.user_id == user_id,  # ✅ 添加用户筛选条件
            Alert.timestamp >= start_date,
            Alert.timestamp <= end_date
        )
        .group_by(Alert.type)
        .all()
    )

    default_types = ["语音霸凌检测", "RFID霸凌检测"]
    counts = {type_: 0 for type_ in default_types}

    for type_, count in results:
        counts[type_] = count

    return counts
