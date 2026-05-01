"""
校车管理系统 - FastAPI主应用
"""
import os
import asyncio
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from enum import Enum

from fastapi import FastAPI, Depends, HTTPException, Request, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, desc, func, and_
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
from sqlalchemy.exc import IntegrityError


# ==================== 配置 ====================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./schoolbus.db")
REFRESH_INTERVAL = 3  # 秒
TRAJETORY_RETENTION_DAYS = 90  # 3个月
GEOFENCE_THRESHOLD = 3  # 越界阈值

# ==================== 数据库模型 ====================
Base = declarative_base()


class VehicleStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    RUNNING = "running"
    IDLE = "idle"
    MAINTENANCE = "maintenance"


class GeofenceType(str, Enum):
    SCHOOL = "school"
    DANGER = "danger"
    HOME = "home"
    OTHER = "other"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    IGNORED = "ignored"


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False, index=True)
    driver_name = Column(String(50))
    driver_phone = Column(String(20))
    driver_license = Column(String(50))
    vehicle_model = Column(String(100))
    vehicle_type = Column(String(50))
    school = Column(String(100))
    capacity = Column(Integer, default=45)
    status = Column(String(20), default=VehicleStatus.IDLE)
    device_id = Column(String(50), unique=True, index=True)
    
    current_lat = Column(Float)
    current_lng = Column(Float)
    current_speed = Column(Float, default=0)
    current_direction = Column(Integer, default=0)
    
    last_online_time = Column(DateTime)
    last_location_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    trajectories = relationship("Trajectory", back_populates="vehicle")
    alerts = relationship("Alert", back_populates="vehicle")


class Trajectory(Base):
    __tablename__ = "trajectories"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    plate_number = Column(String(20))
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)
    speed = Column(Float, default=0)
    direction = Column(Integer, default=0)
    
    satellites = Column(Integer, default=0)
    gps_accuracy = Column(Float, default=5.0)
    data_source = Column(String(20), default="gps")
    
    location_time = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    vehicle = relationship("Vehicle", back_populates="trajectories")


class Geofence(Base):
    __tablename__ = "geofences"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    fence_type = Column(String(20), default=GeofenceType.OTHER)
    description = Column(String(500))
    
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    radius = Column(Float, default=500)
    
    threshold = Column(Integer, default=GEOFENCE_THRESHOLD)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    plate_number = Column(String(20))
    
    alert_type = Column(String(50), default="geofence_violation")
    severity = Column(String(20), default="medium")
    
    geofence_id = Column(Integer, ForeignKey("geofences.id"))
    fence_name = Column(String(100))
    fence_type = Column(String(20))
    
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    direction = Column(Integer)
    
    violation_count = Column(Integer, default=1)
    message = Column(String(500))
    status = Column(String(20), default=AlertStatus.ACTIVE)
    
    resolved_at = Column(DateTime)
    resolved_by = Column(String(50))
    resolve_note = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    vehicle = relationship("Vehicle", back_populates="alerts")


class AlertNotification(Base):
    __tablename__ = "alert_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False, index=True)
    
    notify_type = Column(String(20))
    notify_target = Column(String(100))
    notify_content = Column(String(500))
    notify_status = Column(String(20), default="pending")
    
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


# ==================== Pydantic模型 ====================
class GPSData(BaseModel):
    device_id: str
    vehicle_id: int
    latitude: float
    longitude: float
    speed: float = 0.0
    direction: int = 0
    altitude: float = 0.0
    satellites: int = 0
    gps_accuracy: float = 5.0
    location_time: str
    data_source: str = "gps"


class VehicleCreate(BaseModel):
    plate_number: str
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    driver_license: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_type: Optional[str] = None
    school: Optional[str] = None
    capacity: int = 45
    status: str = "idle"


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    driver_license: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_type: Optional[str] = None
    school: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class GeofenceCreate(BaseModel):
    name: str
    fence_type: str = "other"
    description: Optional[str] = None
    center_lat: float
    center_lng: float
    radius: float = 500
    threshold: int = 3
    is_active: bool = True


