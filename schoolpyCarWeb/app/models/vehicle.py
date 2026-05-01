"""
车辆数据模型
定义校车的基本信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Vehicle(Base):
    """
    车辆表
    存储校车基本信息
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, comment="车辆ID，主键")
    vehicle_code = Column(String(50), unique=True, index=True, comment="车辆编码")
    license_plate = Column(String(20), unique=True, nullable=False, comment="车牌号")
    vehicle_model = Column(String(100), comment="车辆型号")
    seat_count = Column(Integer, nullable=False, comment="座位数")
    purchase_date = Column(Date, comment="购置时间")
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="所属学校ID")
    campus = Column(String(100), comment="校区")
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True, comment="所属司机ID")
    status = Column(String(20), default="available", comment="状态：available(可用) / in_use(使用中) / maintenance(维护中) / disabled(停用)")
    insurance_expire = Column(Date, comment="保险到期日期")
    inspection_expire = Column(Date, comment="年检到期日期")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    school = relationship("School", back_populates="vehicles")
    driver = relationship("Driver", back_populates="vehicles")

    def __repr__(self):
        return f"<Vehicle(id={self.id}, license_plate={self.license_plate})>"
