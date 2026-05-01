"""
报警路由
处理报警相关的API接口
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import Alarm, AlarmLevel, AlarmType, Bus, Driver
from backend.app.schemas import (
    AlarmCreate, AlarmUpdate, AlarmResponse, AlarmTrigger
)

router = APIRouter(prefix="/api/alarms", tags=["报警管理"])


def build_alarm_detail(alarm: Alarm, db: Session) -> dict:
    """
    构建完整的报警详情字典，包含级别、类型、校车等关联信息
    """
    level = db.query(AlarmLevel).filter(AlarmLevel.id == alarm.level_id).first()
    alarm_type = db.query(AlarmType).filter(AlarmType.id == alarm.type_id).first()
    bus = db.query(Bus).filter(Bus.id == alarm.bus_id).first()
    driver = db.query(Driver).filter(Driver.id == alarm.driver_id).first() if alarm.driver_id else None
    
    return {
        "id": alarm.id,
        "alarm_number": alarm.alarm_number,
        "type_id": alarm.type_id,
        "level_id": alarm.level_id,
        "bus_id": alarm.bus_id,
        "driver_id": alarm.driver_id,
        "latitude": alarm.latitude,
        "longitude": alarm.longitude,
        "location_name": alarm.location_name,
        "status": alarm.status,
        "is_read": alarm.is_read,
        "triggered_at": alarm.triggered_at.isoformat() if alarm.triggered_at else None,
        "resolved_at": alarm.resolved_at.isoformat() if alarm.resolved_at else None,
        "description": alarm.description,
        "remark": alarm.remark,
        "created_at": alarm.created_at.isoformat() if alarm.created_at else None,
        "updated_at": alarm.updated_at.isoformat() if alarm.updated_at else None,
        "level_name": level.name if level else None,
        "level_color": level.color if level else None,
        "level_description": level.description if level else None,
        "type_name": alarm_type.name if alarm_type else None,
        "type_description": alarm_type.description if alarm_type else None,
        "is_auto_type": alarm_type.is_auto if alarm_type else False,
        "bus_plate": bus.plate_number if bus else None,
        "bus_number": bus.bus_number if bus else None,
        "bus_model": bus.model if bus else None,
        "driver_name": driver.name if driver else None,
        "driver_phone": driver.phone if driver else None
    }


@router.get("/")
def get_alarms(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    level_id: Optional[int] = None,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取报警列表（完整信息版本）
    支持分页、状态筛选、级别筛选、已读筛选
    返回包含级别、类型、校车等关联信息的完整数据
    """
    query = db.query(Alarm).order_by(desc(Alarm.triggered_at))
    
    if status:
        query = query.filter(Alarm.status == status)
    if level_id:
        query = query.filter(Alarm.level_id == level_id)
    if is_read is not None:
        query = query.filter(Alarm.is_read == is_read)
    
    alarms = query.offset(skip).limit(limit).all()
    
    result = [build_alarm_detail(alarm, db) for alarm in alarms]
    return result


@router.get("/{alarm_id}")
def get_alarm(alarm_id: int, db: Session = Depends(get_db)):
    """
    获取单个报警详情（完整信息版本）
    """
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not alarm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警记录不存在"
        )
    return build_alarm_detail(alarm, db)


@router.post("/", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED)
def create_alarm(alarm: AlarmCreate, db: Session = Depends(get_db)):
    """
    创建报警记录
    """
    alarm_type = db.query(AlarmType).filter(AlarmType.id == alarm.type_id).first()
    if not alarm_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警类型不存在"
        )
    
    bus = db.query(Bus).filter(Bus.id == alarm.bus_id).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    
    db_alarm = Alarm(**alarm.model_dump())
    db.add(db_alarm)
    db.commit()
    db.refresh(db_alarm)
    return db_alarm


@router.post("/trigger")
def trigger_alarm(trigger: AlarmTrigger, db: Session = Depends(get_db)):
    """
    触发报警
    这是核心功能，用于模拟或实际触发报警事件
    返回完整的报警详情
    """
    alarm_type = db.query(AlarmType).filter(AlarmType.id == trigger.type_id).first()
    if not alarm_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警类型不存在"
        )
    
    bus = db.query(Bus).filter(Bus.id == trigger.bus_id).first()
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="校车不存在"
        )
    
    import time
    import random
    alarm_number = f"ALM{int(time.time())}{random.randint(1000, 9999)}"
    
    db_alarm = Alarm(
        alarm_number=alarm_number,
        type_id=trigger.type_id,
        level_id=alarm_type.level_id,
        bus_id=trigger.bus_id,
        driver_id=bus.driver_id,
        latitude=trigger.latitude if trigger.latitude else bus.current_latitude,
        longitude=trigger.longitude if trigger.longitude else bus.current_longitude,
        location_name=trigger.location_name,
        status="pending",
        is_read=False,
        description=trigger.description or alarm_type.description,
        triggered_at=datetime.now()
    )
    
    db.add(db_alarm)
    db.commit()
    db.refresh(db_alarm)
    
    return build_alarm_detail(db_alarm, db)


