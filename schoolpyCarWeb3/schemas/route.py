from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class RouteStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RouteBase(BaseModel):
    route_name: str = Field(..., min_length=2, max_length=100)
    route_code: Optional[str] = None
    start_point: str = Field(..., min_length=2, max_length=100)
    end_point: str = Field(..., min_length=2, max_length=100)
    waypoints: Optional[str] = None
    distance_km: int = Field(default=0, ge=0)
    estimated_duration_min: int = Field(default=30, ge=1)


class RouteCreate(RouteBase):
    bus_id: Optional[int] = None
    driver_id: Optional[int] = None
    scheduled_departure: Optional[datetime] = None


class RouteUpdate(BaseModel):
    route_name: Optional[str] = None
    start_point: Optional[str] = None
    end_point: Optional[str] = None
    waypoints: Optional[str] = None
    distance_km: Optional[int] = None
    estimated_duration_min: Optional[int] = None
    bus_id: Optional[int] = None
    driver_id: Optional[int] = None
    status: Optional[RouteStatus] = None
    scheduled_departure: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None


class RouteResponse(RouteBase):
    id: int
    bus_id: Optional[int] = None
    driver_id: Optional[int] = None
    status: RouteStatus
    scheduled_departure: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
