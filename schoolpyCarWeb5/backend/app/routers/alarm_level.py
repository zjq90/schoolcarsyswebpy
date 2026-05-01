"""
报警级别路由
处理报警级别相关的API接口
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import AlarmLevel
from backend.app.schemas import AlarmLevelCreate, AlarmLevelUpdate, AlarmLevelResponse

router = APIRouter(prefix="/api/alarm-levels", tags=["报警级别管理"])


@router.get("/", response_model=List[AlarmLevelResponse])
def get_alarm_levels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取报警级别列表
    """
    query = db.query(AlarmLevel).order_by(AlarmLevel.level)
    levels = query.offset(skip).limit(limit).all()
    return levels


@router.get("/{level_id}", response_model=AlarmLevelResponse)
def get_alarm_level(level_id: int, db: Session = Depends(get_db)):
    """
    获取单个报警级别详情
    """
    level = db.query(AlarmLevel).filter(AlarmLevel.id == level_id).first()
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警级别不存在"
        )
    return level


@router.post("/", response_model=AlarmLevelResponse, status_code=status.HTTP_201_CREATED)
def create_alarm_level(level: AlarmLevelCreate, db: Session = Depends(get_db)):
    """
    创建报警级别
    """
    # 检查级别值是否已存在
    existing_level = db.query(AlarmLevel).filter(AlarmLevel.level == level.level).first()
    if existing_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"级别 {level.level} 已存在"
        )
    
    db_level = AlarmLevel(**level.model_dump())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level


@router.put("/{level_id}", response_model=AlarmLevelResponse)
def update_alarm_level(
    level_id: int,
    level_update: AlarmLevelUpdate,
    db: Session = Depends(get_db)
):
    """
    更新报警级别
    """
    db_level = db.query(AlarmLevel).filter(AlarmLevel.id == level_id).first()
    if not db_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警级别不存在"
        )
    
    update_data = level_update.model_dump(exclude_unset=True)
    
    # 检查级别值是否已被其他级别使用
    if "level" in update_data:
        existing_level = db.query(AlarmLevel).filter(
            AlarmLevel.level == update_data["level"],
            AlarmLevel.id != level_id
        ).first()
        if existing_level:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"级别 {update_data['level']} 已被其他级别使用"
            )
    
    for key, value in update_data.items():
        setattr(db_level, key, value)
    
    db.commit()
    db.refresh(db_level)
    return db_level


@router.delete("/{level_id}")
def delete_alarm_level(level_id: int, db: Session = Depends(get_db)):
    """
    删除报警级别
    """
    db_level = db.query(AlarmLevel).filter(AlarmLevel.id == level_id).first()
    if not db_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报警级别不存在"
        )
    
    # 检查是否有关联的报警类型
    from backend.app.models import AlarmType
    related_types = db.query(AlarmType).filter(AlarmType.level_id == level_id).count()
    if related_types > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该级别下有 {related_types} 个报警类型，无法删除"
        )
    
    db.delete(db_level)
    db.commit()
    
    return {"message": "删除成功", "level_id": level_id}