class GeofenceUpdate(BaseModel):
    name: Optional[str] = None
    fence_type: Optional[str] = None
    description: Optional[str] = None
    center_lat: Optional[float] = None
    center_lng: Optional[float] = None
    radius: Optional[float] = None
    threshold: Optional[int] = None
    is_active: Optional[bool] = None


# ==================== 数据库配置 ====================
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 工具函数 ====================
def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    import math
    R = 6371000
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lng / 2) * math.sin(d_lng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def is_point_in_fence(lat: float, lng: float, fence: Geofence) -> bool:
    distance = calculate_distance(lat, lng, fence.center_lat, fence.center_lng)
    return distance <= fence.radius


def clean_old_trajectories(db: Session):
    cutoff_date = datetime.now() - timedelta(days=TRAJETORY_RETENTION_DAYS)
    deleted = db.query(Trajectory).filter(Trajectory.location_time < cutoff_date).delete()
    db.commit()
    return deleted


# ==================== 生命周期管理 ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建")
    yield


# ==================== FastAPI应用 ====================
app = FastAPI(
    title="校车管理系统API",
    description="GPS/北斗双模定位 + 4G/5G数据回传的校车管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# 静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ==================== 页面路由 ====================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request):
    return templates.TemplateResponse("vehicles.html", {"request": request})


@app.get("/location", response_class=HTMLResponse)
async def location_page(request: Request):
    return templates.TemplateResponse("location.html", {"request": request})


@app.get("/trajectory", response_class=HTMLResponse)
async def trajectory_page(request: Request):
    return templates.TemplateResponse("trajectory.html", {"request": request})


@app.get("/geofence", response_class=HTMLResponse)
async def geofence_page(request: Request):
    return templates.TemplateResponse("geofence.html", {"request": request})


@app.get("/alerts", response_class=HTMLResponse)
async def alerts_page(request: Request):
    return templates.TemplateResponse("alerts.html", {"request": request})


# ==================== API路由 ====================

# --- 仪表盘统计 ---
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    total_vehicles = db.query(Vehicle).count()
    online_vehicles = db.query(Vehicle).filter(Vehicle.status == "online").count()
    running_vehicles = db.query(Vehicle).filter(Vehicle.status == "running").count()
    
    total_geofences = db.query(Geofence).count()
    school_fences = db.query(Geofence).filter(Geofence.fence_type == "school").count()
    danger_fences = db.query(Geofence).filter(Geofence.fence_type == "danger").count()
    home_fences = db.query(Geofence).filter(Geofence.fence_type == "home").count()
    
    active_alerts = db.query(Alert).filter(Alert.status == "active").count()
    high_alerts = db.query(Alert).filter(Alert.severity == "high", Alert.status == "active").count()
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_alerts = db.query(Alert).filter(Alert.created_at >= today_start).count()
    
    total_tracks = db.query(Trajectory).count()
    today_tracks = db.query(Trajectory).filter(Trajectory.created_at >= today_start).count()
    
    return {
        "vehicle_stats": {
            "total": total_vehicles,
            "online": online_vehicles,
            "running": running_vehicles
        },
        "alert_stats": {
            "active": active_alerts,
            "high": high_alerts,
            "today": today_alerts
        },
        "fence_stats": {
            "total": total_geofences,
            "school": school_fences,
            "danger": danger_fences,
            "home": home_fences
        },
        "trajectory_stats": {
            "total": total_tracks,
            "today": today_tracks,
            "total_distance": 0
        }
    }


# --- 车辆管理 ---
@app.get("/api/vehicles")
async def get_vehicles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    sort_field: str = "id",
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    query = db.query(Vehicle)
    
    if keyword:
        query = query.filter(
            Vehicle.plate_number.contains(keyword) |
            Vehicle.driver_name.contains(keyword) |
            Vehicle.device_id.contains(keyword)
        )
    
    if status:
        query = query.filter(Vehicle.status == status)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Vehicle, sort_field, Vehicle.id)))
    else:
        query = query.order_by(getattr(Vehicle, sort_field, Vehicle.id))
    
    vehicles = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "data": [
            {
                "id": v.id,
                "plate_number": v.plate_number,
                "driver_name": v.driver_name,
                "driver_phone": v.driver_phone,
                "driver_license": v.driver_license,
                "vehicle_model": v.vehicle_model,
                "vehicle_type": v.vehicle_type,
                "school": v.school,
                "capacity": v.capacity,
                "status": v.status,
                "device_id": v.device_id,
                "current_lat": v.current_lat,
                "current_lng": v.current_lng,
                "current_speed": v.current_speed,
                "current_direction": v.current_direction,
                "last_online_time": v.last_online_time,
                "last_location_time": v.last_location_time,
                "created_at": v.created_at,
                "updated_at": v.updated_at
            } for v in vehicles
        ],
        "page_info": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages
        }
    }


