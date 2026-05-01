"""
用户基础模型
============

用户表，存储所有系统用户的基础信息。
用户类型包括：家长(parent)、司机(driver)、管理员(admin)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    用户基础表

    Attributes:
        id: 用户ID，主键
        phone: 手机号，唯一索引，用于登录
        password_hash: 密码哈希值
        user_type: 用户类型：parent(家长)、driver(司机)、admin(管理员)
        nickname: 昵称
        avatar: 头像URL
        status: 状态：1-正常，0-禁用
        last_login_time: 最后登录时间
        last_login_ip: 最后登录IP
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(20), unique=True, index=True, nullable=False, comment="手机号")
    password_hash = Column(String(255), nullable=True, comment="密码哈希")
    user_type = Column(String(20), nullable=False, comment="用户类型: parent/driver/admin")
    nickname = Column(String(50), nullable=True, comment="昵称")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    status = Column(Integer, default=1, comment="状态: 1-正常, 0-禁用")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(50), nullable=True, comment="最后登录IP")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone}, user_type={self.user_type})>"
