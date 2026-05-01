"""
校车管理系统API主入口
=====================

FastAPI应用入口文件，包含应用配置、路由注册、事件处理等。
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routers import parent_router, driver_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    应用启动时初始化数据库连接和表结构。
    """
    print(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}...")

    init_db()

    print(f"{settings.APP_NAME} 启动成功!")

    yield

    print(f"{settings.APP_NAME} 关闭中...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="校车管理系统后端API，支持家长端和司机端功能",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parent_router)
app.include_router(driver_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理器

    处理所有未捕获的异常，返回统一的错误响应。
    """
    if settings.DEBUG:
        import traceback
        detail = traceback.format_exc()
    else:
        detail = "服务器内部错误"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": str(exc),
            "data": {"detail": detail} if settings.DEBUG else None
        }
    )


@app.get("/", tags=["根路径"])
async def root():
    """
    根路径接口

    返回应用基本信息。
    """
    return {
        "code": 200,
        "message": "success",
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查接口

    用于检查服务是否正常运行。
    """
    return {
        "code": 200,
        "message": "success",
        "data": {
            "status": "healthy",
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
    }
