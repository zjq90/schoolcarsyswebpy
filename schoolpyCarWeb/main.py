"""
校车管理系统主应用入口文件
使用FastAPI框架，提供RESTful API和静态HTML页面
"""
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.config import STATIC_DIR, TEMPLATES_DIR
from app.database import init_db
from app.routers import (
    auth_router, user_router, school_router,
    vehicle_router, driver_router, student_router,
    route_router, policy_router, dispatch_router
)

# 创建FastAPI应用实例
app = FastAPI(
    title="校车管理系统",
    description="基于Python+SQLite+FastAPI+Bootstrap的校车web后台管理系统",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 配置模板引擎
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 注册路由
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(school_router)
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(student_router)
app.include_router(route_router)
app.include_router(policy_router)
app.include_router(dispatch_router)


@app.on_event("startup")
async def startup_event():
    """
    应用启动时执行的事件
    初始化数据库
    """
    init_db()
    print("校车管理系统启动成功！")
    print(f"API文档地址: http://localhost:8080/api/docs")
    print(f"系统访问地址: http://localhost:8080/")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    首页路由
    返回登录页面
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    仪表盘页面
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/schools", response_class=HTMLResponse)
async def schools_page(request: Request):
    """
    学校管理页面
    """
    return templates.TemplateResponse("schools.html", {"request": request})


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """
    用户管理页面
    """
    return templates.TemplateResponse("users.html", {"request": request})


@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request):
    """
    车辆管理页面
    """
    return templates.TemplateResponse("vehicles.html", {"request": request})


@app.get("/drivers", response_class=HTMLResponse)
async def drivers_page(request: Request):
    """
    司机管理页面
    """
    return templates.TemplateResponse("drivers.html", {"request": request})


@app.get("/students", response_class=HTMLResponse)
async def students_page(request: Request):
    """
    学生管理页面
    """
    return templates.TemplateResponse("students.html", {"request": request})


@app.get("/routes", response_class=HTMLResponse)
async def routes_page(request: Request):
    """
    路线管理页面
    """
    return templates.TemplateResponse("routes.html", {"request": request})


@app.get("/policies", response_class=HTMLResponse)
async def policies_page(request: Request):
    """
    政策管理页面
    """
    return templates.TemplateResponse("policies.html", {"request": request})


@app.get("/dispatches", response_class=HTMLResponse)
async def dispatches_page(request: Request):
    """
    调度管理页面
    """
    return templates.TemplateResponse("dispatches.html", {"request": request})


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """
    测试功能页面
    """
    return templates.TemplateResponse("test.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
