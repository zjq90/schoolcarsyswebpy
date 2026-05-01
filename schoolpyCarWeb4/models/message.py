"""
校车管理系统 - 消息推送和状态数据模型
定义学生、消息推送和校车状态相关的数据结构
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class StudentBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="学生姓名，1-50个字符"
    )
    student_no: Optional[str] = Field(
        None, 
        max_length=30, 
        description="学号，最多30个字符"
    )
    class_name: Optional[str] = Field(
        None, 
        max_length=30, 
        description="班级名称，最多30个字符"
    )
    card_id: Optional[str] = Field(
        None, 
        max_length=30, 
        description="卡号，最多30个字符"
    )
    parent_phone: Optional[str] = Field(
        None, 
        max_length=20, 
        description="家长联系电话"
    )
    status: str = Field(
        default="active", 
        max_length=20, 
        description="状态：active/inactive"
    )

    @field_validator('parent_phone')
    @classmethod
    def validate_parent_phone(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('家长手机号格式不正确，应为11位数字且以1开头')
        return v

    @field_validator('student_no')
    @classmethod
    def validate_student_no(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if len(v) > 30:
            raise ValueError('学号长度不能超过30个字符')
        return v

    @field_validator('card_id')
    @classmethod
    def validate_card_id(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if len(v) > 30:
            raise ValueError('卡号长度不能超过30个字符')
        return v


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=50
    )
    student_no: Optional[str] = Field(
        None, 
        max_length=30
    )
    class_name: Optional[str] = Field(
        None, 
        max_length=30
    )
    card_id: Optional[str] = Field(
        None, 
        max_length=30
    )
    parent_phone: Optional[str] = Field(
        None, 
        max_length=20
    )
    status: Optional[str] = Field(
        None, 
        max_length=20
    )

    @field_validator('parent_phone')
    @classmethod
    def validate_parent_phone(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('家长手机号格式不正确，应为11位数字且以1开头')
        return v


class StudentResponse(StudentBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessagePushBase(BaseModel):
    student_id: Optional[int] = Field(
        None, 
        gt=0, 
        description="学生ID，必须大于0"
    )
    message_type: str = Field(
        ..., 
        min_length=1, 
        max_length=30, 
        description="消息类型"
    )
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="消息内容"
    )
    push_time: Optional[datetime] = None
    status: str = Field(
        default="sent", 
        max_length=20
    )
    receiver_phone: Optional[str] = Field(
        None, 
        max_length=20
    )

    @field_validator('receiver_phone')
    @classmethod
    def validate_receiver_phone(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('接收方手机号格式不正确，应为11位数字且以1开头')
        return v


class MessagePushCreate(MessagePushBase):
    pass


class MessagePushResponse(MessagePushBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessagePushWithStudent(MessagePushResponse):
    student_name: Optional[str] = None


class BusStatusBase(BaseModel):
    vehicle_id: int = Field(
        ..., 
        gt=0, 
        description="车辆ID，必须大于0"
    )
    driver_id: Optional[int] = Field(
        None, 
        gt=0, 
        description="司机ID，必须大于0"
    )
    status_type: str = Field(
        ..., 
        min_length=1, 
        max_length=30, 
        description="状态类型"
    )
    status_value: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="状态值"
    )
    location: Optional[str] = Field(
        None, 
        max_length=100, 
        description="位置信息"
    )
    record_time: Optional[datetime] = None
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="描述信息"
    )


class BusStatusCreate(BusStatusBase):
    pass


class BusStatusResponse(BusStatusBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 带关联信息的校车状态响应
class BusStatusWithDetails(BusStatusResponse):
    plate_number: Optional[str] = None
    driver_name: Optional[str] = None


class BusDepartureRequest(BaseModel):
    vehicle_id: int = Field(..., gt=0, description="车辆ID，必须大于0")
    driver_id: Optional[int] = Field(None, gt=0, description="司机ID（可选）")
    location: str = Field(default="学校", max_length=100, description="发车位置")


class BusArrivalRequest(BaseModel):
    vehicle_id: int = Field(..., gt=0, description="车辆ID，必须大于0")
    driver_id: Optional[int] = Field(None, gt=0, description="司机ID（可选）")
    location: str = Field(default="学校", max_length=100, description="到站位置")


class BusAbnormalRequest(BaseModel):
    vehicle_id: int = Field(..., gt=0, description="车辆ID，必须大于0")
    abnormal_type: str = Field(..., min_length=1, max_length=50, description="异常类型")
    driver_id: Optional[int] = Field(None, gt=0, description="司机ID（可选）")
    location: Optional[str] = Field(None, max_length=100, description="位置")
    description: Optional[str] = Field(None, max_length=500, description="详细描述")
