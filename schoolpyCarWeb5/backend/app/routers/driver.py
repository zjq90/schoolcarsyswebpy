"""
司机路由
处理司机相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import Driver
from backend.app.schemas import DriverCreate, DriverUpdate, DriverResponse

router = APIRouter(prefix="/api/drivers", tags=["司机管理"])


@router.get("/", response_model=List[DriverResponse])
def get_drivers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取司机列表
    支持分页和状态筛选
    """
    query = db.query(Driver).order_by(desc(Driver.created_at))
    
    if status is not None:
        query = query.filter(Driver.status == status)
    
    drivers = query.offset(skip).limit(limit).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    """
    获取单个司机详情
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    return driver


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """
    创建司机
    """
    # 检查身份证号是否已存在
    if driver.id_card:
        existing_driver = db.query(Driver).filter(Driver.id_card == driver.id_card).first()
        if existing_driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已存在"
            )
    
    # 检查驾驶证号是否已存在
    if driver.license_number:
        existing_license = db.query(Driver).filter(Driver.license_number == driver.license_number).first()
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="驾驶证号已存在"
            )
    
    db_driver = Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    driver_update: DriverUpdate,
    db: Session = Depends(get_db)
):
    """
    更新司机信息
    """
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    
    update_data = driver_update.model_dump(exclude_unset=True)
    
    # 检查身份证号是否已被其他司机使用
    if "id_card" in update_data and update_data["id_card"]:
        existing_driver = db.query(Driver).filter(
            Driver.id_card == update_data["id_card"],
            Driver.id != driver_id
        ).first()
        if existing_driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已被其他司机使用"
            )
    
    # 检查驾驶证号是否已被其他司机使用
    if "license_number" in update_data and update_data["license_number"]:
        existing_license = db.query(Driver).filter(
            Driver.license_number == update_data["license_number"],
            Driver.id != driver_id
        ).first()
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="驾驶证号已被其他司机使用"
            )
    
    for key, value in update_data.items():
        setattr(db_driver, key, value)
    
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    """
    删除司机
    """
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    
    db.delete(db_driver)
    db.commit()
    
    return {"message": "删除成功", "driver_id": driver_id}


@router.get("/stats/overview")
def get_driver_stats(db: Session = Depends(get_db)):
    """
    获取司机统计
    """
    total_count = db.query(Driver).count()
    active_count = db.query(Driver).filter(Driver.status == True).count()
    inactive_count = db.query(Driver).filter(Driver.status == False).count()
    
    return {
        "total": total_count,
        "active": active_count,
        "inactive": inactive_count
    }
