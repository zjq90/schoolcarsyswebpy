"""
学生数据模型
定义学生的基本信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    """
    学生表
    存储学生基本信息
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, comment="学生ID，主键")
    student_code = Column(String(50), unique=True, index=True, comment="学生学号")
    real_name = Column(String(50), nullable=False, comment="姓名")
    gender = Column(String(10), comment="性别")
    birthday = Column(Date, comment="出生日期")
    id_card = Column(String(18), unique=True, comment="身份证号")
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="所属学校ID")
    grade = Column(String(20), comment="年级")
    class_name = Column(String(50), comment="班级")
    parent_name = Column(String(50), comment="家长姓名")
    parent_phone = Column(String(20), comment="家长联系电话")
    home_address = Column(String(255), comment="家庭住址")
    pickup_address = Column(String(255), comment="上车地址")
    dropoff_address = Column(String(255), comment="下车地址")
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True, comment="所属路线ID")
    status = Column(String(20), default="active", comment="状态：active(在校) / transferred(转学) / graduated(毕业)")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    school = relationship("School", back_populates="students")
    route = relationship("Route", back_populates="students")

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.real_name})>"
