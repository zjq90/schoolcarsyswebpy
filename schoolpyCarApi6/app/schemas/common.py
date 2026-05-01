"""
通用数据模型
=============

包含通用的请求和响应模型。
"""

from typing import Generic, List, Optional, TypeVar, Any
from pydantic import BaseModel, Field
from datetime import datetime


DataT = TypeVar("DataT")


class CommonResponse(BaseModel, Generic[DataT]):
    """
    通用响应模型

    Attributes:
        code: 状态码，200表示成功
        message: 响应消息
        data: 响应数据
    """

    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Optional[DataT] = Field(None, description="响应数据")


class PaginationParams(BaseModel):
    """
    分页参数模型

    Attributes:
        page: 页码，从1开始
        page_size: 每页数量
    """

    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class PaginatedResponse(BaseModel, Generic[DataT]):
    """
    分页响应模型

    Attributes:
        items: 数据列表
        total: 总数
        page: 当前页码
        page_size: 每页数量
        total_pages: 总页数
    """

    items: List[DataT] = Field(..., description="数据列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")


class LoginRequest(BaseModel):
    """登录请求基础模型"""

    phone: str = Field(..., description="手机号")


class UserLogin(LoginRequest):
    """
    密码登录请求模型

    Attributes:
        phone: 手机号
        password: 密码
    """

    password: str = Field(..., description="密码")


class UserLoginByCode(LoginRequest):
    """
    验证码登录请求模型

    Attributes:
        phone: 手机号
        code: 验证码
    """

    code: str = Field(..., description="验证码")


class Token(BaseModel):
    """
    Token响应模型

    Attributes:
        access_token: 访问令牌
        token_type: 令牌类型
        expires_in: 过期时间（秒）
    """

    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")


class TokenData(BaseModel):
    """
    Token数据模型

    Attributes:
        user_id: 用户ID
        phone: 手机号
        user_type: 用户类型
    """

    user_id: Optional[int] = None
    phone: Optional[str] = None
    user_type: Optional[str] = None
