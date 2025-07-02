import asyncio
import json
import threading
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect
import numpy as np

from app.crud.keyword import get_keywords_by_user_id
from app.database import SessionLocal
from app.models.alerts import Alert
from app.service.audio_worker import analyze_block
from app.schemas.voice_data import VoiceData, VoiceDataCreate, VoiceDataUpdate
from app.crud import voice_data as crud_voice
from app.dependencies import get_db
import sounddevice as sd

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


ws_clients = []
listening = False
current_user_id = None

SAMPLE_RATE = 16000
BLOCK_DURATION = 1.0
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)
user_keywords = []  # 预加载关键词

try:
    db = SessionLocal()
    if current_user_id is not None:
        user_keywords = get_keywords_by_user_id(db, current_user_id)
finally:
    db.close()

def audio_loop():
    global listening
    print("🎤 audio_loop 正在运行中")
    audio_buffer = []  # 用于累积 2 秒音频

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32',
            blocksize=BLOCK_SIZE
        ) as stream:
            while listening:
                block = stream.read(BLOCK_SIZE)[0]  # 1 秒
                audio_buffer.append(block)

                if len(audio_buffer) >= 2:
                    full_block = np.concatenate(audio_buffer, axis=0)  # 合成 2 秒
                    audio_buffer.clear()

                    result = analyze_block(full_block, user_keywords)
                    try:
                        db = SessionLocal()
                        if current_user_id is not None:
                            create_alert_if_needed(result, db, current_user_id)
                    finally:
                        db.close()

                    # 异步广播给所有连接的前端
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(broadcast_result(result))
    except Exception as e:
        print("音频采集异常：", e)


async def broadcast_result(data):
    to_remove = []
    for ws in ws_clients:
        try:
            await ws.send_json(data)
        except:
            to_remove.append(ws)
    for ws in to_remove:
        ws_clients.remove(ws)

def create_alert_if_needed(result: dict, db: Session, user_id: int):
    trigger_count = 0
    trigger_details = []

    # 1. VOSK 中是否检测到霸凌关键词
    if result["keywords"]:
        trigger_count += 1
        trigger_details.append(f"关键词命中：{'，'.join(result['keywords'])}")

    # 2. YAMNet 检测是否是危险声音
    if result.get("is_danger_event"):
        top_event = result["events"][0]
        trigger_count += 1
        trigger_details.append(f"检测到危险声音：{top_event['label']}（置信度 {top_event['score']:.2f}）")

    # 3. Emotion2Vec 检测是否为危险情绪
    danger_emotions = ["angry", "fear", "disgust"]
    if result["emotion"]:
        label = result["emotion"]["label"]
        score = result["emotion"]["score"]
        if label in danger_emotions:
            trigger_count += 1
            trigger_details.append(f"情绪识别：{label}（置信度 {score:.2f}）")

    # 没有触发就不创建警告
    if trigger_count == 0:
        return None

    # 等级划分
    level_map = {1: "低", 2: "中", 3: "高"}
    level = level_map.get(trigger_count, "低")

    # 构建描述
    description_lines = [
        f"触发模型数：{trigger_count}，预警等级：{level}",
        f"原始语音识别文本：{result['text'] or '无识别内容'}",
        *trigger_details
    ]
    full_description = "\n".join(description_lines)

    alert = Alert(
        user_id=user_id,
        type="语音霸凌检测",
        level=level,
        description=full_description,
        timestamp=datetime.fromisoformat(result["timestamp"]),
        status="未处理"
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.websocket("/ws/audio-stream")
async def audio_stream_ws(websocket: WebSocket):
    await websocket.accept()
    print("websocket已连接")

    global listening, current_user_id

    # 第一次接收到的消息应是 user_id
    init_msg = await websocket.receive_text()
    try:
        current_user_id = int(json.loads(init_msg)["user_id"])
        print("当前用户 ID:", current_user_id)
    except Exception:
        await websocket.close()
        print("❌ 未提供合法 user_id")
        return

    ws_clients.append(websocket)

    if not listening:
        listening = True
        threading.Thread(target=audio_loop, daemon=True).start()

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients.remove(websocket)
        print("客户端断开 WebSocket")
        if not ws_clients:
            listening = False
            current_user_id = None
