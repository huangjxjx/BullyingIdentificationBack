# app/init_db.py

from app.database import Base, engine
from app.models import user, voice_data, rfid_data, alerts, keyword

def init_db():
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("创建完成")

if __name__ == "__main__":
    init_db()
