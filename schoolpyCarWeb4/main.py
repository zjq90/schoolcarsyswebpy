"""
校车管理系统 - 主应用文件
FastAPI应用入口，整合所有路由和静态文件服务
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date

# 导入路由
from routers.driver import router as driver_router
from routers.maintenance import router as maintenance_router
from routers.message import router as message_router

# 导入DAO层用于首页数据统计
from dao.driver_dao import DriverDAO, DriverScoreDAO
from dao.maintenance_dao import VehicleDAO, MaintenanceDAO
from dao.message_dao import StudentDAO, MessagePushDAO, BusStatusDAO

# 创建FastAPI应用
app = FastAPI(
    title="校车管理系统",
    description="基于Python + FastAPI + SQLite + Bootstrap的校车Web后台管理系统",
    version="1.0.0"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 配置模板目录
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=template_dir)

# 注册路由
app.include_router(driver_router)
app.include_router(maintenance_router)
app.include_router(message_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    首页仪表盘
    展示系统统计数据和快捷入口
    """
    # 获取统计数据
    stats = {
        "driver_count": DriverDAO.get_count(),
        "vehicle_count": VehicleDAO.get_count(),
        "student_count": StudentDAO.get_count(),
        "score_count": DriverScoreDAO.get_count(),
        "maintenance_count": MaintenanceDAO.get_count(),
        "message_count": MessagePushDAO.get_count(),
        "bus_status_count": BusStatusDAO.get_count(),
    }
    
    # 获取最近的消息推送记录
    recent_messages = MessagePushDAO.get_recent(24)
    
    # 获取最近的校车状态
    recent_status = BusStatusDAO.get_recent(24)
    
    # 获取司机评分统计（最近30天平均分）
    drivers = DriverDAO.get_all()
    driver_scores = []
    for driver in drivers[:5]:  # 只取前5个司机
        avg_score = DriverScoreDAO.get_average_score(driver['id'], 30)
        driver_scores.append({
            "id": driver['id'],
            "name": driver['name'],
            "avg_score": round(avg_score, 2) if avg_score else 0
        })
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stats": stats,
            "recent_messages": recent_messages[:10],
            "recent_status": recent_status[:10],
            "driver_scores": driver_scores,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


@app.get("/drivers", response_class=HTMLResponse)
async def drivers_page(request: Request):
    """
    司机管理页面
    """
    drivers = DriverDAO.get_all()
    return templates.TemplateResponse(
        "drivers.html",
        {"request": request, "drivers": drivers}
    )


@app.get("/driver-scores", response_class=HTMLResponse)
async def driver_scores_page(request: Request):
    """
    司机评分页面
    """
    scores = DriverScoreDAO.get_all()
    drivers = DriverDAO.get_all()
    return templates.TemplateResponse(
        "driver_scores.html",
        {"request": request, "scores": scores[:100], "drivers": drivers}
    )


@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request):
    """
    车辆管理页面
    """
    vehicles = VehicleDAO.get_all()
    return templates.TemplateResponse(
        "vehicles.html",
        {"request": request, "vehicles": vehicles}
    )


@app.get("/maintenance", response_class=HTMLResponse)
async def maintenance_page(request: Request):
    """
    运维记录页面
    """
    records = MaintenanceDAO.get_all()
    vehicles = VehicleDAO.get_all()
    drivers = DriverDAO.get_all()
    return templates.TemplateResponse(
        "maintenance.html",
        {"request": request, "records": records[:100], "vehicles": vehicles, "drivers": drivers}
    )


@app.get("/students", response_class=HTMLResponse)
async def students_page(request: Request):
    """
    学生管理页面
    """
    students = StudentDAO.get_all()
    return templates.TemplateResponse(
        "students.html",
        {"request": request, "students": students}
    )


@app.get("/message-logs", response_class=HTMLResponse)
async def message_logs_page(request: Request):
    """
    消息推送记录页面
    """
    logs = MessagePushDAO.get_all()
    students = StudentDAO.get_all()
    return templates.TemplateResponse(
        "message_logs.html",
        {"request": request, "logs": logs[:100], "students": students}
    )


@app.get("/bus-status", response_class=HTMLResponse)
async def bus_status_page(request: Request):
    """
    校车状态页面
    """
    status_logs = BusStatusDAO.get_all()
    vehicles = VehicleDAO.get_all()
    drivers = DriverDAO.get_all()
    return templates.TemplateResponse(
        "bus_status.html",
        {"request": request, "status_logs": status_logs[:100], "vehicles": vehicles, "drivers": drivers}
    )


@app.get("/api/stats")
async def get_statistics():
    """
    获取系统统计数据API
    """
    # 运维类型统计
    maintenance_stats = MaintenanceDAO.get_statistics_by_type()
    
    # 消息类型统计
    message_types = ["上车刷卡", "下车刷卡", "校车发车", "校车到站", "异常通知"]
    message_stats = []
    for msg_type in message_types:
        logs = MessagePushDAO.get_by_type(msg_type, limit=9999)
        message_stats.append({
            "type": msg_type,
            "count": len(logs)
        })
    
    # 状态类型统计
    status_types = ["发车", "到站", "正常", "异常"]
    status_stats = []
    for status_type in status_types:
        logs = BusStatusDAO.get_by_type(status_type, limit=9999)
        status_stats.append({
            "type": status_type,
            "count": len(logs)
        })
    
    return JSONResponse({
        "maintenance_stats": maintenance_stats,
        "message_stats": message_stats,
        "status_stats": status_stats
    })


# 启动应用
if __name__ == "__main__":
    import uvicorn
    
    # 检查数据库是否存在，不存在则初始化
    from config import DATABASE
    if not os.path.exists(DATABASE['path']):
        print("数据库不存在，正在初始化...")
        from database.init_db import init_database
        init_database()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
