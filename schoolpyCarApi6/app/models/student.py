"""
学生信息模型
============

学生信息表，存储学生的详细信息。
"""

from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base


class Student(Base):
    """
    学生信息表

    Attributes:
        id: 学生ID，主键
        student_no: 学号
        real_name: 真实姓名
        gender: 性别：1-男，2-女
        birth_date: 出生日期
        school: 学校
        class_name: 班级
        grade: 年级
        address: 家庭住址
        contact_phone: 联系电话
        status: 状态：1-在读，0-休学
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_no = Column(String(20), unique=True, nullable=True, comment="学号")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    gender = Column(Integer, nullable=True, comment="性别: 1-男, 2-女")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    school = Column(String(100), nullable=True, comment="学校")
    class_name = Column(String(50), nullable=True, comment="班级")
    grade = Column(String(20), nullable=True, comment="年级")
    address = Column(String(200), nullable=True, comment="家庭住址")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    status = Column(Integer, default=1, comment="状态: 1-在读, 0-休学")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Student(id={self.id}, real_name={self.real_name})>"
