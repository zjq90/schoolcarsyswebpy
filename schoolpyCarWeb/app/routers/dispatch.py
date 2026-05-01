"""
调度管理路由模块
处理跨校调度的增删改查功能（教育局管理员专用）
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dispatch import Dispatch
from app.models.user import User
from app.schemas.dispatch import DispatchCreate, DispatchResponse, DispatchUpdate
from app.routers.auth import get_current_user, get_current_user_with_permission
from app.config import ROLES

router = APIRouter(prefix="/api/dispatches", tags=["调度管理"])


@router.get("/", response_model=List[DispatchResponse])
def get_dispatches(
    skip: int = 0,
    limit: int = 100,
    from_school_id: Optional[int] = None,
    to_school_id: Optional[int] = None,
    dispatch_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    获取调度列表
    只有教育局管理员可以查看调度
    """
    query = db.query(Dispatch)
    
    # 调出学校过滤
    if from_school_id is not None:
        query = query.filter(Dispatch.from_school_id == from_school_id)
    
    # 调入学校过滤
    if to_school_id is not None:
        query = query.filter(Dispatch.to_school_id == to_school_id)
    
    # 类型过滤
    if dispatch_type:
        query = query.filter(Dispatch.dispatch_type == dispatch_type)
    
    # 状态过滤
    if status:
        query = query.filter(Dispatch.status == status)
    
    # 排序：按创建时间倒序
    query = query.order_by(Dispatch.created_at.desc())
    
    # 分页
    dispatches = query.offset(skip).limit(limit).all()
    return dispatches


@router.get("/{dispatch_id}", response_model=DispatchResponse)
def get_dispatch(
    dispatch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    获取单个调度详情
    只有教育局管理员可以查看调度
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    return dispatch


@router.post("/", response_model=DispatchResponse)
def create_dispatch(
    dispatch_data: DispatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    创建新调度
    只有教育局管理员可以创建调度
    """
    # 检查调度编码是否已存在
    if dispatch_data.dispatch_code:
        existing_dispatch = db.query(Dispatch).filter(
            Dispatch.dispatch_code == dispatch_data.dispatch_code
        ).first()
        if existing_dispatch:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="调度编码已存在"
            )
    
    # 设置调度人为当前用户
    dispatch_data.dispatcher_id = current_user.id
    
    # 创建调度
    new_dispatch = Dispatch(**dispatch_data.model_dump())
    
    db.add(new_dispatch)
    db.commit()
    db.refresh(new_dispatch)
    
    return new_dispatch


@router.put("/{dispatch_id}", response_model=DispatchResponse)
def update_dispatch(
    dispatch_id: int,
    dispatch_data: DispatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    更新调度信息
    只有教育局管理员可以更新调度
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    # 更新调度信息
    update_data = dispatch_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dispatch, key, value)
    
    db.commit()
    db.refresh(dispatch)
    
    return dispatch


@router.delete("/{dispatch_id}")
def delete_dispatch(
    dispatch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    删除调度
    只有教育局管理员可以删除调度
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    # 只能删除待执行的调度
    if dispatch.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能删除待执行的调度"
        )
    
    db.delete(dispatch)
    db.commit()
    
    return {"message": "调度删除成功"}


@router.put("/{dispatch_id}/start")
def start_dispatch(
    dispatch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    开始执行调度
    只有教育局管理员可以操作
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    if dispatch.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能从待执行状态开始调度"
        )
    
    dispatch.status = "in_progress"
    db.commit()
    
    return {"message": "调度已开始执行"}


@router.put("/{dispatch_id}/complete")
def complete_dispatch(
    dispatch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    完成调度
    只有教育局管理员可以操作
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    if dispatch.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能完成执行中的调度"
        )
    
    dispatch.status = "completed"
    db.commit()
    
    return {"message": "调度已完成"}


@router.put("/{dispatch_id}/cancel")
def cancel_dispatch(
    dispatch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    取消调度
    只有教育局管理员可以操作
    """
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度不存在"
        )
    
    if dispatch.status not in ["pending", "in_progress"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能取消待执行或执行中的调度"
        )
    
    dispatch.status = "cancelled"
    db.commit()
    
    return {"message": "调度已取消"}


@router.get("/stats/overview")
def get_dispatch_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    获取调度统计信息
    只有教育局管理员可以查看
    """
    query = db.query(Dispatch)
    
    # 统计各状态调度数量
    total = query.count()
    pending = query.filter(Dispatch.status == "pending").count()
    in_progress = query.filter(Dispatch.status == "in_progress").count()
    completed = query.filter(Dispatch.status == "completed").count()
    cancelled = query.filter(Dispatch.status == "cancelled").count()
    
    # 按类型统计
    type_stats = {}
    for dispatch in query.all():
        dt = dispatch.dispatch_type
        if dt not in type_stats:
            type_stats[dt] = 0
        type_stats[dt] += 1
    
    stats = {
        "total": total,
        "by_status": {
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "cancelled": cancelled
        },
        "by_type": type_stats
    }
    
    return stats
