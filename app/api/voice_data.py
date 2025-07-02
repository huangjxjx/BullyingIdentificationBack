from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.voice_data import VoiceData, VoiceDataCreate, VoiceDataUpdate
from app.crud import voice_data as crud_voice
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=VoiceData)
def create_data(data: VoiceDataCreate, db: Session = Depends(get_db)):
    return crud_voice.create_voice_data(db, data)

@router.get("/{data_id}", response_model=VoiceData)
def read_data(data_id: int, db: Session = Depends(get_db)):
    db_data = crud_voice.get_voice_data(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="语音数据不存在")
    return db_data

@router.get("/", response_model=List[VoiceData])
def read_data_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_voice.get_voice_data_list(db, skip, limit)

@router.put("/{data_id}", response_model=VoiceData)
def update_data(data_id: int, data: VoiceDataUpdate, db: Session = Depends(get_db)):
    updated = crud_voice.update_voice_data(db, data_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="语音数据不存在")
    return updated

@router.delete("/{data_id}", response_model=dict)
def delete_data(data_id: int, db: Session = Depends(get_db)):
    success = crud_voice.delete_voice_data(db, data_id)
    if not success:
        raise HTTPException(status_code=404, detail="语音数据不存在")
    return {"message": "删除成功"}
