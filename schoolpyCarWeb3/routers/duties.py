from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, date

from database import get_db
from models import Duty, DutyStatus, DutyChangeType, User
from schemas import DutyCreate, DutyUpdate, DutyResponse, DutyChangeRequest
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/duties", tags=["值班管理"])


@router.get("/", response_model=List[DutyResponse])
async def get_duties(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    duty_date: date = None,
    driver_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Duty)
    if status:
        query = query.filter(Duty.status == status)
    if duty_date:
        query = query.filter(Duty.duty_date == duty_date)
    if driver_id:
        query = query.filter(Duty.driver_id == driver_id)
    duties = query.order_by(Duty.duty_date.desc(), Duty.start_time.desc()).offset(skip).limit(limit).all()
    return duties


@router.get("/{duty_id}", response_model=DutyResponse)
async def get_duty(
    duty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if duty is None:
        raise HTTPException(status_code=404, detail="值班记录不存在")
    return duty


@router.post("/", response_model=DutyResponse, status_code=status.HTTP_201_CREATED)
async def create_duty(
    duty_data: DutyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_duty = Duty(**duty_data.model_dump())
    if not new_duty.assigned_by:
        new_duty.assigned_by = current_user.id
    db.add(new_duty)
    db.commit()
    db.refresh(new_duty)
    return new_duty


@router.put("/{duty_id}", response_model=DutyResponse)
async def update_duty(
    duty_id: int,
    duty_data: DutyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if duty is None:
        raise HTTPException(status_code=404, detail="值班记录不存在")
    update_data = duty_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(duty, key, value)
    db.commit()
    db.refresh(duty)
    return duty


@router.delete("/{duty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_duty(
    duty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if duty is None:
        raise HTTPException(status_code=404, detail="值班记录不存在")
    db.delete(duty)
    db.commit()


@router.post("/{duty_id}/change", response_model=DutyResponse)
async def change_duty(
    duty_id: int,
    change_data: DutyChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if duty is None:
        raise HTTPException(status_code=404, detail="值班记录不存在")
    duty.is_changed = 1
    duty.change_type = change_data.change_type
    duty.change_reason = change_data.change_reason
    duty.changed_by = current_user.id
    duty.changed_at = datetime.utcnow()
    if change_data.new_driver_id:
        duty.original_driver_id = duty.driver_id
        duty.driver_id = change_data.new_driver_id
    if change_data.new_bus_id:
        duty.original_bus_id = duty.bus_id
        duty.bus_id = change_data.new_bus_id
    if change_data.new_route_id:
        duty.original_route_id = duty.route_id
        duty.route_id = change_data.new_route_id
    duty.status = DutyStatus.CHANGED
    db.commit()
    db.refresh(duty)
    return duty


@router.get("/today/summary")
async def get_today_duty_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    today = date.today()
    total = db.query(Duty).filter(Duty.duty_date == today).count()
    scheduled = db.query(Duty).filter(Duty.duty_date == today, Duty.status == DutyStatus.SCHEDULED).count()
    active = db.query(Duty).filter(Duty.duty_date == today, Duty.status == DutyStatus.ACTIVE).count()
    completed = db.query(Duty).filter(Duty.duty_date == today, Duty.status == DutyStatus.COMPLETED).count()
    changed = db.query(Duty).filter(Duty.duty_date == today, Duty.status == DutyStatus.CHANGED).count()
    return {
        "date": today.isoformat(),
        "total": total,
        "scheduled": scheduled,
        "active": active,
        "completed": completed,
        "changed": changed
    }
