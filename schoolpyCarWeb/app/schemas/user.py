"""
用户Pydantic模式定义
用于API请求和响应的数据验证
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    用户基础模式
    """
    username: str
    real_name: str
    role: str
    phone: Optional[str] = None
    email: Optional[str] = None
    school_id: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    """
    用户创建模式
    用于创建用户时的请求数据
    """
    password: str


class UserUpdate(BaseModel):
    """
    用户更新模式
    用于更新用户时的请求数据
    """
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    school_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    """
    用户登录模式
    用于登录时的请求数据
    """
    username: str
    password: str


class UserResponse(UserBase):
    """
    用户响应模式
    用于返回给前端的用户数据
    """
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
