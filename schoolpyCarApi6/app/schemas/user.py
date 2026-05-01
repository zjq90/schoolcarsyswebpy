"""
用户数据模型
=============

包含用户相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.common import (
    LoginRequest,
    Token,
    TokenData,
)


class UserLogin(LoginRequest):
    """
    密码登录请求模型

    Attributes:
        phone: 手机号
        password: 密码
    """

    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserLoginByPhone(LoginRequest):
    """
    手机号登录请求模型（别名）

    Attributes:
        phone: 手机号
        password: 密码
    """

    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserLoginByCode(LoginRequest):
    """
    验证码登录请求模型

    Attributes:
        phone: 手机号
        code: 验证码
    """

    code: str = Field(..., min_length=4, max_length=6, description="验证码")


class UserCreate(BaseModel):
    """
    用户创建模型

    Attributes:
        phone: 手机号
        password: 密码
        user_type: 用户类型
        nickname: 昵称
    """

    phone: str = Field(..., description="手机号")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    user_type: str = Field(..., description="用户类型: parent/driver/admin")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")


class UserUpdate(BaseModel):
    """
    用户更新模型

    Attributes:
        nickname: 昵称
        avatar: 头像URL
    """

    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")


class UserResponse(BaseModel):
    """
    用户响应模型

    Attributes:
        id: 用户ID
        phone: 手机号
        user_type: 用户类型
        nickname: 昵称
        avatar: 头像URL
        status: 状态
        last_login_time: 最后登录时间
        created_at: 创建时间
    """

    id: int = Field(..., description="用户ID")
    phone: str = Field(..., description="手机号")
    user_type: str = Field(..., description="用户类型")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    status: int = Field(..., description="状态")
    last_login_time: Optional[datetime] = Field(None, description="最后登录时间")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


__all__ = [
    "UserLogin",
    "UserLoginByPhone",
    "UserLoginByCode",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "Token",
    "TokenData",
]
