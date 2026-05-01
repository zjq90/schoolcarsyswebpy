"""
校车管理系统 - 运维管理API路由
提供车辆和运维记录相关的RESTful API接口
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, HTTPException

from models.maintenance import (
    VehicleCreate, VehicleUpdate, VehicleResponse,
    MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse, MaintenanceWithDetails
)
from dao.maintenance_dao import VehicleDAO, MaintenanceDAO

# 创建路由
router = APIRouter(prefix="/api/maintenance", tags=["运维管理"])


# ============ 车辆管理 ============

@router.get("/vehicles/", response_model=List[VehicleResponse])
def get_vehicles():
    """
    获取所有车辆列表
    """
    vehicles = VehicleDAO.get_all()
    return vehicles


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int):
    """
    根据ID获取车辆信息
    """
    vehicle = VehicleDAO.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    return vehicle


@router.post("/vehicles/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate):
    """
    创建新车辆
    """
    # 检查车牌号是否已存在
    existing = VehicleDAO.get_by_plate(vehicle.plate_number)
    if existing:
        raise HTTPException(status_code=400, detail="车牌号已存在")
    
    vehicle_id = VehicleDAO.create(
        plate_number=vehicle.plate_number,
        vehicle_type=vehicle.vehicle_type,
        capacity=vehicle.capacity,
        purchase_date=vehicle.purchase_date,
        status=vehicle.status
    )
    return VehicleDAO.get_by_id(vehicle_id)


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate):
    """
    更新车辆信息
    """
    # 检查车辆是否存在
    existing = VehicleDAO.get_by_id(vehicle_id)
    if not existing:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    # 构建更新字段
    update_data = {k: v for k, v in vehicle.dict().items() if v is not None}
    if update_data:
        VehicleDAO.update(vehicle_id, **update_data)
    
    return VehicleDAO.get_by_id(vehicle_id)


@router.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int):
    """
    删除车辆
    """
    existing = VehicleDAO.get_by_id(vehicle_id)
    if not existing:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    success = VehicleDAO.delete(vehicle_id)
    if success:
        return {"message": "删除成功", "success": True}
    raise HTTPException(status_code=500, detail="删除失败")


# ============ 运维记录管理 ============

@router.get("/records/", response_model=List[MaintenanceWithDetails])
def get_maintenance_records(
    vehicle_id: Optional[int] = None,
    record_type: Optional[str] = None,
    limit: int = 100
):
    """
    获取运维记录列表
    - vehicle_id: 指定车辆ID
    - record_type: 记录类型（年检、保险、维修、油耗）
    - limit: 返回记录数量
    """
    if vehicle_id:
        records = MaintenanceDAO.get_by_vehicle(vehicle_id, limit)
    elif record_type:
        records = MaintenanceDAO.get_by_type(record_type, limit)
    else:
        records = MaintenanceDAO.get_all()
    return records[:limit]


@router.get("/records/{record_id}", response_model=MaintenanceWithDetails)
def get_maintenance_record(record_id: int):
    """
    根据ID获取运维记录
    """
    record = MaintenanceDAO.get_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="运维记录不存在")
    return record


@router.post("/records/", response_model=MaintenanceResponse)
def create_maintenance_record(record: MaintenanceCreate):
    """
    创建运维记录
    记录类型包括：
    - 年检：车辆年度安全检查
    - 保险：车辆保险购买
    - 维修：车辆维修保养
    - 油耗：燃油消耗统计
    """
    # 检查车辆是否存在
    vehicle = VehicleDAO.get_by_id(record.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=400, detail="指定车辆不存在")
    
    record_id = MaintenanceDAO.create(
        record_type=record.record_type,
        vehicle_id=record.vehicle_id,
        driver_id=record.driver_id,
        record_date=record.record_date,
        amount=record.amount,
        description=record.description,
        status=record.status
    )
    return MaintenanceDAO.get_by_id(record_id)


@router.put("/records/{record_id}", response_model=MaintenanceResponse)
def update_maintenance_record(record_id: int, record: MaintenanceUpdate):
    """
    更新运维记录
    """
    # 检查记录是否存在
    existing = MaintenanceDAO.get_by_id(record_id)
    if not existing:
        raise HTTPException(status_code=404, detail="运维记录不存在")
    
    # 构建更新字段
    update_data = {k: v for k, v in record.dict().items() if v is not None}
    if update_data:
        MaintenanceDAO.update(record_id, **update_data)
    
    return MaintenanceDAO.get_by_id(record_id)


@router.delete("/records/{record_id}")
def delete_maintenance_record(record_id: int):
    """
    删除运维记录
    """
    existing = MaintenanceDAO.get_by_id(record_id)
    if not existing:
        raise HTTPException(status_code=404, detail="运维记录不存在")
    
    success = MaintenanceDAO.delete(record_id)
    if success:
        return {"message": "删除成功", "success": True}
    raise HTTPException(status_code=500, detail="删除失败")


@router.get("/statistics/by-type")
def get_statistics_by_type(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    按类型统计运维金额
    统计各类型（年检、保险、维修、油耗）的记录数量和总金额
    """
    stats = MaintenanceDAO.get_statistics_by_type(start_date, end_date)
    
    # 添加类型名称映射
    type_names = {
        "年检": "年度检查",
        "保险": "保险购买",
        "维修": "维修保养",
        "油耗": "燃油消耗"
    }
    
    for stat in stats:
        stat['type_name'] = type_names.get(stat['record_type'], stat['record_type'])
    
    # 计算总计
    total_count = sum(s['record_count'] for s in stats)
    total_amount = sum(s['total_amount'] or 0 for s in stats)
    
    return {
        "statistics": stats,
        "summary": {
            "total_count": total_count,
            "total_amount": round(total_amount, 2),
            "start_date": start_date,
            "end_date": end_date
        }
    }


@router.post("/fuel-consumption")
def record_fuel_consumption(
    vehicle_id: int,
    record_date: date,
    liters: float,
    cost: float,
    odometer: float = None,
    driver_id: int = None
):
    """
    记录油耗（专用接口）
    - vehicle_id: 车辆ID
    - record_date: 记录日期
    - liters: 加油升数
    - cost: 加油金额
    - odometer: 当前里程数（可选）
    - driver_id: 司机ID（可选）
    """
    # 检查车辆是否存在
    vehicle = VehicleDAO.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=400, detail="指定车辆不存在")
    
    description = f"加油{liters}升，金额{cost}元"
    if odometer:
        description += f"，里程表{odometer}公里"
    
    record_id = MaintenanceDAO.create(
        record_type="油耗",
        vehicle_id=vehicle_id,
        driver_id=driver_id,
        record_date=record_date,
        amount=cost,
        description=description,
        status="completed"
    )
    
    return {
        "message": "油耗记录成功",
        "record_id": record_id,
        "vehicle_plate": vehicle['plate_number']
    }
