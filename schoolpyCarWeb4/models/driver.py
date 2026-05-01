"""
校车管理系统 - 司机相关数据模型
定义司机和评分相关的数据结构
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class DriverBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="司机姓名，1-50个字符"
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20, 
        description="联系电话"
    )
    license_no: Optional[str] = Field(
        None, 
        max_length=20, 
        description="驾驶证号"
    )
    hire_date: Optional[date] = Field(
        None, 
        description="入职日期"
    )
    status: str = Field(
        default="active", 
        max_length=20, 
        description="状态：active/inactive"
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式不正确，应为11位数字且以1开头')
        return v

    @field_validator('license_no')
    @classmethod
    def validate_license_no(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip().upper()
        if not v:
            return None
        if not re.match(r'^[0-9]{15}$|^[0-9]{17}[0-9Xx]$', v):
            raise ValueError('驾驶证号格式不正确，应为15位或18位数字（最后一位可为X）')
        return v


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=50
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20
    )
    license_no: Optional[str] = Field(
        None, 
        max_length=20
    )
    hire_date: Optional[date] = None
    status: Optional[str] = Field(
        None, 
        max_length=20
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip()
        if not v:
            return None
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式不正确，应为11位数字且以1开头')
        return v

    @field_validator('license_no')
    @classmethod
    def validate_license_no(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip().upper()
        if not v:
            return None
        if not re.match(r'^[0-9]{15}$|^[0-9]{17}[0-9Xx]$', v):
            raise ValueError('驾驶证号格式不正确，应为15位或18位数字（最后一位可为X）')
        return v


class DriverResponse(DriverBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DriverScoreBase(BaseModel):
    driver_id: int = Field(
        ..., 
        gt=0, 
        description="司机ID，必须大于0"
    )
    score_date: date = Field(
        ..., 
        description="评分日期"
    )
    violation_count: int = Field(
        default=0, 
        ge=0, 
        description="违章次数，不能为负数"
    )
    complaint_count: int = Field(
        default=0, 
        ge=0, 
        description="投诉次数，不能为负数"
    )
    safe_driving_hours: float = Field(
        default=0.0, 
        ge=0.0, 
        le=24.0, 
        description="安全驾驶时长，0-24小时"
    )
    credit_score: float = Field(
        default=100.0, 
        ge=0.0, 
        le=100.0, 
        description="信用分，0-100分"
    )
    notes: Optional[str] = Field(
        None, 
        max_length=500, 
        description="备注，最多500字符"
    )


class DriverScoreCreate(DriverScoreBase):
    pass


class DriverScoreResponse(DriverScoreBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DriverScoreWithDriver(DriverScoreResponse):
    driver_name: Optional[str] = None