@router.put("/{alarm_id}")
def update_alarm(
    alarm_id: int,
    alarm_update: AlarmUpdate,
    db: Session = Depends(get_db)
):
    """
    更新报警记录
    返回完整的报警详情
    """
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not db_alarm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警记录不存在"
        )
    
    update_data = alarm_update.model_dump(exclude_unset=True)
    
    if "status" in update_data and update_data["status"] == "resolved":
        update_data["resolved_at"] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_alarm, key, value)
    
    db.commit()
    db.refresh(db_alarm)
    return build_alarm_detail(db_alarm, db)


@router.put("/{alarm_id}/read")
def mark_as_read(alarm_id: int, db: Session = Depends(get_db)):
    """
    标记报警为已读
    """
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not db_alarm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警记录不存在"
        )
    
    db_alarm.is_read = True
    db.commit()
    
    return {"message": "已标记为已读", "alarm_id": alarm_id, "is_read": True}


@router.delete("/{alarm_id}")
def delete_alarm(alarm_id: int, db: Session = Depends(get_db)):
    """
    删除报警记录
    """
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not db_alarm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警记录不存在"
        )
    
    db.delete(db_alarm)
    db.commit()
    
    return {"message": "删除成功", "alarm_id": alarm_id}


@router.get("/stats/overview")
def get_alarm_stats(db: Session = Depends(get_db)):
    """
    获取报警统计概览
    """
    pending_count = db.query(Alarm).filter(Alarm.status == "pending").count()
    processing_count = db.query(Alarm).filter(Alarm.status == "processing").count()
    resolved_count = db.query(Alarm).filter(Alarm.status == "resolved").count()
    closed_count = db.query(Alarm).filter(Alarm.status == "closed").count()
    
    level1_count = db.query(Alarm).filter(Alarm.level_id == 1).count()
    level2_count = db.query(Alarm).filter(Alarm.level_id == 2).count()
    level3_count = db.query(Alarm).filter(Alarm.level_id == 3).count()
    
    unread_count = db.query(Alarm).filter(Alarm.is_read == False).count()
    
    return {
        "status_stats": {
            "pending": pending_count,
            "processing": processing_count,
            "resolved": resolved_count,
            "closed": closed_count
        },
        "level_stats": {
            "level1": level1_count,
            "level2": level2_count,
            "level3": level3_count
        },
        "unread_count": unread_count
    }


@router.get("/unread/latest")
def get_latest_unread_alarms(db: Session = Depends(get_db)):
    """
    获取最新的未读报警
    用于前端轮询获取最新报警
    """
    alarms = db.query(Alarm).filter(
        Alarm.is_read == False,
        Alarm.status.in_(["pending", "processing"])
    ).order_by(desc(Alarm.triggered_at)).limit(10).all()
    
    result = [build_alarm_detail(alarm, db) for alarm in alarms]
    return result


@router.post("/{alarm_id}/process")
def process_alarm(
    alarm_id: int,
    action: str,
    remark: Optional[str] = None,
    notify_police: bool = False,
    notify_school: bool = False,
    notify_parents: bool = False,
    notify_driver: bool = False,
    db: Session = Depends(get_db)
):
    """
    处理报警（高级功能）
    支持不同的处理动作和通知设置
    """
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if not db_alarm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警记录不存在"
        )
    
    if action == "start":
        db_alarm.status = "processing"
    elif action == "resolve":
        db_alarm.status = "resolved"
        db_alarm.resolved_at = datetime.now()
    elif action == "close":
        db_alarm.status = "closed"
    elif action == "read":
        db_alarm.is_read = True
    
    if remark:
        db_alarm.remark = (db_alarm.remark or "") + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {remark}"
    
    db_alarm.is_read = True
    db.commit()
    db.refresh(db_alarm)
    
    return {
        "message": "处理成功",
        "alarm_id": alarm_id,
        "action": action,
        "status": db_alarm.status,
        "notify_police": notify_police,
        "notify_school": notify_school,
        "notify_parents": notify_parents,
        "notify_driver": notify_driver
    }
