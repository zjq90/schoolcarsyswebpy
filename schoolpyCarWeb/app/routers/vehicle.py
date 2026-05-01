"""
车辆管理路由模块
处理车辆的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.routers.auth import get_current_user
from app.config import ROLES

router = APIRouter(prefix="/api/vehicles", tags=["车辆管理"])


@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    skip: int = 0,
    limit: int = 100,
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取车辆列表
    教育局管理员可以查看所有车辆，学校管理员只能查看本校车辆
    """
    query = db.query(Vehicle)
    
    # 权限控制：学校管理员只能看本校车辆
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Vehicle.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Vehicle.school_id == school_id)
    
    # 状态过滤
    if status:
        query = query.filter(Vehicle.status == status)
    
    # 关键词搜索（车牌号、车辆编码、型号）
    if keyword:
        query = query.filter(
            (Vehicle.license_plate.contains(keyword)) |
            (Vehicle.vehicle_code.contains(keyword)) |
            (Vehicle.vehicle_model.contains(keyword))
        )
    
    # 分页
    vehicles = query.offset(skip).limit(limit).all()
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个车辆详情
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="车辆不存在"
        )
    
    # 权限控制：学校管理员只能查看本校车辆
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if vehicle.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校的车辆"
            )
    
    return vehicle


@router.post("/", response_model=VehicleResponse)
def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新车辆
    教育局管理员可以创建任意学校的车辆，学校管理员只能创建本校车辆
    """
    # 权限控制：学校管理员只能创建本校车辆
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if vehicle_data.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：只能创建本校的车辆"
            )
    
    # 检查车牌号是否已存在
    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.license_plate == vehicle_data.license_plate
    ).first()
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="车牌号已存在"
        )
    
    # 检查车辆编码是否已存在
    if vehicle_data.vehicle_code:
        existing_code = db.query(Vehicle).filter(
            Vehicle.vehicle_code == vehicle_data.vehicle_code
        ).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="车辆编码已存在"
            )
    
    # 创建车辆
    new_vehicle = Vehicle(**vehicle_data.model_dump())
    
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    
    return new_vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新车辆信息
    教育局管理员可以更新所有车辆，学校管理员只能更新本校车辆
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="车辆不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if vehicle.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校的车辆"
            )
    
    # 更新车辆信息
    update_data = vehicle_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle, key, value)
    
    db.commit()
    db.refresh(vehicle)
    
    return vehicle


@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除车辆
    教育局管理员可以删除任意车辆，学校管理员只能删除本校车辆
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="车辆不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if vehicle.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法删除其他学校的车辆"
            )
    
    db.delete(vehicle)
    db.commit()
    
    return {"message": "车辆删除成功"}


@router.get("/stats/overview")
def get_vehicle_stats(
    school_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取车辆统计信息
    """
    query = db.query(Vehicle)
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Vehicle.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Vehicle.school_id == school_id)
    
    # 统计各状态车辆数量
    total = query.count()
    available = query.filter(Vehicle.status == "available").count()
    in_use = query.filter(Vehicle.status == "in_use").count()
    maintenance = query.filter(Vehicle.status == "maintenance").count()
    disabled = query.filter(Vehicle.status == "disabled").count()
    
    # 统计总座位数
    total_seats = sum(v.seat_count for v in query.all())
    
    stats = {
        "total": total,
        "total_seats": total_seats,
        "by_status": {
            "available": available,
            "in_use": in_use,
            "maintenance": maintenance,
            "disabled": disabled
        }
    }
    
    return stats
