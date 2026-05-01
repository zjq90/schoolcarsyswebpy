from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import TrafficData, TrafficCondition, User
from schemas import TrafficDataCreate, TrafficDataUpdate, TrafficDataResponse
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/traffic", tags=["交通数据与避堵"])


@router.get("/", response_model=List[TrafficDataResponse])
async def get_traffic_data(
    skip: int = 0,
    limit: int = 100,
    route_id: int = None,
    condition: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(TrafficData)
    if route_id:
        query = query.filter(TrafficData.route_id == route_id)
    if condition:
        query = query.filter(TrafficData.condition == condition)
    traffic_data = query.order_by(TrafficData.created_at.desc()).offset(skip).limit(limit).all()
    return traffic_data


@router.get("/{traffic_id}", response_model=TrafficDataResponse)
async def get_traffic(
    traffic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    traffic = db.query(TrafficData).filter(TrafficData.id == traffic_id).first()
    if traffic is None:
        raise HTTPException(status_code=404, detail="交通数据不存在")
    return traffic


@router.post("/", response_model=TrafficDataResponse, status_code=status.HTTP_201_CREATED)
async def create_traffic_data(
    traffic_data: TrafficDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_traffic = TrafficData(**traffic_data.model_dump())
    db.add(new_traffic)
    db.commit()
    db.refresh(new_traffic)
    return new_traffic


@router.put("/{traffic_id}", response_model=TrafficDataResponse)
async def update_traffic_data(
    traffic_id: int,
    traffic_data: TrafficDataUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    traffic = db.query(TrafficData).filter(TrafficData.id == traffic_id).first()
    if traffic is None:
        raise HTTPException(status_code=404, detail="交通数据不存在")
    update_data = traffic_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(traffic, key, value)
    if traffic_data.is_sent_to_bus:
        traffic.sent_at = datetime.utcnow()
    db.commit()
    db.refresh(traffic)
    return traffic


@router.delete("/{traffic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_traffic_data(
    traffic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    traffic = db.query(TrafficData).filter(TrafficData.id == traffic_id).first()
    if traffic is None:
        raise HTTPException(status_code=404, detail="交通数据不存在")
    db.delete(traffic)
    db.commit()


@router.post("/{traffic_id}/send-to-bus", response_model=TrafficDataResponse)
async def send_traffic_to_bus(
    traffic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    traffic = db.query(TrafficData).filter(TrafficData.id == traffic_id).first()
    if traffic is None:
        raise HTTPException(status_code=404, detail="交通数据不存在")
    traffic.is_sent_to_bus = 1
    traffic.sent_at = datetime.utcnow()
    db.commit()
    db.refresh(traffic)
    return traffic


@router.get("/statistics/overview")
async def get_traffic_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total = db.query(TrafficData).count()
    by_condition = {}
    for condition in TrafficCondition:
        count = db.query(TrafficData).filter(TrafficData.condition == condition).count()
        by_condition[condition.value] = count
    avg_delay = db.query(TrafficData).with_entities(db.func.avg(TrafficData.delay_minutes)).scalar() or 0
    return {
        "total_records": total,
        "by_condition": by_condition,
        "average_delay_minutes": round(avg_delay, 2)
    }


@router.get("/routes/{route_id}/analysis")
async def analyze_route_traffic(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    traffic_data = db.query(TrafficData).filter(TrafficData.route_id == route_id).all()
    if not traffic_data:
        return {
            "route_id": route_id,
            "message": "该路线暂无交通数据",
            "recommended_action": "正常行驶"
        }
    total_delay = sum(t.delay_minutes for t in traffic_data)
    avg_delay = total_delay / len(traffic_data)
    worst_condition = max(traffic_data, key=lambda x: x.delay_minutes)
    if avg_delay > 30:
        recommended_action = "建议绕道行驶"
    elif avg_delay > 15:
        recommended_action = "建议提前出发"
    else:
        recommended_action = "正常行驶"
    return {
        "route_id": route_id,
        "total_data_points": len(traffic_data),
        "average_delay_minutes": round(avg_delay, 2),
        "worst_condition": {
            "location": worst_condition.location_name,
            "delay_minutes": worst_condition.delay_minutes,
            "condition": worst_condition.condition.value if worst_condition.condition else None
        },
        "recommended_action": recommended_action
    }