@app.get("/api/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    return {
        "id": vehicle.id,
        "plate_number": vehicle.plate_number,
        "driver_name": vehicle.driver_name,
        "driver_phone": vehicle.driver_phone,
        "driver_license": vehicle.driver_license,
        "vehicle_model": vehicle.vehicle_model,
        "vehicle_type": vehicle.vehicle_type,
        "school": vehicle.school,
        "capacity": vehicle.capacity,
        "status": vehicle.status,
        "device_id": vehicle.device_id,
        "current_lat": vehicle.current_lat,
        "current_lng": vehicle.current_lng,
        "current_speed": vehicle.current_speed,
        "current_direction": vehicle.current_direction,
        "last_online_time": vehicle.last_online_time,
        "last_location_time": vehicle.last_location_time,
        "created_at": vehicle.created_at,
        "updated_at": vehicle.updated_at
    }


@app.post("/api/vehicles")
async def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    try:
        new_vehicle = Vehicle(
            plate_number=vehicle.plate_number,
            driver_name=vehicle.driver_name,
            driver_phone=vehicle.driver_phone,
            driver_license=vehicle.driver_license,
            vehicle_model=vehicle.vehicle_model,
            vehicle_type=vehicle.vehicle_type,
            school=vehicle.school,
            capacity=vehicle.capacity,
            status=vehicle.status,
            device_id=f"DEV{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
        return {"message": "创建成功", "id": new_vehicle.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="车牌号已存在")


@app.put("/api/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    update_data = vehicle.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_vehicle, key, value)
    
    db.commit()
    return {"message": "更新成功"}


@app.delete("/api/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "删除成功"}


# --- GPS数据接收 ---
@app.post("/api/gps/upload")
async def upload_gps_data(gps_data: GPSData, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == gps_data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    location_time = datetime.fromisoformat(gps_data.location_time.replace('Z', '+00:00'))
    
    trajectory = Trajectory(
        vehicle_id=vehicle.id,
        plate_number=vehicle.plate_number,
        latitude=gps_data.latitude,
        longitude=gps_data.longitude,
        altitude=gps_data.altitude,
        speed=gps_data.speed,
        direction=gps_data.direction,
        satellites=gps_data.satellites,
        gps_accuracy=gps_data.gps_accuracy,
        data_source=gps_data.data_source,
        location_time=location_time
    )
    db.add(trajectory)
    
    vehicle.current_lat = gps_data.latitude
    vehicle.current_lng = gps_data.longitude
    vehicle.current_speed = gps_data.speed
    vehicle.current_direction = gps_data.direction
    vehicle.last_location_time = location_time
    vehicle.last_online_time = datetime.now()
    vehicle.status = "running" if gps_data.speed > 0 else "online"
    
    active_fences = db.query(Geofence).filter(Geofence.is_active == True).all()
    for fence in active_fences:
        is_inside = is_point_in_fence(gps_data.latitude, gps_data.longitude, fence)
        
        if not is_inside:
            recent_alerts = db.query(Alert).filter(
                Alert.vehicle_id == vehicle.id,
                Alert.geofence_id == fence.id,
                Alert.status == "active"
            ).first()
            
            if not recent_alerts:
                day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                today_violations = db.query(Alert).filter(
                    Alert.vehicle_id == vehicle.id,
                    Alert.geofence_id == fence.id,
                    Alert.created_at >= day_start
                ).count()
                
                new_count = today_violations + 1
                
                if new_count >= fence.threshold:
                    severity = "high" if fence.fence_type == "danger" else "medium"
                    alert = Alert(
                        vehicle_id=vehicle.id,
                        plate_number=vehicle.plate_number,
                        alert_type="geofence_violation",
                        severity=severity,
                        geofence_id=fence.id,
                        fence_name=fence.name,
                        fence_type=fence.fence_type,
                        latitude=gps_data.latitude,
                        longitude=gps_data.longitude,
                        speed=gps_data.speed,
                        direction=gps_data.direction,
                        violation_count=new_count,
                        message=f"车辆{vehicle.plate_number}越界{new_count}次，围栏：{fence.name}",
                        status="active"
                    )
                    db.add(alert)
                    db.flush()
                    
                    if vehicle.driver_phone:
                        notification = AlertNotification(
                            alert_id=alert.id,
                            notify_type="sms",
                            notify_target=vehicle.driver_phone,
                            notify_content=f"【校车预警】您驾驶的车辆{vehicle.plate_number}越界{new_count}次，请立即返回指定区域！",
                            notify_status="sent",
                            sent_at=datetime.now()
                        )
                        db.add(notification)
    
    db.commit()
    return {"message": "数据接收成功", "vehicle_id": vehicle.id}


# --- 实时定位 ---
@app.get("/api/realtime/locations")
async def get_realtime_locations(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).filter(
        Vehicle.status != "offline",
        Vehicle.last_location_time.isnot(None)
    ).all()
    
    return [
        {
            "vehicle_id": v.id,
            "plate_number": v.plate_number,
            "driver_name": v.driver_name,
            "device_id": v.device_id,
            "latitude": v.current_lat,
            "longitude": v.current_lng,
            "speed": v.current_speed,
            "direction": v.current_direction,
            "status": v.status,
            "location_time": v.last_location_time
        } for v in vehicles
    ]


@app.get("/api/realtime/locations/{vehicle_id}")
async def get_vehicle_location(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    return {
        "vehicle_id": vehicle.id,
        "plate_number": vehicle.plate_number,
        "driver_name": vehicle.driver_name,
        "device_id": vehicle.device_id,
        "latitude": vehicle.current_lat,
        "longitude": vehicle.current_lng,
        "speed": vehicle.current_speed,
        "direction": vehicle.current_direction,
        "status": vehicle.status,
        "location_time": vehicle.last_location_time
    }


# --- 历史轨迹 ---
@app.get("/api/trajectory/{vehicle_id}")
async def get_trajectory(
    vehicle_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Trajectory).filter(Trajectory.vehicle_id == vehicle_id)
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace(' ', 'T'))
            query = query.filter(Trajectory.location_time >= start_dt)
        except:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace(' ', 'T'))
            query = query.filter(Trajectory.location_time <= end_dt)
        except:
            pass
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    trajectories = query.order_by(desc(Trajectory.location_time)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "data": [
            {
                "id": t.id,
                "vehicle_id": t.vehicle_id,
                "plate_number": t.plate_number,
                "latitude": t.latitude,
                "longitude": t.longitude,
                "altitude": t.altitude,
                "speed": t.speed,
                "direction": t.direction,
                "satellites": t.satellites,
                "gps_accuracy": t.gps_accuracy,
                "location_time": t.location_time,
                "created_at": t.created_at
            } for t in trajectories
        ],
        "page_info": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages
        }
    }


# --- 电子围栏 ---
@app.get("/api/geofences")
async def get_geofences(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    fence_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Geofence)
    
    if fence_type:
        query = query.filter(Geofence.fence_type == fence_type)
    
    if is_active is not None:
        query = query.filter(Geofence.is_active == is_active)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    fences = query.order_by(desc(Geofence.id)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "data": [
            {
                "id": f.id,
                "name": f.name,
                "fence_type": f.fence_type,
                "description": f.description,
                "center_lat": f.center_lat,
                "center_lng": f.center_lng,
                "radius": f.radius,
                "threshold": f.threshold,
                "is_active": f.is_active,
                "created_at": f.created_at,
                "updated_at": f.updated_at
            } for f in fences
        ],
        "page_info": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages
        }
    }


@app.get("/api/geofences/{fence_id}")
async def get_geofence(fence_id: int, db: Session = Depends(get_db)):
    fence = db.query(Geofence).filter(Geofence.id == fence_id).first()
    if not fence:
        raise HTTPException(status_code=404, detail="围栏不存在")
    return {
        "id": fence.id,
        "name": fence.name,
        "fence_type": fence.fence_type,
        "description": fence.description,
        "center_lat": fence.center_lat,
        "center_lng": fence.center_lng,
        "radius": fence.radius,
        "threshold": fence.threshold,
        "is_active": fence.is_active,
        "created_at": fence.created_at,
        "updated_at": fence.updated_at
    }


@app.post("/api/geofences")
async def create_geofence(fence: GeofenceCreate, db: Session = Depends(get_db)):
    new_fence = Geofence(
        name=fence.name,
        fence_type=fence.fence_type,
        description=fence.description,
        center_lat=fence.center_lat,
        center_lng=fence.center_lng,
        radius=fence.radius,
        threshold=fence.threshold,
        is_active=fence.is_active
    )
    db.add(new_fence)
    db.commit()
    db.refresh(new_fence)
    return {"message": "创建成功", "id": new_fence.id}


@app.put("/api/geofences/{fence_id}")
async def update_geofence(fence_id: int, fence: GeofenceUpdate, db: Session = Depends(get_db)):
    db_fence = db.query(Geofence).filter(Geofence.id == fence_id).first()
    if not db_fence:
        raise HTTPException(status_code=404, detail="围栏不存在")
    
    update_data = fence.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_fence, key, value)
    
    db.commit()
    return {"message": "更新成功"}


