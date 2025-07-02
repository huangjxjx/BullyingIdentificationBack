from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.keyword import Keyword, KeywordCreate, KeywordUpdate
from app.crud import keyword as crud_keywords
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Keyword)
def create_keyword(keyword: KeywordCreate, db: Session = Depends(get_db)):
    return crud_keywords.create_keyword(db, keyword)

@router.get("/{keyword_id}", response_model=Keyword)
def read_keyword(keyword_id: int, db: Session = Depends(get_db)):
    db_keyword = crud_keywords.get_keyword(db, keyword_id)
    if not db_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@router.get("/", response_model=List[Keyword])
def read_keywords(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_keywords.get_keywords(db, skip, limit)

@router.put("/{keyword_id}", response_model=Keyword)
def update_keyword(keyword_id: int, keyword: KeywordUpdate, db: Session = Depends(get_db)):
    db_keyword = crud_keywords.update_keyword(db, keyword_id, keyword)
    if not db_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@router.delete("/{keyword_id}", response_model=dict)
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    success = crud_keywords.delete_keyword(db, keyword_id)
    if not success:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return {"message": "Keyword deleted successfully"}
