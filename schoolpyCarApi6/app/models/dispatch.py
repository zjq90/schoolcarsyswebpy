"""
调度消息模型
=============

调度消息表，存储给司机的调度消息。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Dispatch(Base):
    """
    调度消息表

    Attributes:
        id: 调度ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        route_id: 路线ID，外键
        title: 调度标题
        content: 调度内容
        dispatch_time: 调度时间
        estimated_arrival_time: 预计到达时间
        actual_arrival_time: 实际到达时间
        status: 状态：1-待接收，2-已接收，3-执行中，4-已完成，5-已取消
        dispatcher_id: 调度人ID
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="车辆ID")
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True, comment="路线ID")
    title = Column(String(200), nullable=False, comment="调度标题")
    content = Column(Text, nullable=False, comment="调度内容")
    dispatch_time = Column(DateTime, nullable=False, comment="调度时间")
    estimated_arrival_time = Column(DateTime, nullable=True, comment="预计到达时间")
    actual_arrival_time = Column(DateTime, nullable=True, comment="实际到达时间")
    status = Column(Integer, default=1, comment="状态: 1-待接收, 2-已接收, 3-执行中, 4-已完成, 5-已取消")
    dispatcher_id = Column(Integer, nullable=True, comment="调度人ID")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="dispatches")
    vehicle = relationship("Vehicle", backref="dispatches")
    route = relationship("Route", backref="dispatches")

    def __repr__(self):
        return f"<Dispatch(id={self.id}, title={self.title})>"
