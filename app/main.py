from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user, voice_data, rfid_data, alerts, keyword

app = FastAPI(
    title="Monitoring System Backend",
    description="用于语音 + RFID 多模态校园霸凌监控的后端系统",
    version="1.0.0",
    docs_url="/docs",  # 默认是 /docs，确保没有禁用
    redoc_url="/redoc",
    openapi_url="/openapi.json"  # 确保默认路径没被改动
)

# 跨域支持，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议替换为指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user.router,prefix="/users", tags=["users"])
app.include_router(alerts.router,prefix="/alerts", tags=["alerts"])
app.include_router(keyword.router,prefix="/keywords", tags=["keywords"])
app.include_router(rfid_data.router,prefix="/rfid_data", tags=["RFID 数据"])
app.include_router(voice_data.router,prefix="/voice_data", tags=["voice_data"])
"""






"""
# 根路由可选
@app.get("/")
def read_root():
    return {"message": "Welcome to Monitoring System Backend"}

@app.get("/test")
def read_test():
    return {"message": "test"}