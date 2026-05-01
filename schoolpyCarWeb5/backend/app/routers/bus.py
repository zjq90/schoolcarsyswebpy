"""
校车路由
处理校车相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import Bus, Driver
from backend.app.schemas import BusCreate, BusUpdate, BusResponse

router = APIRouter(prefix="/api/buses", tags=["校车管理"])


@router.get("/", response_model=List[BusResponse])
def get_buses(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取校车列表
    支持分页和状态筛选
    """
    query = db.query(Bus).order_by(desc(Bus.created_at))
    
    if status:
        query = query.filter(Bus.status == status)
    
    buses = query.offset(skip).limit(limit).all()
    return buses


@router.get("/{bus_id}", response_model=BusResponse)
def get_bus(bus_id: int, db: Session = Depends(get_db)):
    """
    获取单个校车详情
    """
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    return bus


@router.post("/", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    """
    创建校车
    """
    # 检查车牌号是否已存在
    existing_bus = db.query(Bus).filter(Bus.plate_number == bus.plate_number).first()
    if existing_bus:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="车牌号已存在"
        )
    
    # 检查校车编号是否已存在
    existing_bus_number = db.query(Bus).filter(Bus.bus_number == bus.bus_number).first()
    if existing_bus_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="校车编号已存在"
        )
    
    db_bus = Bus(**bus.model_dump())
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus


@router.put("/{bus_id}", response_model=BusResponse)
def update_bus(
    bus_id: int,
    bus_update: BusUpdate,
    db: Session = Depends(get_db)
):
    """
    更新校车信息
    """
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    
    update_data = bus_update.model_dump(exclude_unset=True)
    
    # 检查车牌号是否已被其他校车使用
    if "plate_number" in update_data:
        existing_bus = db.query(Bus).filter(
            Bus.plate_number == update_data["plate_number"],
            Bus.id != bus_id
        ).first()
        if existing_bus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="车牌号已被其他校车使用"
            )
    
    # 检查校车编号是否已被其他校车使用
    if "bus_number" in update_data:
        existing_bus_number = db.query(Bus).filter(
            Bus.bus_number == update_data["bus_number"],
            Bus.id != bus_id
        ).first()
        if existing_bus_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="校车编号已被其他校车使用"
            )
    
    for key, value in update_data.items():
        setattr(db_bus, key, value)
    
    db.commit()
    db.refresh(db_bus)
    return db_bus


@router.delete("/{bus_id}")
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    """
    删除校车
    """
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    
    db.delete(db_bus)
    db.commit()
    
    return {"message": "删除成功", "bus_id": bus_id}


@router.put("/{bus_id}/location")
def update_bus_location(
    bus_id: int,
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None,
    speed: Optional[float] = None,
    direction: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    更新校车位置
    """
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not db_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    
    db_bus.current_latitude = latitude
    db_bus.current_longitude = longitude
    
    db.commit()
    
    return {
        "message": "位置更新成功",
        "bus_id": bus_id,
        "latitude": latitude,
        "longitude": longitude
    }


@router.get("/stats/overview")
def get_bus_stats(db: Session = Depends(get_db)):
    """
    获取校车统计
    """
    total_count = db.query(Bus).count()
    idle_count = db.query(Bus).filter(Bus.status == "idle").count()
    running_count = db.query(Bus).filter(Bus.status == "running").count()
    maintenance_count = db.query(Bus).filter(Bus.status == "maintenance").count()
    
    return {
        "total": total_count,
        "idle": idle_count,
        "running": running_count,
        "maintenance": maintenance_count
    }
