"""
消息分类模型
============

消息分类表，定义所有消息的分类。
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class MessageCategory(Base):
    """
    消息分类表

    Attributes:
        id: 分类ID，主键
        name: 分类名称
        code: 分类代码
        message_type: 消息类型：parent(家长端)、driver(司机端)
        description: 分类描述
        sort_order: 排序
        status: 状态：1-启用，0-禁用
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "message_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="分类名称")
    code = Column(String(50), unique=True, nullable=False, comment="分类代码")
    message_type = Column(String(20), nullable=False, comment="消息类型: parent/driver")
    description = Column(String(200), nullable=True, comment="分类描述")
    sort_order = Column(Integer, default=0, comment="排序")
    status = Column(Integer, default=1, comment="状态: 1-启用, 0-禁用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<MessageCategory(id={self.id}, name={self.name})>"
