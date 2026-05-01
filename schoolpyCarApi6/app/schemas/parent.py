"""
家长数据模型
=============

包含家长相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class ParentCreate(BaseModel):
    """
    家长创建模型

    Attributes:
        real_name: 真实姓名
        id_card: 身份证号
        address: 家庭地址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
    """

    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    address: Optional[str] = Field(None, max_length=200, description="家庭地址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")


class ParentUpdate(BaseModel):
    """
    家长更新模型

    Attributes:
        real_name: 真实姓名
        id_card: 身份证号
        address: 家庭地址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
    """

    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    address: Optional[str] = Field(None, max_length=200, description="家庭地址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")


class ParentResponse(BaseModel):
    """
    家长响应模型

    Attributes:
        id: 家长ID
        user_id: 用户ID
        real_name: 真实姓名
        id_card: 身份证号
        address: 家庭地址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="家长ID")
    user_id: int = Field(..., description="用户ID")
    real_name: Optional[str] = Field(None, description="真实姓名")
    id_card: Optional[str] = Field(None, description="身份证号")
    address: Optional[str] = Field(None, description="家庭地址")
    emergency_contact: Optional[str] = Field(None, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, description="紧急联系电话")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class StudentBindRequest(BaseModel):
    """
    学生绑定请求模型

    Attributes:
        student_no: 学号
        real_name: 学生姓名
        relation: 与学生的关系
    """

    student_no: Optional[str] = Field(None, description="学号")
    real_name: str = Field(..., description="学生姓名")
    relation: str = Field(..., description="与学生的关系: 父亲/母亲/其他")


__all__ = [
    "ParentCreate",
    "ParentUpdate",
    "ParentResponse",
    "StudentBindRequest",
]
