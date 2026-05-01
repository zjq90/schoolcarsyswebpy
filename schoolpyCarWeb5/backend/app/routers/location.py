"""
位置记录路由
处理位置记录相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import Location, Bus
from backend.app.schemas import LocationCreate, LocationResponse

router = APIRouter(prefix="/api/locations", tags=["位置管理"])


@router.get("/", response_model=List[LocationResponse])
def get_locations(
    skip: int = 0,
    limit: int = 100,
    bus_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取位置记录列表
    支持分页和校车筛选
    """
    query = db.query(Location).order_by(desc(Location.created_at))
    
    if bus_id:
        query = query.filter(Location.bus_id == bus_id)
    
    locations = query.offset(skip).limit(limit).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """
    获取单个位置记录详情
    """
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="位置记录不存在"
        )
    return location


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """
    创建位置记录
    用于上报校车位置信息
    """
    # 检查校车是否存在
    existing_bus = db.query(Bus).filter(Bus.id == location.bus_id).first()
    if not existing_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定的校车不存在"
        )
    
    db_location = Location(**location.model_dump())
    db.add(db_location)
    
    # 同时更新校车的当前位置
    existing_bus.current_latitude = location.latitude
    existing_bus.current_longitude = location.longitude
    
    db.commit()
    db.refresh(db_location)
    return db_location


@router.get("/bus/{bus_id}/latest")
def get_bus_latest_location(bus_id: int, db: Session = Depends(get_db)):
    """
    获取校车的最新位置
    """
    # 检查校车是否存在
    existing_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not existing_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定的校车不存在"
        )
    
    # 获取最新的位置记录
    latest_location = db.query(Location).filter(
        Location.bus_id == bus_id
    ).order_by(desc(Location.created_at)).first()
    
    if latest_location:
        return {
            "bus_id": bus_id,
            "plate_number": existing_bus.plate_number,
            "bus_number": existing_bus.bus_number,
            "latitude": latest_location.latitude,
            "longitude": latest_location.longitude,
            "location_name": latest_location.location_name,
            "speed": latest_location.speed,
            "direction": latest_location.direction,
            "recorded_at": latest_location.created_at.isoformat()
        }
    else:
        return {
            "bus_id": bus_id,
            "plate_number": existing_bus.plate_number,
            "bus_number": existing_bus.bus_number,
            "latitude": existing_bus.current_latitude,
            "longitude": existing_bus.current_longitude,
            "location_name": None,
            "speed": 0,
            "direction": 0,
            "recorded_at": None
        }


@router.get("/bus/{bus_id}/history")
def get_bus_location_history(
    bus_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    获取校车的位置历史记录
    """
    # 检查校车是否存在
    existing_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not existing_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定的校车不存在"
        )
    
    locations = db.query(Location).filter(
        Location.bus_id == bus_id
    ).order_by(desc(Location.created_at)).limit(limit).all()
    
    return {
        "bus_id": bus_id,
        "plate_number": existing_bus.plate_number,
        "bus_number": existing_bus.bus_number,
        "locations": [
            {
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "location_name": loc.location_name,
                "speed": loc.speed,
                "direction": loc.direction,
                "recorded_at": loc.created_at.isoformat()
            }
            for loc in locations
        ]
    }
