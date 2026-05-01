"""
报警类型路由
处理报警类型相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import AlarmType, AlarmLevel
from backend.app.schemas import AlarmTypeCreate, AlarmTypeUpdate, AlarmTypeResponse

router = APIRouter(prefix="/api/alarm-types", tags=["报警类型管理"])


def build_alarm_type_detail(alarm_type: AlarmType, db: Session) -> dict:
    """
    构建完整的报警类型详情字典，包含级别信息
    """
    level = db.query(AlarmLevel).filter(AlarmLevel.id == alarm_type.level_id).first()
    
    return {
        "id": alarm_type.id,
        "name": alarm_type.name,
        "level_id": alarm_type.level_id,
        "description": alarm_type.description,
        "trigger_condition": alarm_type.trigger_condition,
        "is_auto": alarm_type.is_auto,
        "created_at": alarm_type.created_at.isoformat() if alarm_type.created_at else None,
        "updated_at": alarm_type.updated_at.isoformat() if alarm_type.updated_at else None,
        "level_name": level.name if level else None,
        "level_color": level.color if level else None,
        "level_description": level.description if level else None,
        "response_mechanism": level.response_mechanism if level else None
    }


@router.get("/")
def get_alarm_types(
    skip: int = 0,
    limit: int = 100,
    level_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取报警类型列表（完整信息版本）
    支持分页和级别筛选
    返回包含级别信息的完整数据
    """
    query = db.query(AlarmType).order_by(desc(AlarmType.created_at))
    
    if level_id:
        query = query.filter(AlarmType.level_id == level_id)
    
    types = query.offset(skip).limit(limit).all()
    
    result = [build_alarm_type_detail(alarm_type, db) for alarm_type in types]
    return result


@router.get("/{type_id}")
def get_alarm_type(type_id: int, db: Session = Depends(get_db)):
    """
    获取单个报警类型详情（完整信息版本）
    """
    alarm_type = db.query(AlarmType).filter(AlarmType.id == type_id).first()
    if not alarm_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警类型不存在"
        )
    return build_alarm_type_detail(alarm_type, db)


@router.post("/", response_model=AlarmTypeResponse, status_code=status.HTTP_201_CREATED)
def create_alarm_type(alarm_type: AlarmTypeCreate, db: Session = Depends(get_db)):
    """
    创建报警类型
    """
    existing_level = db.query(AlarmLevel).filter(AlarmLevel.id == alarm_type.level_id).first()
    if not existing_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定的报警级别不存在"
        )
    
    db_type = AlarmType(**alarm_type.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


@router.put("/{type_id}")
def update_alarm_type(
    type_id: int,
    type_update: AlarmTypeUpdate,
    db: Session = Depends(get_db)
):
    """
    更新报警类型
    返回完整的报警类型详情
    """
    db_type = db.query(AlarmType).filter(AlarmType.id == type_id).first()
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警类型不存在"
        )
    
    update_data = type_update.model_dump(exclude_unset=True)
    
    if "level_id" in update_data:
        existing_level = db.query(AlarmLevel).filter(AlarmLevel.id == update_data["level_id"]).first()
        if not existing_level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定的报警级别不存在"
            )
    
    for key, value in update_data.items():
        setattr(db_type, key, value)
    
    db.commit()
    db.refresh(db_type)
    return build_alarm_type_detail(db_type, db)


@router.delete("/{type_id}")
def delete_alarm_type(type_id: int, db: Session = Depends(get_db)):
    """
    删除报警类型
    """
    db_type = db.query(AlarmType).filter(AlarmType.id == type_id).first()
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警类型不存在"
        )
    
    from backend.app.models import Alarm
    related_alarms = db.query(Alarm).filter(Alarm.type_id == type_id).count()
    if related_alarms > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该类型下有 {related_alarms} 个报警记录，无法删除"
        )
    
    db.delete(db_type)
    db.commit()
    
    return {"message": "删除成功", "type_id": type_id}


@router.get("/by-level/{level}")
def get_alarm_types_by_level(level: int, db: Session = Depends(get_db)):
    """
    根据级别获取报警类型列表
    级别: 1-一级(红色), 2-二级(橙色), 3-三级(蓝色)
    """
    level_obj = db.query(AlarmLevel).filter(AlarmLevel.level == level).first()
    if not level_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"级别 {level} 不存在"
        )
    
    types = db.query(AlarmType).filter(AlarmType.level_id == level_obj.id).all()
    result = [build_alarm_type_detail(t, db) for t in types]
    return result
