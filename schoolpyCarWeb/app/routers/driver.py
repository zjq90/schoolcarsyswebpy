"""
司机管理路由模块
处理司机的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.driver import Driver
from app.models.user import User
from app.schemas.driver import DriverCreate, DriverResponse, DriverUpdate
from app.routers.auth import get_current_user
from app.config import ROLES

router = APIRouter(prefix="/api/drivers", tags=["司机管理"])


@router.get("/", response_model=List[DriverResponse])
def get_drivers(
    skip: int = 0,
    limit: int = 100,
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取司机列表
    教育局管理员可以查看所有司机，学校管理员只能查看本校司机
    """
    query = db.query(Driver)
    
    # 权限控制：学校管理员只能看本校司机
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Driver.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Driver.school_id == school_id)
    
    # 状态过滤
    if status:
        query = query.filter(Driver.status == status)
    
    # 关键词搜索（姓名、司机编码、驾驶证号）
    if keyword:
        query = query.filter(
            (Driver.real_name.contains(keyword)) |
            (Driver.driver_code.contains(keyword)) |
            (Driver.license_number.contains(keyword))
        )
    
    # 分页
    drivers = query.offset(skip).limit(limit).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个司机详情
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    
    # 权限控制：学校管理员只能查看本校司机
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if driver.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校的司机"
            )
    
    return driver


@router.post("/", response_model=DriverResponse)
def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新司机
    教育局管理员可以创建任意学校的司机，学校管理员只能创建本校司机
    """
    # 权限控制：学校管理员只能创建本校司机
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if driver_data.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：只能创建本校的司机"
            )
    
    # 检查身份证号是否已存在
    if driver_data.id_card:
        existing_driver = db.query(Driver).filter(
            Driver.id_card == driver_data.id_card
        ).first()
        if existing_driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已存在"
            )
    
    # 检查司机编码是否已存在
    if driver_data.driver_code:
        existing_code = db.query(Driver).filter(
            Driver.driver_code == driver_data.driver_code
        ).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="司机编码已存在"
            )
    
    # 创建司机
    new_driver = Driver(**driver_data.model_dump())
    
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    return new_driver


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    driver_data: DriverUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新司机信息
    教育局管理员可以更新所有司机，学校管理员只能更新本校司机
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if driver.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校的司机"
            )
    
    # 更新司机信息
    update_data = driver_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(driver, key, value)
    
    db.commit()
    db.refresh(driver)
    
    return driver


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除司机
    教育局管理员可以删除任意司机，学校管理员只能删除本校司机
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if driver.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法删除其他学校的司机"
            )
    
    db.delete(driver)
    db.commit()
    
    return {"message": "司机删除成功"}


@router.get("/stats/overview")
def get_driver_stats(
    school_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取司机统计信息
    """
    query = db.query(Driver)
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Driver.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Driver.school_id == school_id)
    
    # 统计各状态司机数量
    total = query.count()
    available = query.filter(Driver.status == "available").count()
    on_duty = query.filter(Driver.status == "on_duty").count()
    on_leave = query.filter(Driver.status == "on_leave").count()
    disabled = query.filter(Driver.status == "disabled").count()
    
    # 平均驾龄
    drivers = query.all()
    total_driving_years = sum(d.driving_years for d in drivers)
    avg_driving_years = round(total_driving_years / total, 1) if total > 0 else 0
    
    stats = {
        "total": total,
        "avg_driving_years": avg_driving_years,
        "by_status": {
            "available": available,
            "on_duty": on_duty,
            "on_leave": on_leave,
            "disabled": disabled
        }
    }
    
    return stats