@app.delete("/api/geofences/{fence_id}")
async def delete_geofence(fence_id: int, db: Session = Depends(get_db)):
    fence = db.query(Geofence).filter(Geofence.id == fence_id).first()
    if not fence:
        raise HTTPException(status_code=404, detail="围栏不存在")
    
    db.delete(fence)
    db.commit()
    return {"message": "删除成功"}


# --- 预警管理 ---
@app.get("/api/alerts")
async def get_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    
    if status:
        query = query.filter(Alert.status == status)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    alerts = query.order_by(desc(Alert.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return {
        "data": [
            {
                "id": a.id,
                "vehicle_id": a.vehicle_id,
                "plate_number": a.plate_number,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "geofence_id": a.geofence_id,
                "fence_name": a.fence_name,
                "fence_type": a.fence_type,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "speed": a.speed,
                "direction": a.direction,
                "violation_count": a.violation_count,
                "message": a.message,
                "status": a.status,
                "resolved_at": a.resolved_at,
                "resolved_by": a.resolved_by,
                "resolve_note": a.resolve_note,
                "created_at": a.created_at
            } for a in alerts
        ],
        "page_info": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages
        }
    }


@app.get("/api/alerts/active/count")
async def get_active_alerts_count(db: Session = Depends(get_db)):
    count = db.query(Alert).filter(Alert.status == "active").count()
    return {"count": count}


@app.get("/api/alerts/{alert_id}")
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="预警不存在")
    return {
        "id": alert.id,
        "vehicle_id": alert.vehicle_id,
        "plate_number": alert.plate_number,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "geofence_id": alert.geofence_id,
        "fence_name": alert.fence_name,
        "fence_type": alert.fence_type,
        "latitude": alert.latitude,
        "longitude": alert.longitude,
        "speed": alert.speed,
        "direction": alert.direction,
        "violation_count": alert.violation_count,
        "message": alert.message,
        "status": alert.status,
        "resolved_at": alert.resolved_at,
        "resolved_by": alert.resolved_by,
        "resolve_note": alert.resolve_note,
        "created_at": alert.created_at
    }


