from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TrafficCondition(str, Enum):
    SMOOTH = "smooth"
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    JAM = "jam"


class TrafficDataBase(BaseModel):
    route_id: Optional[int] = None
    location_name: Optional[str] = None
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    condition: TrafficCondition = TrafficCondition.SMOOTH
    speed_kmh: int = Field(default=60, ge=0)
    delay_minutes: int = Field(default=0, ge=0)
    distance_km: float = Field(default=0.0, ge=0)
    data_source: str = "system"
    description: Optional[str] = None


class TrafficDataCreate(TrafficDataBase):
    pass


class TrafficDataUpdate(BaseModel):
    condition: Optional[TrafficCondition] = None
    speed_kmh: Optional[int] = None
    delay_minutes: Optional[int] = None
    is_sent_to_bus: Optional[int] = None


class TrafficDataResponse(TrafficDataBase):
    id: int
    is_sent_to_bus: int
    sent_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
