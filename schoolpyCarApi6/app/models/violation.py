"""
违章记录模型
=============

违章记录表，存储司机的违章信息。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Violation(Base):
    """
    违章记录表

    Attributes:
        id: 违章ID，主键
        driver_id: 司机ID，外键
        vehicle_id: 车辆ID，外键
        violation_no: 违章编号
        violation_type: 违章类型：1-超速，2-闯红灯，3-违规停车，4-其他
        violation_time: 违章时间
        violation_address: 违章地点
        latitude: 违章地点纬度
        longitude: 违章地点经度
        description: 违章描述
        fine_amount: 罚款金额（分）
        deduct_points: 扣分
        status: 状态：1-未处理，2-已处理，3-已申诉
        handle_time: 处理时间
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False, comment="司机ID")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="车辆ID")
    violation_no = Column(String(50), unique=True, nullable=True, comment="违章编号")
    violation_type = Column(Integer, default=4, comment="违章类型: 1-超速, 2-闯红灯, 3-违规停车, 4-其他")
    violation_time = Column(DateTime, nullable=False, comment="违章时间")
    violation_address = Column(String(200), nullable=False, comment="违章地点")
    latitude = Column(DECIMAL(10, 7), nullable=True, comment="违章地点纬度")
    longitude = Column(DECIMAL(10, 7), nullable=True, comment="违章地点经度")
    description = Column(Text, nullable=True, comment="违章描述")
    fine_amount = Column(Integer, default=0, comment="罚款金额(分)")
    deduct_points = Column(Integer, default=0, comment="扣分")
    status = Column(Integer, default=1, comment="状态: 1-未处理, 2-已处理, 3-已申诉")
    handle_time = Column(DateTime, nullable=True, comment="处理时间")
    remark = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    driver = relationship("Driver", backref="violations")
    vehicle = relationship("Vehicle", backref="violations")

    def __repr__(self):
        return f"<Violation(id={self.id}, violation_no={self.violation_no})>"
