from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class DriverBehaviorType(str, enum.Enum):
    FATIGUE = "fatigue"
    PHONE_CALL = "phone_call"
    ABSENT = "absent"
    SMOKING = "smoking"
    DRINKING = "drinking"
    DISTRACTED = "distracted"


class BehaviorSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DriverBehavior(Base):
    __tablename__ = "driver_behaviors"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    behavior_type = Column(Enum(DriverBehaviorType), nullable=False)
    severity = Column(Enum(BehaviorSeverity), default=BehaviorSeverity.MEDIUM)
    confidence = Column(Integer, default=80)
    location_lat = Column(String(30))
    location_lng = Column(String(30))
    image_path = Column(String(255))
    video_clip_path = Column(String(255))
    description = Column(Text)
    is_handled = Column(Integer, default=0)
    handled_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    handled_at = Column(DateTime(timezone=True))
    handle_remark = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bus = relationship("Bus", backref="driver_behaviors")
    driver = relationship("User", foreign_keys=[driver_id], backref="driver_behavior_records")
    handler = relationship("User", foreign_keys=[handled_by], backref="handled_driver_behaviors")

    def to_dict(self):
        return {
            "id": self.id,
            "bus_id": self.bus_id,
            "driver_id": self.driver_id,
            "behavior_type": self.behavior_type.value if self.behavior_type else None,
            "severity": self.severity.value if self.severity else None,
            "confidence": self.confidence,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "image_path": self.image_path,
            "video_clip_path": self.video_clip_path,
            "description": self.description,
            "is_handled": self.is_handled,
            "handled_by": self.handled_by,
            "handled_at": self.handled_at.isoformat() if self.handled_at else None,
            "handle_remark": self.handle_remark,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
