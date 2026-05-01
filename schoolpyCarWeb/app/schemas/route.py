"""
路线Pydantic模式定义
"""
from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel


class RouteBase(BaseModel):
    """
    路线基础模式
    """
    route_code: str
    route_name: str
    school_id: int
    start_address: Optional[str] = None
    end_address: Optional[str] = None
    main_route: Optional[str] = None
    main_route_stops: Optional[str] = None
    emergency_route: Optional[str] = None
    emergency_route_stops: Optional[str] = None
    backup_route: Optional[str] = None
    backup_route_stops: Optional[str] = None
    departure_time: Optional[time] = None
    estimated_duration: Optional[int] = None
    return_departure_time: Optional[time] = None
    return_estimated_duration: Optional[int] = None
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    status: str = "active"
    remarks: Optional[str] = None


class RouteCreate(RouteBase):
    """
    路线创建模式
    """
    pass


class RouteUpdate(BaseModel):
    """
    路线更新模式
    """
    route_code: Optional[str] = None
    route_name: Optional[str] = None
    school_id: Optional[int] = None
    start_address: Optional[str] = None
    end_address: Optional[str] = None
    main_route: Optional[str] = None
    main_route_stops: Optional[str] = None
    emergency_route: Optional[str] = None
    emergency_route_stops: Optional[str] = None
    backup_route: Optional[str] = None
    backup_route_stops: Optional[str] = None
    departure_time: Optional[time] = None
    estimated_duration: Optional[int] = None
    return_departure_time: Optional[time] = None
    return_estimated_duration: Optional[int] = None
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class RouteResponse(RouteBase):
    """
    路线响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
