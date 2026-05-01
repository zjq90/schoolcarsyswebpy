from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class BusStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class BusBase(BaseModel):
    plate_number: str = Field(..., min_length=5, max_length=20)
    bus_model: Optional[str] = None
    capacity: int = Field(default=40, ge=1, le=100)
    status: BusStatus = BusStatus.IDLE


class BusCreate(BusBase):
    pass


class BusUpdate(BaseModel):
    bus_model: Optional[str] = None
    capacity: Optional[int] = Field(default=None, ge=1, le=100)
    status: Optional[BusStatus] = None
    current_driver_id: Optional[int] = None
    gps_latitude: Optional[str] = None
    gps_longitude: Optional[str] = None


class BusResponse(BusBase):
    id: int
    current_driver_id: Optional[int] = None
    gps_latitude: Optional[str] = None
    gps_longitude: Optional[str] = None
    last_update: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
