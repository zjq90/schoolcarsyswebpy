"""
司机车辆绑定模型
=================

司机与车辆的绑定表。
一个司机在一个时间段只能绑定一辆车，一辆车在一个时间段只能被一个司机绑定。
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class DriverVehicle(Base):
    """
    司机与车辆绑定表

    Attributes:
        id: 绑定ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        bind_time: 绑定时间
        unbind_time: 解绑时间
        status: 状态：1-已绑定，0-已解绑
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "driver_vehicle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="车辆ID")
    bind_time = Column(DateTime, nullable=False, comment="绑定时间")
    unbind_time = Column(DateTime, nullable=True, comment="解绑时间")
    status = Column(Integer, default=1, comment="状态: 1-已绑定, 0-已解绑")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="vehicle_bindings")
    vehicle = relationship("Vehicle", backref="driver_bindings")

    def __repr__(self):
        return f"<DriverVehicle(id={self.id}, driver_id={self.driver_id}, vehicle_id={self.vehicle_id})>"
