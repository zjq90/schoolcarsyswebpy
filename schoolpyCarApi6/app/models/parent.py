"""
家长信息模型
============

家长信息表，存储家长的详细信息。
与User表是一对一关系。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Parent(Base):
    """
    家长信息表

    Attributes:
        id: 家长ID，主键
        user_id: 关联的用户ID，外键
        real_name: 真实姓名
        id_card: 身份证号
        address: 家庭地址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="关联用户ID")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    address = Column(String(200), nullable=True, comment="家庭地址")
    emergency_contact = Column(String(50), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    user = relationship("User", backref="parent_info")

    def __repr__(self):
        return f"<Parent(id={self.id}, real_name={self.real_name})>"
