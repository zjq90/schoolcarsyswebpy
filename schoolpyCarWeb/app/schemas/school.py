"""
学校Pydantic模式定义
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SchoolBase(BaseModel):
    """
    学校基础模式
    """
    school_name: str
    school_code: str
    address: Optional[str] = None
    principal: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


class SchoolCreate(SchoolBase):
    """
    学校创建模式
    """
    pass


class SchoolUpdate(BaseModel):
    """
    学校更新模式
    """
    school_name: Optional[str] = None
    school_code: Optional[str] = None
    address: Optional[str] = None
    principal: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


class SchoolResponse(SchoolBase):
    """
    学校响应模式
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
