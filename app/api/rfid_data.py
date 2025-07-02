from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import rfid_data as schemas
from app.crud import rfid_data as crud

router = APIRouter()

@router.post("/", response_model=schemas.RFIDDataOut)
def create(data: schemas.RFIDDataCreate, db: Session = Depends(get_db)):
    return crud.create_rfid_data(db, data)

@router.get("/{data_id}", response_model=schemas.RFIDDataOut)
def read(data_id: int, db: Session = Depends(get_db)):
    db_data = crud.get_rfid_data(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="数据未找到")
    return db_data

@router.get("/", response_model=list[schemas.RFIDDataOut])
def read_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rfid_data_list(db, skip=skip, limit=limit)

@router.put("/{data_id}", response_model=schemas.RFIDDataOut)
def update(data_id: int, update: schemas.RFIDDataUpdate, db: Session = Depends(get_db)):
    db_data = crud.update_rfid_data(db, data_id, update)
    if not db_data:
        raise HTTPException(status_code=404, detail="更新失败：数据不存在")
    return db_data

@router.delete("/{data_id}")
def delete(data_id: int, db: Session = Depends(get_db)):
    db_data = crud.delete_rfid_data(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="删除失败：数据不存在")
    return {"msg": "删除成功"}
