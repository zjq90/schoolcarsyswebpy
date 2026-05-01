"""
调度Pydantic模式定义
"""
from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel


class DispatchBase(BaseModel):
    """
    调度基础模式
    """
    dispatch_code: str
    dispatch_type: str = "temporary"
    from_school_id: int
    from_vehicle_id: int
    from_driver_id: Optional[int] = None
    to_school_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    departure_time: Optional[time] = None
    return_time: Optional[time] = None
    reason: Optional[str] = None
    dispatch_route: Optional[str] = None
    dispatcher_id: int
    status: str = "pending"
    remarks: Optional[str] = None


class DispatchCreate(DispatchBase):
    """
    调度创建模式
    """
    pass


class DispatchUpdate(BaseModel):
    """
    调度更新模式
    """
    dispatch_code: Optional[str] = None
    dispatch_type: Optional[str] = None
    from_school_id: Optional[int] = None
    from_vehicle_id: Optional[int] = None
    from_driver_id: Optional[int] = None
    to_school_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    departure_time: Optional[time] = None
    return_time: Optional[time] = None
    reason: Optional[str] = None
    dispatch_route: Optional[str] = None
    dispatcher_id: Optional[int] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class DispatchResponse(DispatchBase):
    """
    调度响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
