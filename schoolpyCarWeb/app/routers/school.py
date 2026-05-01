"""
学校管理路由模块
处理学校的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.school import School
from app.models.user import User
from app.schemas.school import SchoolCreate, SchoolResponse, SchoolUpdate
from app.routers.auth import get_current_user, get_current_user_with_permission
from app.config import ROLES

router = APIRouter(prefix="/api/schools", tags=["学校管理"])


@router.get("/", response_model=List[SchoolResponse])
def get_schools(
    skip: int = 0,
    limit: int = 100,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学校列表
    教育局管理员可以查看所有学校，学校管理员只能查看本校
    """
    query = db.query(School)
    
    # 权限控制：学校管理员只能看本校
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(School.id == current_user.school_id)
    
    # 关键词搜索
    if keyword:
        query = query.filter(
            (School.school_name.contains(keyword)) |
            (School.school_code.contains(keyword))
        )
    
    # 分页
    schools = query.offset(skip).limit(limit).all()
    return schools


@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个学校详情
    """
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 权限控制：学校管理员只能查看本校
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if school.id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校信息"
            )
    
    return school


@router.post("/", response_model=SchoolResponse)
def create_school(
    school_data: SchoolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    创建新学校
    只有教育局管理员可以创建学校
    """
    # 检查学校编码是否已存在
    existing_school = db.query(School).filter(
        School.school_code == school_data.school_code
    ).first()
    if existing_school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="学校编码已存在"
        )
    
    # 创建学校
    new_school = School(
        school_name=school_data.school_name,
        school_code=school_data.school_code,
        address=school_data.address,
        principal=school_data.principal,
        contact_phone=school_data.contact_phone,
        description=school_data.description
    )
    
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    
    return new_school


@router.put("/{school_id}", response_model=SchoolResponse)
def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新学校信息
    教育局管理员可以更新所有学校，学校管理员只能更新本校
    """
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if school.id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校信息"
            )
    
    # 更新学校信息
    update_data = school_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(school, key, value)
    
    db.commit()
    db.refresh(school)
    
    return school


@router.delete("/{school_id}")
def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    删除学校
    只有教育局管理员可以删除学校
    """
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 检查是否有关联数据
    # 这里简单处理，实际应用中可能需要级联删除或迁移数据
    if school.admins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学校存在管理员用户，无法删除"
        )
    
    db.delete(school)
    db.commit()
    
    return {"message": "学校删除成功"}


@router.get("/{school_id}/stats")
def get_school_stats(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学校统计信息
    包括车辆数、司机数、学生数、路线数等
    """
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学校不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if school.id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
    
    # 统计数据
    from app.models.vehicle import Vehicle
    from app.models.driver import Driver
    from app.models.student import Student
    from app.models.route import Route
    
    stats = {
        "school_id": school.id,
        "school_name": school.school_name,
        "vehicle_count": db.query(Vehicle).filter(Vehicle.school_id == school_id).count(),
        "driver_count": db.query(Driver).filter(Driver.school_id == school_id).count(),
        "student_count": db.query(Student).filter(Student.school_id == school_id).count(),
        "route_count": db.query(Route).filter(Route.school_id == school_id).count(),
    }
    
    return stats
