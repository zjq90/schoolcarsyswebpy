from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class CaptureType(str, enum.Enum):
    DRIVER_BEHAVIOR = "driver_behavior"
    STUDENT_BEHAVIOR = "student_behavior"
    EMERGENCY = "emergency"
    ROAD_CONDITION = "road_condition"
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class Capture(Base):
    __tablename__ = "captures"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    capture_type = Column(Enum(CaptureType), nullable=False)
    image_path = Column(String(255))
    video_path = Column(String(255))
    thumbnail_path = Column(String(255))
    location_lat = Column(String(30))
    location_lng = Column(String(30))
    description = Column(Text)
    related_behavior_id = Column(Integer, nullable=True)
    is_uploaded = Column(Integer, default=0)
    uploaded_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bus = relationship("Bus", backref="captures")

    def to_dict(self):
        return {
            "id": self.id,
            "bus_id": self.bus_id,
            "capture_type": self.capture_type.value if self.capture_type else None,
            "image_path": self.image_path,
            "video_path": self.video_path,
            "thumbnail_path": self.thumbnail_path,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "description": self.description,
            "related_behavior_id": self.related_behavior_id,
            "is_uploaded": self.is_uploaded,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
