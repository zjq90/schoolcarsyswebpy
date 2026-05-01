from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from models import Bus, BusStatus, User
from schemas import BusCreate, BusUpdate, BusResponse
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/buses", tags=["校车管理"])


@router.get("/", response_model=List[BusResponse])
async def get_buses(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Bus)
    if status:
        query = query.filter(Bus.status == status)
    buses = query.offset(skip).limit(limit).all()
    return buses


@router.get("/{bus_id}", response_model=BusResponse)
async def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail="校车不存在")
    return bus


@router.post("/", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
async def create_bus(
    bus_data: BusCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    existing_bus = db.query(Bus).filter(Bus.plate_number == bus_data.plate_number).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="车牌号已存在")
    new_bus = Bus(**bus_data.model_dump())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus


@router.put("/{bus_id}", response_model=BusResponse)
async def update_bus(
    bus_id: int,
    bus_data: BusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail="校车不存在")
    update_data = bus_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(bus, key, value)
    db.commit()
    db.refresh(bus)
    return bus


@router.delete("/{bus_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail="校车不存在")
    db.delete(bus)
    db.commit()


@router.put("/{bus_id}/status", response_model=BusResponse)
async def update_bus_status(
    bus_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if bus is None:
        raise HTTPException(status_code=404, detail="校车不存在")
    try:
        bus.status = BusStatus(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的状态值")
    db.commit()
    db.refresh(bus)
    return bus
