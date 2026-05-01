"""
数据库配置
==========

包含数据库连接、会话管理和基础模型类。
使用SQLAlchemy 2.0异步模式。
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 创建数据库引擎
# SQLite需要启用check_same_thread=False
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖项

    使用示例:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            pass

    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库

    创建所有表。在应用启动时调用。
    """
    Base.metadata.create_all(bind=engine)
