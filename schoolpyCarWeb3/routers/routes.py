from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from models import Route, RouteStatus, User
from schemas import RouteCreate, RouteUpdate, RouteResponse
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/routes", tags=["路线管理"])


@router.get("/", response_model=List[RouteResponse])
async def get_routes(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Route)
    if status:
        query = query.filter(Route.status == status)
    routes = query.offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="路线不存在")
    return route


@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_route = Route(**route_data.model_dump())
    if not new_route.route_code:
        new_route.route_code = f"RT{new_route.route_name[:3].upper()}{len(db.query(Route).all()) + 1:03d}"
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: int,
    route_data: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="路线不存在")
    update_data = route_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(route, key, value)
    db.commit()
    db.refresh(route)
    return route


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="路线不存在")
    db.delete(route)
    db.commit()


@router.post("/{route_id}/optimize", response_model=RouteResponse)
async def optimize_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="路线不存在")
    route.estimated_duration_min = max(route.estimated_duration_min - 5, 10)
    db.commit()
    db.refresh(route)
    return route
