from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from config import STATIC_DIR, TEMPLATES_DIR
from database import init_db, SessionLocal
from models import User, UserRole
from routers.auth import get_password_hash
from routers import auth, users, buses, routes, driver_behaviors, student_behaviors, captures, duties, traffic, test


def init_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                real_name="系统管理员",
                phone="13800138000",
                email="admin@school.com",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("=" * 50)
            print("默认管理员账号已创建:")
            print("  用户名: admin")
            print("  密码: admin123")
            print("=" * 50)
    except Exception as e:
        print(f"初始化管理员时出错: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_default_admin()
    yield


app = FastAPI(
    title="校车后台管理系统",
    description="基于FastAPI的校车司机行为检测、学生行为检测、动态避堵、值班管理系统",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(buses.router)
app.include_router(routes.router)
app.include_router(driver_behaviors.router)
app.include_router(student_behaviors.router)
app.include_router(captures.router)
app.include_router(duties.router)
app.include_router(traffic.router)
app.include_router(test.router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/driver-behaviors")
async def driver_behaviors_page(request: Request):
    return templates.TemplateResponse("driver_behaviors.html", {"request": request})


@app.get("/student-behaviors")
async def student_behaviors_page(request: Request):
    return templates.TemplateResponse("student_behaviors.html", {"request": request})


@app.get("/captures")
async def captures_page(request: Request):
    return templates.TemplateResponse("captures.html", {"request": request})


@app.get("/routes")
async def routes_page(request: Request):
    return templates.TemplateResponse("routes.html", {"request": request})


@app.get("/traffic")
async def traffic_page(request: Request):
    return templates.TemplateResponse("traffic.html", {"request": request})


@app.get("/duties")
async def duties_page(request: Request):
    return templates.TemplateResponse("duties.html", {"request": request})


@app.get("/users")
async def users_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})


@app.get("/test")
async def test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
