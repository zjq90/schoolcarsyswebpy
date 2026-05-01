from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class DutyStatus(str, Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    CHANGED = "changed"


class DutyChangeType(str, Enum):
    TEMPORARY_SHIFT = "temporary_shift"
    EMERGENCY_DETOUR = "emergency_detour"
    BUS_SWAP = "bus_swap"
    DRIVER_SWAP = "driver_swap"


class DutyBase(BaseModel):
    duty_date: date
    shift_type: str = "morning"
    driver_id: Optional[int] = None
    bus_id: Optional[int] = None
    route_id: Optional[int] = None


class DutyCreate(DutyBase):
    assigned_by: Optional[int] = None
    start_time: Optional[datetime] = None


class DutyUpdate(BaseModel):
    status: Optional[DutyStatus] = None
    driver_id: Optional[int] = None
    bus_id: Optional[int] = None
    route_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class DutyChangeRequest(BaseModel):
    change_type: DutyChangeType
    change_reason: str
    new_driver_id: Optional[int] = None
    new_bus_id: Optional[int] = None
    new_route_id: Optional[int] = None


class DutyResponse(DutyBase):
    id: int
    status: DutyStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    assigned_by: Optional[int] = None
    is_changed: int
    change_type: Optional[DutyChangeType] = None
    change_reason: Optional[str] = None
    changed_by: Optional[int] = None
    changed_at: Optional[datetime] = None
    original_driver_id: Optional[int] = None
    original_bus_id: Optional[int] = None
    original_route_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
