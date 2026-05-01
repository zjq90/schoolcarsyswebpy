"""
校车管理系统后端API
===================

技术栈: Python + SQLite + FastAPI + SQLAlchemy

模块说明:
- models: 数据库模型定义
- schemas: Pydantic数据模型（请求/响应验证）
- routers: API路由定义（家长端、司机端）
- utils: 工具函数（JWT认证、密码加密、验证码等）
- database.py: 数据库连接配置
- dependencies.py: 依赖项（数据库会话、认证等）
- config.py: 配置文件
- main.py: 应用入口
"""

__version__ = "1.0.0"
__author__ = "SchoolCar API Team"
