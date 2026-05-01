"""
司机信息模型
============

司机信息表，存储司机的详细信息。
与User表是一对一关系。
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Driver(Base):
    """
    司机信息表

    Attributes:
        id: 司机ID，主键
        user_id: 关联的用户ID，外键
        real_name: 真实姓名
        id_card: 身份证号
        driver_license_no: 驾驶证号
        driver_license_type: 驾驶证类型
        driver_license_expiry: 驾驶证有效期
        phone: 联系电话
        address: 住址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
        status: 状态：1-在职，0-离职
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="关联用户ID")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    driver_license_no = Column(String(50), nullable=True, comment="驾驶证号")
    driver_license_type = Column(String(20), nullable=True, comment="驾驶证类型")
    driver_license_expiry = Column(Date, nullable=True, comment="驾驶证有效期")
    phone = Column(String(20), nullable=True, comment="联系电话")
    address = Column(String(200), nullable=True, comment="住址")
    emergency_contact = Column(String(50), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    status = Column(Integer, default=1, comment="状态: 1-在职, 0-离职")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    user = relationship("User", backref="driver_info")

    def __repr__(self):
        return f"<Driver(id={self.id}, real_name={self.real_name})>"
