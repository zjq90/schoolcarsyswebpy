"""
校车管理系统 - 运维记录数据模型
定义车辆和运维记录相关的数据结构
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class VehicleBase(BaseModel):
    plate_number: str = Field(
        ..., 
        min_length=1, 
        max_length=10, 
        description="车牌号，如：京A12345"
    )
    vehicle_type: Optional[str] = Field(
        None, 
        max_length=30, 
        description="车辆类型，最多30个字符"
    )
    capacity: Optional[int] = Field(
        None, 
        gt=0, 
        le=100, 
        description="核载人数，1-100人"
    )
    purchase_date: Optional[date] = Field(
        None, 
        description="购买日期"
    )
    status: str = Field(
        default="active", 
        max_length=20, 
        description="状态：active/inactive"
    )

    @field_validator('plate_number')
    @classmethod
    def validate_plate_number(cls, v):
        if v is None or v == '':
            raise ValueError('车牌号不能为空')
        v = str(v).strip().upper()
        if not v:
            raise ValueError('车牌号不能为空')
        
        china_plate_pattern = r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Z][A-Z0-9]{5,6}$'
        if not re.match(china_plate_pattern, v):
            raise ValueError(
                '车牌号格式不正确，应为：省份简称+字母+5-6位数字/字母，如：京A12345'
            )
        return v


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=10
    )
    vehicle_type: Optional[str] = Field(
        None, 
        max_length=30
    )
    capacity: Optional[int] = Field(
        None, 
        gt=0, 
        le=100
    )
    purchase_date: Optional[date] = None
    status: Optional[str] = Field(
        None, 
        max_length=20
    )

    @field_validator('plate_number')
    @classmethod
    def validate_plate_number(cls, v):
        if v is None or v == '':
            return None
        v = str(v).strip().upper()
        if not v:
            return None
        
        china_plate_pattern = r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Z][A-Z0-9]{5,6}$'
        if not re.match(china_plate_pattern, v):
            raise ValueError(
                '车牌号格式不正确，应为：省份简称+字母+5-6位数字/字母，如：京A12345'
            )
        return v


class VehicleResponse(VehicleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaintenanceBase(BaseModel):
    record_type: str = Field(
        ..., 
        min_length=1, 
        max_length=20, 
        description="记录类型：年检/保险/维修/油耗"
    )
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
    record_date: date = Field(
        ..., 
        description="记录日期"
    )
    amount: float = Field(
        default=0.0, 
        ge=0.0, 
        le=999999.99, 
        description="金额，不能为负数"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="描述信息，最多500字符"
    )
    status: str = Field(
        default="completed", 
        max_length=20, 
        description="状态"
    )


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    record_type: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=20
    )
    vehicle_id: Optional[int] = Field(
        None, 
        gt=0
    )
    driver_id: Optional[int] = Field(
        None, 
        gt=0
    )
    record_date: Optional[date] = None
    amount: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=999999.99
    )
    description: Optional[str] = Field(
        None, 
        max_length=500
    )
    status: Optional[str] = Field(
        None, 
        max_length=20
    )


class MaintenanceResponse(MaintenanceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaintenanceWithDetails(MaintenanceResponse):
    plate_number: Optional[str] = None
    driver_name: Optional[str] = None
