from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class RouteStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String(100), nullable=False)
    route_code = Column(String(50), unique=True, index=True)
    start_point = Column(String(100), nullable=False)
    end_point = Column(String(100), nullable=False)
    waypoints = Column(Text)
    distance_km = Column(Integer, default=0)
    estimated_duration_min = Column(Integer, default=30)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(RouteStatus), default=RouteStatus.PLANNED)
    scheduled_departure = Column(DateTime(timezone=True))
    actual_departure = Column(DateTime(timezone=True))
    actual_arrival = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    bus = relationship("Bus", backref="routes")
    driver = relationship("User", backref="routes")

    def to_dict(self):
        return {
            "id": self.id,
            "route_name": self.route_name,
            "route_code": self.route_code,
            "start_point": self.start_point,
            "end_point": self.end_point,
            "waypoints": self.waypoints,
            "distance_km": self.distance_km,
            "estimated_duration_min": self.estimated_duration_min,
            "bus_id": self.bus_id,
            "driver_id": self.driver_id,
            "status": self.status.value if self.status else None,
            "scheduled_departure": self.scheduled_departure.isoformat() if self.scheduled_departure else None,
            "actual_departure": self.actual_departure.isoformat() if self.actual_departure else None,
            "actual_arrival": self.actual_arrival.isoformat() if self.actual_arrival else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
