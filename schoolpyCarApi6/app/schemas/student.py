"""
学生数据模型
=============

包含学生相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class StudentCreate(BaseModel):
    """
    学生创建模型

    Attributes:
        student_no: 学号
        real_name: 真实姓名
        gender: 性别：1-男，2-女
        birth_date: 出生日期
        school: 学校
        class_name: 班级
        grade: 年级
        address: 家庭住址
        contact_phone: 联系电话
    """

    student_no: Optional[str] = Field(None, max_length=20, description="学号")
    real_name: str = Field(..., max_length=50, description="真实姓名")
    gender: Optional[int] = Field(None, description="性别: 1-男, 2-女")
    birth_date: Optional[date] = Field(None, description="出生日期")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    class_name: Optional[str] = Field(None, max_length=50, description="班级")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    address: Optional[str] = Field(None, max_length=200, description="家庭住址")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")


class StudentUpdate(BaseModel):
    """
    学生更新模型

    Attributes:
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
    """

    student_no: Optional[str] = Field(None, max_length=20, description="学号")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    gender: Optional[int] = Field(None, description="性别: 1-男, 2-女")
    birth_date: Optional[date] = Field(None, description="出生日期")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    class_name: Optional[str] = Field(None, max_length=50, description="班级")
    grade: Optional[str] = Field(None, max_length=20, description="年级")
    address: Optional[str] = Field(None, max_length=200, description="家庭住址")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    status: Optional[int] = Field(None, description="状态: 1-在读, 0-休学")


class StudentResponse(BaseModel):
    """
    学生响应模型

    Attributes:
        id: 学生ID
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

    id: int = Field(..., description="学生ID")
    student_no: Optional[str] = Field(None, description="学号")
    real_name: str = Field(..., description="真实姓名")
    gender: Optional[int] = Field(None, description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    school: Optional[str] = Field(None, description="学校")
    class_name: Optional[str] = Field(None, description="班级")
    grade: Optional[str] = Field(None, description="年级")
    address: Optional[str] = Field(None, description="家庭住址")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class StudentWithRelationResponse(StudentResponse):
    """
    带关系的学生响应模型

    Attributes:
        relation: 与家长的关系
    """

    relation: Optional[str] = Field(None, description="与家长的关系")


__all__ = [
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "StudentWithRelationResponse",
]
