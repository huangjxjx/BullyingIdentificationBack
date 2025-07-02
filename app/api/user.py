from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin
from app.crud import user as crud_user
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud_user.create_user(db, user)

@router.get("/{username}", response_model=User)
def read_user(username:str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username)
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_user.get_users(db, skip, limit)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}

@router.post("/login", response_model=User)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return db_user
