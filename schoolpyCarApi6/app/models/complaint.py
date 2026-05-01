"""
投诉模型
=========

投诉表，存储家长提交的投诉信息。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Complaint(Base):
    """
    投诉表

    Attributes:
        id: 投诉ID，主键
        parent_id: 家长ID，外键
        student_id: 学生ID，外键
        title: 投诉标题
        content: 投诉内容
        images: 图片URL列表（JSON格式）
        complaint_type: 投诉类型：1-司机服务，2-车辆问题，3-路线问题，4-其他
        status: 状态：1-待处理，2-处理中，3-已处理，4-已关闭
        handler_id: 处理人ID
        handler_remark: 处理备注
        handle_time: 处理时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False, comment="家长ID")
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True, comment="学生ID")
    title = Column(String(200), nullable=False, comment="投诉标题")
    content = Column(Text, nullable=False, comment="投诉内容")
    images = Column(Text, nullable=True, comment="图片URL列表(JSON)")
    complaint_type = Column(Integer, default=4, comment="投诉类型: 1-司机服务, 2-车辆问题, 3-路线问题, 4-其他")
    status = Column(Integer, default=1, comment="状态: 1-待处理, 2-处理中, 3-已处理, 4-已关闭")
    handler_id = Column(Integer, nullable=True, comment="处理人ID")
    handler_remark = Column(Text, nullable=True, comment="处理备注")
    handle_time = Column(DateTime, nullable=True, comment="处理时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    parent = relationship("Parent", backref="complaints")
    student = relationship("Student", backref="complaints")

    def __repr__(self):
        return f"<Complaint(id={self.id}, title={self.title})>"
