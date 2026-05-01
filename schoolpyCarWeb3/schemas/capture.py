from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CaptureType(str, Enum):
    DRIVER_BEHAVIOR = "driver_behavior"
    STUDENT_BEHAVIOR = "student_behavior"
    EMERGENCY = "emergency"
    ROAD_CONDITION = "road_condition"
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class CaptureBase(BaseModel):
    bus_id: Optional[int] = None
    capture_type: CaptureType
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    description: Optional[str] = None
    related_behavior_id: Optional[int] = None


class CaptureCreate(CaptureBase):
    pass


class CaptureUpdate(BaseModel):
    is_uploaded: Optional[int] = None


class CaptureResponse(CaptureBase):
    id: int
    is_uploaded: int
    uploaded_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
