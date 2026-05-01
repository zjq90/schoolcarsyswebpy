"""
FastAPI主应用文件
"""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.routers import (
    alarm_router, bus_router, driver_router, student_router,
    user_router, alarm_level_router, alarm_type_router, location_router, test_router
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="校车后台管理系统 - 应急报警响应管理平台"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 模板目录
templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates")

# 注册路由
app.include_router(alarm_router)
app.include_router(bus_router)
app.include_router(driver_router)
app.include_router(student_router)
app.include_router(user_router)
app.include_router(alarm_level_router)
app.include_router(alarm_type_router)
app.include_router(location_router)
app.include_router(test_router)


def read_html(filename: str) -> str:
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# 页面路由
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return read_html("index.html")


@app.get("/alarms", response_class=HTMLResponse)
async def alarms_page(request: Request):
    return read_html("alarms.html")


@app.get("/buses", response_class=HTMLResponse)
async def buses_page(request: Request):
    return read_html("buses.html")


@app.get("/drivers", response_class=HTMLResponse)
async def drivers_page(request: Request):
    return read_html("drivers.html")


@app.get("/students", response_class=HTMLResponse)
async def students_page(request: Request):
    return read_html("students.html")


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return read_html("settings.html")


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    return read_html("test.html")


# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }
