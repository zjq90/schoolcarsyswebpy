"""
车辆信息模型
============

车辆信息表，存储校车的详细信息。
"""

from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base


class Vehicle(Base):
    """
    车辆信息表

    Attributes:
        id: 车辆ID，主键
        plate_no: 车牌号
        vehicle_no: 车辆编号
        vehicle_type: 车辆类型
        brand: 品牌
        model: 型号
        color: 颜色
        seat_count: 座位数
        buy_date: 购买日期
        last_maintenance_date: 最后保养日期
        next_maintenance_date: 下次保养日期
        mileage: 行驶里程(公里)
        status: 状态：1-可用，0-维修中，2-报废
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plate_no = Column(String(20), unique=True, nullable=False, comment="车牌号")
    vehicle_no = Column(String(20), unique=True, nullable=True, comment="车辆编号")
    vehicle_type = Column(String(50), nullable=True, comment="车辆类型")
    brand = Column(String(50), nullable=True, comment="品牌")
    model = Column(String(50), nullable=True, comment="型号")
    color = Column(String(20), nullable=True, comment="颜色")
    seat_count = Column(Integer, nullable=True, comment="座位数")
    buy_date = Column(Date, nullable=True, comment="购买日期")
    last_maintenance_date = Column(Date, nullable=True, comment="最后保养日期")
    next_maintenance_date = Column(Date, nullable=True, comment="下次保养日期")
    mileage = Column(Integer, default=0, comment="行驶里程(公里)")
    status = Column(Integer, default=1, comment="状态: 1-可用, 0-维修中, 2-报废")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Vehicle(id={self.id}, plate_no={self.plate_no})>"
