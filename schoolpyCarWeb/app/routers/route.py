"""
路线管理路由模块
处理路线的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.route import Route
from app.models.user import User
from app.schemas.route import RouteCreate, RouteResponse, RouteUpdate
from app.routers.auth import get_current_user
from app.config import ROLES

router = APIRouter(prefix="/api/routes", tags=["路线管理"])


@router.get("/", response_model=List[RouteResponse])
def get_routes(
    skip: int = 0,
    limit: int = 100,
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取路线列表
    教育局管理员可以查看所有路线，学校管理员只能查看本校路线
    """
    query = db.query(Route)
    
    # 权限控制：学校管理员只能看本校路线
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Route.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Route.school_id == school_id)
    
    # 状态过滤
    if status:
        query = query.filter(Route.status == status)
    
    # 关键词搜索（路线名称、路线编码）
    if keyword:
        query = query.filter(
            (Route.route_name.contains(keyword)) |
            (Route.route_code.contains(keyword))
        )
    
    # 分页
    routes = query.offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个路线详情
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="路线不存在"
        )
    
    # 权限控制：学校管理员只能查看本校路线
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if route.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校的路线"
            )
    
    return route


@router.post("/", response_model=RouteResponse)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新路线
    教育局管理员可以创建任意学校的路线，学校管理员只能创建本校路线
    """
    # 权限控制：学校管理员只能创建本校路线
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if route_data.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：只能创建本校的路线"
            )
    
    # 检查路线编码是否已存在
    if route_data.route_code:
        existing_route = db.query(Route).filter(
            Route.route_code == route_data.route_code
        ).first()
        if existing_route:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="路线编码已存在"
            )
    
    # 创建路线
    new_route = Route(**route_data.model_dump())
    
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    
    return new_route


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    route_data: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新路线信息
    教育局管理员可以更新所有路线，学校管理员只能更新本校路线
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="路线不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if route.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校的路线"
            )
    
    # 更新路线信息
    update_data = route_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(route, key, value)
    
    db.commit()
    db.refresh(route)
    
    return route


@router.delete("/{route_id}")
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除路线
    教育局管理员可以删除任意路线，学校管理员只能删除本校路线
    """
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="路线不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if route.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法删除其他学校的路线"
            )
    
    db.delete(route)
    db.commit()
    
    return {"message": "路线删除成功"}


@router.get("/stats/overview")
def get_route_stats(
    school_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取路线统计信息
    """
    query = db.query(Route)
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Route.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Route.school_id == school_id)
    
    # 统计各状态路线数量
    total = query.count()
    active = query.filter(Route.status == "active").count()
    inactive = query.filter(Route.status == "inactive").count()
    
    stats = {
        "total": total,
        "by_status": {
            "active": active,
            "inactive": inactive
        }
    }
    
    return stats
