"""
认证路由模块
处理用户登录、获取当前用户等认证相关功能
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserResponse
from app.utils.security import verify_password, create_access_token, decode_access_token
from app.config import ROLES

router = APIRouter(prefix="/api/auth", tags=["认证管理"])

# OAuth2密码Bearer认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    从JWT令牌中解析用户信息并查询数据库
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    return user


def get_current_user_with_permission(
    required_roles: Optional[list] = None,
    required_permissions: Optional[list] = None
):
    """
    获取当前用户并检查权限
    可以指定需要的角色或权限
    """
    def dependency(
        current_user: User = Depends(get_current_user)
    ) -> User:
        # 检查角色
        if required_roles:
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足：需要指定角色"
                )
        return current_user
    return dependency


@router.post("/login", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    使用OAuth2密码模式，返回JWT访问令牌
    """
    # 查询用户
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 验证用户存在和密码正确
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否启用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    # 更新最后登录时间
    user.last_login = datetime.now()
    db.commit()
    
    # 创建访问令牌
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "school_id": user.school_id
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "role": user.role,
            "school_id": user.school_id
        }
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户信息
    """
    return current_user


@router.get("/check-role/{role}")
def check_user_role(
    role: str,
    current_user: User = Depends(get_current_user)
):
    """
    检查当前用户是否具有指定角色
    """
    has_role = current_user.role == role
    return {
        "has_role": has_role,
        "current_role": current_user.role
    }
