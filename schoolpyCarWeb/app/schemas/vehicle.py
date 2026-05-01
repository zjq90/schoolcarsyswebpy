"""
车辆Pydantic模式定义
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class VehicleBase(BaseModel):
    """
    车辆基础模式
    """
    vehicle_code: str
    license_plate: str
    vehicle_model: Optional[str] = None
    seat_count: int
    purchase_date: Optional[date] = None
    school_id: int
    campus: Optional[str] = None
    driver_id: Optional[int] = None
    status: str = "available"
    insurance_expire: Optional[date] = None
    inspection_expire: Optional[date] = None
    remarks: Optional[str] = None


class VehicleCreate(VehicleBase):
    """
    车辆创建模式
    """
    pass


class VehicleUpdate(BaseModel):
    """
    车辆更新模式
    """
    vehicle_code: Optional[str] = None
    license_plate: Optional[str] = None
    vehicle_model: Optional[str] = None
    seat_count: Optional[int] = None
    purchase_date: Optional[date] = None
    school_id: Optional[int] = None
    campus: Optional[str] = None
    driver_id: Optional[int] = None
    status: Optional[str] = None
    insurance_expire: Optional[date] = None
    inspection_expire: Optional[date] = None
    remarks: Optional[str] = None


class VehicleResponse(VehicleBase):
    """
    车辆响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
