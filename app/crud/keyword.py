from sqlalchemy.orm import Session
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from typing import List, Optional, Any


def get_keyword(db: Session, keyword_id: int) -> Optional[Keyword]:
    return db.query(Keyword).filter(Keyword.id == keyword_id).first()

def get_keywords(db: Session, skip: int = 0, limit: int = 100) -> list[type[Keyword]]:
    return db.query(Keyword).offset(skip).limit(limit).all()

def create_keyword(db: Session, keyword: KeywordCreate) -> Keyword:
    db_keyword = Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def update_keyword(db: Session, keyword_id: int, keyword: KeywordUpdate) -> Optional[Keyword]:
    db_keyword = get_keyword(db, keyword_id)
    if not db_keyword:
        return None
    update_data = keyword.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_keyword, key, value)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def delete_keyword(db: Session, keyword_id: int) -> bool:
    db_keyword = get_keyword(db, keyword_id)
    if not db_keyword:
        return False
    db.delete(db_keyword)
    db.commit()
    return True

def get_keywords_by_user_id(db: Session, user_id: int):
    return db.query(Keyword).filter(Keyword.user_id == user_id).all()
