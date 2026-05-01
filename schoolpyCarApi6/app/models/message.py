"""
消息推送模型
============

消息推送表，存储所有推送的消息。
支持家长端和司机端的消息推送。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Message(Base):
    """
    消息推送表

    Attributes:
        id: 消息ID，主键
        title: 消息标题
        content: 消息内容
        message_type: 消息类型：parent(家长端)、driver(司机端)
        category_id: 消息分类ID
        receiver_id: 接收者ID（家长ID或司机ID）
        user_id: 关联的用户ID
        is_read: 是否已读：0-未读，1-已读
        read_time: 阅读时间
        extra_data: 额外数据（JSON格式）
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="消息标题")
    content = Column(Text, nullable=True, comment="消息内容")
    message_type = Column(String(20), nullable=False, comment="消息类型: parent/driver")
    category_id = Column(Integer, ForeignKey("message_categories.id"), nullable=True, comment="消息分类ID")
    receiver_id = Column(Integer, nullable=False, comment="接收者ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="关联用户ID")
    is_read = Column(Integer, default=0, comment="是否已读: 0-未读, 1-已读")
    read_time = Column(DateTime, nullable=True, comment="阅读时间")
    extra_data = Column(Text, nullable=True, comment="额外数据(JSON)")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    category = relationship("MessageCategory", backref="messages")
    user = relationship("User", backref="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, title={self.title})>"
