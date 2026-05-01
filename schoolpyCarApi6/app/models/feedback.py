"""
反馈模型
=========

反馈表，存储司机提交的处理结果反馈和车辆保养反馈。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Feedback(Base):
    """
    反馈表

    Attributes:
        id: 反馈ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        feedback_type: 反馈类型：1-处理结果反馈，2-车辆保养反馈
        title: 反馈标题
        content: 反馈内容
        images: 图片URL列表（JSON格式）
        related_message_id: 关联消息ID
        status: 状态：1-待审核，2-已通过，3-已驳回
        reviewer_id: 审核人ID
        reviewer_remark: 审核备注
        review_time: 审核时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True, comment="车辆ID")
    feedback_type = Column(Integer, nullable=False, comment="反馈类型: 1-处理结果反馈, 2-车辆保养反馈")
    title = Column(String(200), nullable=False, comment="反馈标题")
    content = Column(Text, nullable=False, comment="反馈内容")
    images = Column(Text, nullable=True, comment="图片URL列表(JSON)")
    related_message_id = Column(Integer, nullable=True, comment="关联消息ID")
    status = Column(Integer, default=1, comment="状态: 1-待审核, 2-已通过, 3-已驳回")
    reviewer_id = Column(Integer, nullable=True, comment="审核人ID")
    reviewer_remark = Column(Text, nullable=True, comment="审核备注")
    review_time = Column(DateTime, nullable=True, comment="审核时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="feedbacks")
    vehicle = relationship("Vehicle", backref="feedbacks")

    def __repr__(self):
        return f"<Feedback(id={self.id}, title={self.title})>"
