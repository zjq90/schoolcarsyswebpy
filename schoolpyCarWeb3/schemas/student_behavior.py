from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class StudentBehaviorType(str, Enum):
    STANDING = "standing"
    WANDERING = "wandering"
    LEFT_BEHIND = "left_behind"
    NO_SEATBELT = "no_seatbelt"
    PLAYING = "playing"
    FIGHTING = "fighting"
    SHOUTING = "shouting"


class StudentBehaviorBase(BaseModel):
    bus_id: Optional[int] = None
    behavior_type: StudentBehaviorType
    confidence: int = Field(default=80, ge=0, le=100)
    student_count: int = Field(default=1, ge=1)
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    image_path: Optional[str] = None
    video_clip_path: Optional[str] = None
    description: Optional[str] = None


class StudentBehaviorCreate(StudentBehaviorBase):
    pass


class StudentBehaviorUpdate(BaseModel):
    is_handled: Optional[int] = None
    handled_by: Optional[int] = None
    handle_remark: Optional[str] = None


class StudentBehaviorResponse(StudentBehaviorBase):
    id: int
    is_handled: int
    handled_by: Optional[int] = None
    handled_at: Optional[datetime] = None
    handle_remark: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
