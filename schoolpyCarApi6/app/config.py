"""
配置文件
========

包含系统的所有配置项:
- 数据库配置
- JWT认证配置
- 短信验证码配置
- 分页配置等
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """系统配置类"""

    # 应用配置
    APP_NAME: str = "校车管理系统API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./schoolcar.db"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时

    # 短信验证码配置
    SMS_CODE_EXPIRE_MINUTES: int = 5  # 5分钟
    SMS_CODE_LENGTH: int = 6

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # 用户类型
    USER_TYPE_PARENT: str = "parent"
    USER_TYPE_DRIVER: str = "driver"
    USER_TYPE_ADMIN: str = "admin"

    # 消息类型
    MESSAGE_TYPE_PARENT: str = "parent"
    MESSAGE_TYPE_DRIVER: str = "driver"

    # 家长消息分类
    PARENT_MESSAGE_CATEGORIES: list = [
        "学生违规消息",
        "学生上下学消息",
        "车辆状况提醒",
        "投诉反馈",
    ]

    # 司机消息分类
    DRIVER_MESSAGE_CATEGORIES: list = [
        "学生违规提醒",
        "紧急状况提醒",
        "路线规划提醒",
        "违章提醒",
        "车辆保养提醒",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
