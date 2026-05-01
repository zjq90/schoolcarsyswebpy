"""
司机Pydantic模式定义
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class DriverBase(BaseModel):
    """
    司机基础模式
    """
    driver_code: str
    real_name: str
    id_card: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None
    driving_years: int = 0
    health_status: str = "良好"
    license_number: Optional[str] = None
    license_type: Optional[str] = None
    license_expire: Optional[date] = None
    qualification_cert: Optional[str] = None
    qualification_expire: Optional[date] = None
    no_crime_record: bool = True
    school_id: int
    status: str = "available"
    remarks: Optional[str] = None


class DriverCreate(DriverBase):
    """
    司机创建模式
    """
    pass


class DriverUpdate(BaseModel):
    """
    司机更新模式
    """
    driver_code: Optional[str] = None
    real_name: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None
    driving_years: Optional[int] = None
    health_status: Optional[str] = None
    license_number: Optional[str] = None
    license_type: Optional[str] = None
    license_expire: Optional[date] = None
    qualification_cert: Optional[str] = None
    qualification_expire: Optional[date] = None
    no_crime_record: Optional[bool] = None
    school_id: Optional[int] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class DriverResponse(DriverBase):
    """
    司机响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
