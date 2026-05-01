"""
用户路由
处理用户相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    status: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    获取用户列表
    支持分页、角色筛选、状态筛选
    """
    query = db.query(User).order_by(desc(User.created_at))
    
    if role:
        query = query.filter(User.role == role)
    if status is not None:
        query = query.filter(User.status == status)
    
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    获取单个用户详情
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    创建用户
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 简单的密码加密（实际项目中应该使用bcrypt等）
    import hashlib
    hashed_password = hashlib.md5(user.password.encode()).hexdigest()
    
    db_user = User(
        username=user.username,
        password=hashed_password,
        real_name=user.real_name,
        phone=user.phone,
        email=user.email,
        role=user.role,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # 如果有密码更新，需要加密
    if "password" in update_data and update_data["password"]:
        import hashlib
        update_data["password"] = hashlib.md5(update_data["password"].encode()).hexdigest()
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    删除用户
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不允许删除最后一个管理员
    if db_user.role == "admin":
        admin_count = db.query(User).filter(User.role == "admin", User.id != user_id).count()
        if admin_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除最后一个管理员"
            )
    
    db.delete(db_user)
    db.commit()
    
    return {"message": "删除成功", "user_id": user_id}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    用户登录
    """
    import hashlib
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    user = db.query(User).filter(
        User.username == username,
        User.password == hashed_password
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    return {
        "message": "登录成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "role": user.role
        }
    }
