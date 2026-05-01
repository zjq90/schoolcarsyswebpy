"""
学生Pydantic模式定义
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class StudentBase(BaseModel):
    """
    学生基础模式
    """
    student_code: str
    real_name: str
    gender: Optional[str] = None
    birthday: Optional[date] = None
    id_card: Optional[str] = None
    school_id: int
    grade: Optional[str] = None
    class_name: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    home_address: Optional[str] = None
    pickup_address: Optional[str] = None
    dropoff_address: Optional[str] = None
    route_id: Optional[int] = None
    status: str = "active"
    remarks: Optional[str] = None


class StudentCreate(StudentBase):
    """
    学生创建模式
    """
    pass


class StudentUpdate(BaseModel):
    """
    学生更新模式
    """
    student_code: Optional[str] = None
    real_name: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    id_card: Optional[str] = None
    school_id: Optional[int] = None
    grade: Optional[str] = None
    class_name: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    home_address: Optional[str] = None
    pickup_address: Optional[str] = None
    dropoff_address: Optional[str] = None
    route_id: Optional[int] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class StudentResponse(StudentBase):
    """
    学生响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
