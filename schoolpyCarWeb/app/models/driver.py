"""
司机数据模型
定义司机的基本信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Driver(Base):
    """
    司机表
    存储司机基本信息
    """
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True, comment="司机ID，主键")
    driver_code = Column(String(50), unique=True, index=True, comment="司机编码")
    real_name = Column(String(50), nullable=False, comment="姓名")
    id_card = Column(String(18), unique=True, comment="身份证号")
    phone = Column(String(20), comment="联系电话")
    gender = Column(String(10), comment="性别")
    birthday = Column(Date, comment="出生日期")
    address = Column(String(255), comment="家庭住址")
    driving_years = Column(Integer, default=0, comment="驾龄（年）")
    health_status = Column(String(50), default="良好", comment="健康状况")
    license_number = Column(String(50), unique=True, comment="驾驶证号")
    license_type = Column(String(20), comment="准驾车型")
    license_expire = Column(Date, comment="驾驶证有效期")
    qualification_cert = Column(String(50), unique=True, comment="从业资格证号")
    qualification_expire = Column(Date, comment="从业资格证有效期")
    no_crime_record = Column(Boolean, default=True, comment="是否无犯罪记录")
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="所属学校ID")
    status = Column(String(20), default="available", comment="状态：available(可用) / on_duty(值班) / on_leave(休假) / disabled(停用)")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    school = relationship("School", back_populates="drivers")
    vehicles = relationship("Vehicle", back_populates="driver")

    def __repr__(self):
        return f"<Driver(id={self.id}, name={self.real_name})>"
