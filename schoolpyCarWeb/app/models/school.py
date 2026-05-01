"""
学校数据模型
定义学校的基本信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base


class School(Base):
    """
    学校表
    存储学校基本信息
    """
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True, comment="学校ID，主键")
    school_name = Column(String(100), nullable=False, comment="学校名称")
    school_code = Column(String(50), unique=True, index=True, comment="学校编码")
    address = Column(String(255), comment="学校地址")
    principal = Column(String(50), comment="校长姓名")
    contact_phone = Column(String(20), comment="联系电话")
    description = Column(Text, comment="学校简介")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    admins = relationship("User", back_populates="school")
    vehicles = relationship("Vehicle", back_populates="school")
    drivers = relationship("Driver", back_populates="school")
    students = relationship("Student", back_populates="school")
    routes = relationship("Route", back_populates="school")

    def __repr__(self):
        return f"<School(id={self.id}, name={self.school_name})>"
