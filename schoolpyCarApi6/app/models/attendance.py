"""
司机打卡记录模型
=================

司机上下班打卡记录表。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Attendance(Base):
    """
    司机上下班打卡记录表

    Attributes:
        id: 记录ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        attendance_date: 打卡日期
        check_in_time: 上班打卡时间
        check_in_latitude: 上班打卡纬度
        check_in_longitude: 上班打卡经度
        check_in_address: 上班打卡地址
        check_out_time: 下班打卡时间
        check_out_latitude: 下班打卡纬度
        check_out_longitude: 下班打卡经度
        check_out_address: 下班打卡地址
        status: 状态：1-正常，2-迟到，3-早退，4-缺勤
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="车辆ID")
    attendance_date = Column(DateTime, nullable=False, comment="打卡日期")
    check_in_time = Column(DateTime, nullable=True, comment="上班打卡时间")
    check_in_latitude = Column(DECIMAL(10, 7), nullable=True, comment="上班打卡纬度")
    check_in_longitude = Column(DECIMAL(10, 7), nullable=True, comment="上班打卡经度")
    check_in_address = Column(String(200), nullable=True, comment="上班打卡地址")
    check_out_time = Column(DateTime, nullable=True, comment="下班打卡时间")
    check_out_latitude = Column(DECIMAL(10, 7), nullable=True, comment="下班打卡纬度")
    check_out_longitude = Column(DECIMAL(10, 7), nullable=True, comment="下班打卡经度")
    check_out_address = Column(String(200), nullable=True, comment="下班打卡地址")
    status = Column(Integer, default=1, comment="状态: 1-正常, 2-迟到, 3-早退, 4-缺勤")
    remark = Column(String(500), nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="attendances")
    vehicle = relationship("Vehicle", backref="attendances")

    def __repr__(self):
        return f"<Attendance(id={self.id}, driver_id={self.driver_id}, attendance_date={self.attendance_date})>"
