"""
校车管理系统 - 司机管理API路由
提供司机和司机评分相关的RESTful API接口
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from models.driver import (
    DriverCreate, DriverUpdate, DriverResponse,
    DriverScoreCreate, DriverScoreResponse, DriverScoreWithDriver
)
from dao.driver_dao import DriverDAO, DriverScoreDAO

# 创建路由
router = APIRouter(prefix="/api/drivers", tags=["司机管理"])


# ============ 司机管理 ============

@router.get("/", response_model=List[DriverResponse])
def get_drivers():
    """
    获取所有司机列表
    """
    drivers = DriverDAO.get_all()
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int):
    """
    根据ID获取司机信息
    """
    driver = DriverDAO.get_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    return driver


@router.post("/", response_model=DriverResponse)
def create_driver(driver: DriverCreate):
    """
    创建新司机
    """
    driver_id = DriverDAO.create(
        name=driver.name,
        phone=driver.phone,
        license_no=driver.license_no,
        hire_date=driver.hire_date,
        status=driver.status
    )
    return DriverDAO.get_by_id(driver_id)


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver: DriverUpdate):
    """
    更新司机信息
    """
    # 检查司机是否存在
    existing = DriverDAO.get_by_id(driver_id)
    if not existing:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    # 构建更新字段
    update_data = {k: v for k, v in driver.dict().items() if v is not None}
    if update_data:
        DriverDAO.update(driver_id, **update_data)
    
    return DriverDAO.get_by_id(driver_id)


@router.delete("/{driver_id}")
def delete_driver(driver_id: int):
    """
    删除司机
    """
    existing = DriverDAO.get_by_id(driver_id)
    if not existing:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    success = DriverDAO.delete(driver_id)
    if success:
        return {"message": "删除成功", "success": True}
    raise HTTPException(status_code=500, detail="删除失败")


# ============ 司机评分管理 ============

@router.get("/scores/", response_model=List[DriverScoreWithDriver])
def get_driver_scores(
    driver_id: Optional[int] = None,
    score_date: Optional[date] = None,
    limit: int = 100
):
    """
    获取司机评分记录
    - driver_id: 指定司机ID
    - score_date: 指定日期
    - limit: 返回记录数量
    """
    if driver_id:
        scores = DriverScoreDAO.get_by_driver(driver_id, limit)
    elif score_date:
        scores = DriverScoreDAO.get_by_date(score_date)
    else:
        scores = DriverScoreDAO.get_all()
    return scores[:limit]


@router.get("/scores/{score_id}", response_model=DriverScoreWithDriver)
def get_driver_score(score_id: int):
    """
    根据ID获取评分记录
    """
    score = DriverScoreDAO.get_by_id(score_id)
    if not score:
        raise HTTPException(status_code=404, detail="评分记录不存在")
    return score


@router.post("/scores/", response_model=DriverScoreResponse)
def create_driver_score(score: DriverScoreCreate):
    """
    创建司机评分记录（自动计算信用分）
    评分规则：
    - 基础分：100分
    - 每次违章扣5分
    - 每次投诉扣10分
    - 每安全驾驶1小时加0.5分
    """
    score_id = DriverScoreDAO.create(
        driver_id=score.driver_id,
        score_date=score.score_date,
        violation_count=score.violation_count,
        complaint_count=score.complaint_count,
        safe_driving_hours=score.safe_driving_hours,
        notes=score.notes
    )
    return DriverScoreDAO.get_by_id(score_id)


@router.get("/{driver_id}/scores/average")
def get_driver_average_score(driver_id: int, days: int = 30):
    """
    获取指定司机最近N天的平均信用分
    """
    # 检查司机是否存在
    driver = DriverDAO.get_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    avg_score = DriverScoreDAO.get_average_score(driver_id, days)
    if avg_score is None:
        return {"driver_id": driver_id, "driver_name": driver['name'], "average_score": 0, "days": days}
    
    return {
        "driver_id": driver_id,
        "driver_name": driver['name'],
        "average_score": round(avg_score, 2),
        "days": days
    }


@router.post("/{driver_id}/generate-daily-score")
def generate_daily_score(
    driver_id: int,
    score_date: date = None,
    violation_count: int = 0,
    complaint_count: int = 0,
    safe_driving_hours: float = 6.0
):
    """
    为司机生成每日评分记录
    这是一个简化的接口，用于演示每日评分生成功能
    """
    # 检查司机是否存在
    driver = DriverDAO.get_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="司机不存在")
    
    if not score_date:
        score_date = date.today()
    
    score_id = DriverScoreDAO.create(
        driver_id=driver_id,
        score_date=score_date,
        violation_count=violation_count,
        complaint_count=complaint_count,
        safe_driving_hours=safe_driving_hours,
        notes=f"自动生成的{score_date}评分记录"
    )
    
    score = DriverScoreDAO.get_by_id(score_id)
    return {
        "message": "每日评分生成成功",
        "score": score
    }