@app.post("/api/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    resolved_by: str = "系统管理员",
    resolve_note: str = "",
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="预警不存在")
    
    alert.status = "resolved"
    alert.resolved_at = datetime.now()
    alert.resolved_by = resolved_by
    alert.resolve_note = resolve_note
    
    db.commit()
    return {"message": "处理成功"}


# --- 数据清理 ---
@app.post("/api/admin/clean-old-data")
async def clean_old_data(db: Session = Depends(get_db)):
    deleted = clean_old_trajectories(db)
    return {"message": f"已清理 {deleted} 条过期轨迹数据"}


# --- 测试数据生成 ---
@app.post("/api/test/init-data")
async def init_test_data(db: Session = Depends(get_db)):
    test_vehicles = [
        {
            "plate_number": "京A12345",
            "driver_name": "张三",
            "driver_phone": "13800138001",
            "driver_license": "A1234567890",
            "vehicle_model": "宇通ZK6102BEV",
            "vehicle_type": "大型校车",
            "school": "阳光小学",
            "capacity": 45,
            "lat": 39.9042,
            "lng": 116.4074
        },
        {
            "plate_number": "京B67890",
            "driver_name": "李四",
            "driver_phone": "13800138002",
            "driver_license": "B1234567890",
            "vehicle_model": "金龙XMQ6110",
            "vehicle_type": "中型校车",
            "school": "实验中学",
            "capacity": 50,
            "lat": 39.9100,
            "lng": 116.4200
        },
        {
            "plate_number": "京C11111",
            "driver_name": "王五",
            "driver_phone": "13800138003",
            "driver_license": "C1234567890",
            "vehicle_model": "黄海DD6109",
            "vehicle_type": "小型校车",
            "school": "幸福幼儿园",
            "capacity": 40,
            "lat": 39.9000,
            "lng": 116.3900
        }
    ]
    
    test_geofences = [
        {
            "name": "阳光小学",
            "fence_type": "school",
            "center_lat": 39.9042,
            "center_lng": 116.4074,
            "radius": 500,
            "threshold": 3,
            "description": "阳光小学上下学区域"
        },
        {
            "name": "建国门危险路段",
            "fence_type": "danger",
            "center_lat": 39.9087,
            "center_lng": 116.4341,
            "radius": 300,
            "threshold": 3,
            "description": "建国门附近交通繁忙危险路段"
        },
        {
            "name": "幸福社区",
            "fence_type": "home",
            "center_lat": 39.9100,
            "center_lng": 116.3800,
            "radius": 1000,
            "threshold": 3,
            "description": "学生家庭所在社区区域"
        }
    ]
    
    created_vehicles = []
    for i, v_data in enumerate(test_vehicles):
        vehicle = Vehicle(
            plate_number=v_data["plate_number"],
            driver_name=v_data["driver_name"],
            driver_phone=v_data["driver_phone"],
            driver_license=v_data["driver_license"],
            vehicle_model=v_data["vehicle_model"],
            vehicle_type=v_data["vehicle_type"],
            school=v_data["school"],
            capacity=v_data["capacity"],
            status="online",
            device_id=f"DEV{str(i + 1).zfill(6)}",
            current_lat=v_data["lat"],
            current_lng=v_data["lng"],
            current_speed=0,
            current_direction=0,
            last_online_time=datetime.now(),
            last_location_time=datetime.now()
        )
        db.add(vehicle)
        db.flush()
        created_vehicles.append(vehicle)
    
    for f_data in test_geofences:
        fence = Geofence(
            name=f_data["name"],
            fence_type=f_data["fence_type"],
            description=f_data["description"],
            center_lat=f_data["center_lat"],
            center_lng=f_data["center_lng"],
            radius=f_data["radius"],
            threshold=f_data["threshold"],
            is_active=True
        )
        db.add(fence)
    
    db.commit()
    
    return {
        "message": "测试数据初始化成功",
        "vehicles_count": len(created_vehicles),
        "geofences_count": len(test_geofences)
    }


