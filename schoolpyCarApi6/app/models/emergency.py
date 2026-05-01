"""
紧急状况申请模型
=================

紧急状况申请表，存储司机提交的紧急状况申请。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Emergency(Base):
    """
    紧急状况申请表

    Attributes:
        id: 申请ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        emergency_type: 紧急类型：1-车辆故障，2-交通事故，3-学生突发状况，4-其他
        title: 紧急情况标题
        content: 紧急情况描述
        latitude: 发生位置纬度
        longitude: 发生位置经度
        location_address: 发生位置地址
        images: 图片URL列表（JSON格式）
        status: 状态：1-待处理，2-处理中，3-已处理，4-已关闭
        handler_id: 处理人ID
        handler_remark: 处理备注
        handle_time: 处理时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "emergencies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="车辆ID")
    emergency_type = Column(Integer, default=4, comment="紧急类型: 1-车辆故障, 2-交通事故, 3-学生突发状况, 4-其他")
    title = Column(String(200), nullable=False, comment="紧急情况标题")
    content = Column(Text, nullable=False, comment="紧急情况描述")
    latitude = Column(DECIMAL(10, 7), nullable=True, comment="发生位置纬度")
    longitude = Column(DECIMAL(10, 7), nullable=True, comment="发生位置经度")
    location_address = Column(String(200), nullable=True, comment="发生位置地址")
    images = Column(Text, nullable=True, comment="图片URL列表(JSON)")
    status = Column(Integer, default=1, comment="状态: 1-待处理, 2-处理中, 3-已处理, 4-已关闭")
    handler_id = Column(Integer, nullable=True, comment="处理人ID")
    handler_remark = Column(Text, nullable=True, comment="处理备注")
    handle_time = Column(DateTime, nullable=True, comment="处理时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="emergencies")
    vehicle = relationship("Vehicle", backref="emergencies")

    def __repr__(self):
        return f"<Emergency(id={self.id}, title={self.title})>"
