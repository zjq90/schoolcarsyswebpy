from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class BusStatus(str, enum.Enum):
    IDLE = "idle"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, index=True, nullable=False)
    bus_model = Column(String(50))
    capacity = Column(Integer, default=40)
    status = Column(Enum(BusStatus), default=BusStatus.IDLE)
    current_driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    gps_latitude = Column(String(30))
    gps_longitude = Column(String(30))
    last_update = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    driver = relationship("User", backref="assigned_bus")

    def to_dict(self):
        return {
            "id": self.id,
            "plate_number": self.plate_number,
            "bus_model": self.bus_model,
            "capacity": self.capacity,
            "status": self.status.value if self.status else None,
            "current_driver_id": self.current_driver_id,
            "gps_latitude": self.gps_latitude,
            "gps_longitude": self.gps_longitude,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
