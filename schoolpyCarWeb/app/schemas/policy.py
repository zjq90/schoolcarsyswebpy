"""
政策Pydantic模式定义
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class PolicyBase(BaseModel):
    """
    政策基础模式
    """
    policy_code: str
    title: str
    content: str
    policy_type: str = "notice"
    publisher_id: int
    publish_date: Optional[date] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    is_published: bool = False
    is_top: bool = False
    attachment_path: Optional[str] = None
    view_count: int = 0
    status: str = "draft"
    remarks: Optional[str] = None


class PolicyCreate(PolicyBase):
    """
    政策创建模式
    """
    pass


class PolicyUpdate(BaseModel):
    """
    政策更新模式
    """
    policy_code: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    policy_type: Optional[str] = None
    publisher_id: Optional[int] = None
    publish_date: Optional[date] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    is_published: Optional[bool] = None
    is_top: Optional[bool] = None
    attachment_path: Optional[str] = None
    view_count: Optional[int] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class PolicyResponse(PolicyBase):
    """
    政策响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
