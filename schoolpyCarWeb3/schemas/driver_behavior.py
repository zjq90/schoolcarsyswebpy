from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DriverBehaviorType(str, Enum):
    FATIGUE = "fatigue"
    PHONE_CALL = "phone_call"
    ABSENT = "absent"
    SMOKING = "smoking"
    DRINKING = "drinking"
    DISTRACTED = "distracted"


class BehaviorSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DriverBehaviorBase(BaseModel):
    bus_id: Optional[int] = None
    driver_id: Optional[int] = None
    behavior_type: DriverBehaviorType
    severity: BehaviorSeverity = BehaviorSeverity.MEDIUM
    confidence: int = Field(default=80, ge=0, le=100)
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    image_path: Optional[str] = None
    video_clip_path: Optional[str] = None
    description: Optional[str] = None


class DriverBehaviorCreate(DriverBehaviorBase):
    pass


class DriverBehaviorUpdate(BaseModel):
    is_handled: Optional[int] = None
    handled_by: Optional[int] = None
    handle_remark: Optional[str] = None


class DriverBehaviorResponse(DriverBehaviorBase):
    id: int
    is_handled: int
    handled_by: Optional[int] = None
    handled_at: Optional[datetime] = None
    handle_remark: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