@app.post("/api/test/clear-data")
async def clear_test_data(db: Session = Depends(get_db)):
    db.query(AlertNotification).delete()
    db.query(Alert).delete()
    db.query(Trajectory).delete()
    db.query(Geofence).delete()
    db.query(Vehicle).delete()
    db.commit()
    return {"message": "所有测试数据已清除"}


@app.post("/api/test/generate-gps/{vehicle_id}")
async def generate_test_gps(
    vehicle_id: int,
    is_violation: bool = False,
    db: Session = Depends(get_db)
):
    import random
    
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    base_lat = vehicle.current_lat or 39.9042
    base_lng = vehicle.current_lng or 116.4074
    
    radius_km = 10.0 if is_violation else 1.0
    
    lat_radius = radius_km / 111.0
    lng_radius = radius_km / (111.0 * abs(base_lat))
    
    lat_offset = random.uniform(-lat_radius, lat_radius)
    lng_offset = random.uniform(-lng_radius, lng_radius)
    
    new_lat = base_lat + lat_offset
    new_lng = base_lng + lng_offset
    new_speed = random.uniform(0, 60)
    new_direction = random.randint(0, 360)
    
    location_time = datetime.now()
    
    trajectory = Trajectory(
        vehicle_id=vehicle.id,
        plate_number=vehicle.plate_number,
        latitude=new_lat,
        longitude=new_lng,
        altitude=random.uniform(20, 100),
        speed=new_speed,
        direction=new_direction,
        satellites=random.randint(5, 12),
        gps_accuracy=random.uniform(1, 10),
        data_source="test",
        location_time=location_time
    )
    db.add(trajectory)
    
    vehicle.current_lat = new_lat
    vehicle.current_lng = new_lng
    vehicle.current_speed = new_speed
    vehicle.current_direction = new_direction
    vehicle.last_location_time = location_time
    vehicle.last_online_time = datetime.now()
    vehicle.status = "running" if new_speed > 0 else "online"
    
    if is_violation:
        active_fences = db.query(Geofence).filter(Geofence.is_active == True).all()
        for fence in active_fences:
            is_inside = is_point_in_fence(new_lat, new_lng, fence)
            
            if not is_inside:
                day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                today_violations = db.query(Alert).filter(
                    Alert.vehicle_id == vehicle.id,
                    Alert.geofence_id == fence.id,
                    Alert.created_at >= day_start
                ).count()
                
                new_count = today_violations + 1
                
                if new_count >= fence.threshold:
                    severity = "high" if fence.fence_type == "danger" else "medium"
                    alert = Alert(
                        vehicle_id=vehicle.id,
                        plate_number=vehicle.plate_number,
                        alert_type="geofence_violation",
                        severity=severity,
                        geofence_id=fence.id,
                        fence_name=fence.name,
                        fence_type=fence.fence_type,
                        latitude=new_lat,
                        longitude=new_lng,
                        speed=new_speed,
                        direction=new_direction,
                        violation_count=new_count,
                        message=f"车辆{vehicle.plate_number}越界{new_count}次，围栏：{fence.name}",
                        status="active"
                    )
                    db.add(alert)
                    break
    
    db.commit()
    
    return {
        "message": "GPS测试数据生成成功",
        "vehicle_id": vehicle.id,
        "latitude": new_lat,
        "longitude": new_lng,
        "speed": new_speed,
        "is_violation": is_violation
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
