from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import StudentBehavior, StudentBehaviorType, User
from schemas import StudentBehaviorCreate, StudentBehaviorUpdate, StudentBehaviorResponse
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/student-behaviors", tags=["学生行为检测"])


@router.get("/", response_model=List[StudentBehaviorResponse])
async def get_student_behaviors(
    skip: int = 0,
    limit: int = 100,
    behavior_type: str = None,
    is_handled: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(StudentBehavior)
    if behavior_type:
        query = query.filter(StudentBehavior.behavior_type == behavior_type)
    if is_handled is not None:
        query = query.filter(StudentBehavior.is_handled == is_handled)
    behaviors = query.order_by(StudentBehavior.created_at.desc()).offset(skip).limit(limit).all()
    return behaviors


@router.get("/{behavior_id}", response_model=StudentBehaviorResponse)
async def get_student_behavior(
    behavior_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    behavior = db.query(StudentBehavior).filter(StudentBehavior.id == behavior_id).first()
    if behavior is None:
        raise HTTPException(status_code=404, detail="行为记录不存在")
    return behavior


@router.post("/", response_model=StudentBehaviorResponse, status_code=status.HTTP_201_CREATED)
async def create_student_behavior(
    behavior_data: StudentBehaviorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_behavior = StudentBehavior(**behavior_data.model_dump())
    db.add(new_behavior)
    db.commit()
    db.refresh(new_behavior)
    return new_behavior


@router.put("/{behavior_id}", response_model=StudentBehaviorResponse)
async def update_student_behavior(
    behavior_id: int,
    behavior_data: StudentBehaviorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    behavior = db.query(StudentBehavior).filter(StudentBehavior.id == behavior_id).first()
    if behavior is None:
        raise HTTPException(status_code=404, detail="行为记录不存在")
    update_data = behavior_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(behavior, key, value)
    if behavior_data.is_handled:
        behavior.handled_by = current_user.id
        behavior.handled_at = datetime.utcnow()
    db.commit()
    db.refresh(behavior)
    return behavior


@router.delete("/{behavior_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_behavior(
    behavior_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    behavior = db.query(StudentBehavior).filter(StudentBehavior.id == behavior_id).first()
    if behavior is None:
        raise HTTPException(status_code=404, detail="行为记录不存在")
    db.delete(behavior)
    db.commit()


@router.get("/statistics/overview")
async def get_student_behavior_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total = db.query(StudentBehavior).count()
    unhandled = db.query(StudentBehavior).filter(StudentBehavior.is_handled == 0).count()
    by_type = {}
    for behavior_type in StudentBehaviorType:
        count = db.query(StudentBehavior).filter(StudentBehavior.behavior_type == behavior_type).count()
        by_type[behavior_type.value] = count
    return {
        "total": total,
        "unhandled": unhandled,
        "by_type": by_type
    }
