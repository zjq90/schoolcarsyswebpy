from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class DutyStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    CHANGED = "changed"


class DutyChangeType(str, enum.Enum):
    TEMPORARY_SHIFT = "temporary_shift"
    EMERGENCY_DETOUR = "emergency_detour"
    BUS_SWAP = "bus_swap"
    DRIVER_SWAP = "driver_swap"


class Duty(Base):
    __tablename__ = "duties"

    id = Column(Integer, primary_key=True, index=True)
    duty_date = Column(Date, nullable=False)
    shift_type = Column(String(20), default="morning")
    driver_id = Column(Integer, ForeignKey("users.id"))
    bus_id = Column(Integer, ForeignKey("buses.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    status = Column(Enum(DutyStatus), default=DutyStatus.SCHEDULED)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    assigned_by = Column(Integer, ForeignKey("users.id"))
    is_changed = Column(Integer, default=0)
    change_type = Column(Enum(DutyChangeType), nullable=True)
    change_reason = Column(Text)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    changed_at = Column(DateTime(timezone=True))
    original_driver_id = Column(Integer, nullable=True)
    original_bus_id = Column(Integer, nullable=True)
    original_route_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    driver = relationship("User", foreign_keys=[driver_id], backref="driver_duties")
    bus = relationship("Bus", backref="bus_duties")
    route = relationship("Route", backref="route_duties")
    assigner = relationship("User", foreign_keys=[assigned_by], backref="assigned_duties")
    changer = relationship("User", foreign_keys=[changed_by], backref="changed_duties")

    def to_dict(self):
        return {
            "id": self.id,
            "duty_date": self.duty_date.isoformat() if self.duty_date else None,
            "shift_type": self.shift_type,
            "driver_id": self.driver_id,
            "bus_id": self.bus_id,
            "route_id": self.route_id,
            "status": self.status.value if self.status else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "assigned_by": self.assigned_by,
            "is_changed": self.is_changed,
            "change_type": self.change_type.value if self.change_type else None,
            "change_reason": self.change_reason,
            "changed_by": self.changed_by,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
            "original_driver_id": self.original_driver_id,
            "original_bus_id": self.original_bus_id,
            "original_route_id": self.original_route_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
