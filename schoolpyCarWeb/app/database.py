"""
数据库连接和会话管理模块
使用SQLAlchemy作为ORM框架
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# 创建数据库引擎
# SQLite需要添加check_same_thread=False参数
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖函数
    在FastAPI路由中使用Depends(get_db)来获取数据库会话
    使用yield实现上下文管理，确保会话正确关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库
    创建所有表
    """
    Base.metadata.create_all(bind=engine)
