from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum


class TrafficCondition(str, enum.Enum):
    SMOOTH = "smooth"
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    JAM = "jam"


class TrafficData(Base):
    __tablename__ = "traffic_data"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    location_name = Column(String(100))
    location_lat = Column(String(30))
    location_lng = Column(String(30))
    condition = Column(Enum(TrafficCondition), default=TrafficCondition.SMOOTH)
    speed_kmh = Column(Integer, default=60)
    delay_minutes = Column(Integer, default=0)
    distance_km = Column(Float, default=0)
    data_source = Column(String(50), default="system")
    description = Column(Text)
    is_sent_to_bus = Column(Integer, default=0)
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    route = relationship("Route", backref="traffic_data")

    def to_dict(self):
        return {
            "id": self.id,
            "route_id": self.route_id,
            "location_name": self.location_name,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "condition": self.condition.value if self.condition else None,
            "speed_kmh": self.speed_kmh,
            "delay_minutes": self.delay_minutes,
            "distance_km": self.distance_km,
            "data_source": self.data_source,
            "description": self.description,
            "is_sent_to_bus": self.is_sent_to_bus,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
