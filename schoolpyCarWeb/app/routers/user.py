"""
用户管理路由模块
处理用户的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.school import School
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.security import get_password_hash
from app.routers.auth import get_current_user, get_current_user_with_permission
from app.config import ROLES

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    school_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户列表
    教育局管理员可以查看所有用户，学校管理员只能查看本校用户
    """
    query = db.query(User)
    
    # 权限控制：学校管理员只能看本校用户
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(User.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(User.school_id == school_id)
    
    # 角色过滤
    if role:
        query = query.filter(User.role == role)
    
    # 分页
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个用户详情
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 权限控制：学校管理员只能查看本校用户
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if user.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校的用户"
            )
    
    return user


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    创建新用户
    只有教育局管理员可以创建用户
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 加密密码
    hashed_password = get_password_hash(user_data.password)
    
    # 创建用户
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        real_name=user_data.real_name,
        role=user_data.role,
        phone=user_data.phone,
        email=user_data.email,
        school_id=user_data.school_id,
        is_active=user_data.is_active
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新用户信息
    教育局管理员可以更新所有用户，学校管理员只能更新自己和本校用户
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        # 学校管理员只能修改自己或本校的学校管理员
        if user.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校的用户"
            )
        # 学校管理员不能修改角色（只能由教育局管理员修改）
        if user_data.role and user_data.role != user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改用户角色"
            )
    
    # 更新用户信息
    update_data = user_data.model_dump(exclude_unset=True)
    
    # 如果有密码，需要加密
    if "password" in update_data and update_data["password"]:
        update_data["password"] = get_password_hash(update_data["password"])
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    删除用户
    只有教育局管理员可以删除用户
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不能删除自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法删除自己的账户"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "用户删除成功"}


@router.put("/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    new_password: str = Query(..., description="新密码"),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    重置用户密码
    只有教育局管理员可以重置用户密码
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    user.password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "密码重置成功"}
