"""
投诉数据模型
=============

包含投诉相关的请求和响应模型。
"""

from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ComplaintCreate(BaseModel):
    """
    投诉创建模型

    Attributes:
        student_id: 学生ID
        title: 投诉标题
        content: 投诉内容
        images: 图片URL列表
        complaint_type: 投诉类型：1-司机服务，2-车辆问题，3-路线问题，4-其他
    """

    student_id: Optional[int] = Field(None, description="学生ID")
    title: str = Field(..., max_length=200, description="投诉标题")
    content: str = Field(..., description="投诉内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    complaint_type: int = Field(4, description="投诉类型: 1-司机服务, 2-车辆问题, 3-路线问题, 4-其他")


class ComplaintUpdate(BaseModel):
    """
    投诉更新模型

    Attributes:
        status: 状态：1-待处理，2-处理中，3-已处理，4-已关闭
        handler_remark: 处理备注
    """

    status: Optional[int] = Field(None, description="状态")
    handler_remark: Optional[str] = Field(None, description="处理备注")


class ComplaintResponse(BaseModel):
    """
    投诉响应模型

    Attributes:
        id: 投诉ID
        parent_id: 家长ID
        student_id: 学生ID
        student_name: 学生姓名
        title: 投诉标题
        content: 投诉内容
        images: 图片URL列表
        complaint_type: 投诉类型
        status: 状态
        handler_id: 处理人ID
        handler_remark: 处理备注
        handle_time: 处理时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="投诉ID")
    parent_id: int = Field(..., description="家长ID")
    student_id: Optional[int] = Field(None, description="学生ID")
    student_name: Optional[str] = Field(None, description="学生姓名")
    title: str = Field(..., description="投诉标题")
    content: str = Field(..., description="投诉内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    complaint_type: int = Field(..., description="投诉类型")
    status: int = Field(..., description="状态")
    handler_id: Optional[int] = Field(None, description="处理人ID")
    handler_remark: Optional[str] = Field(None, description="处理备注")
    handle_time: Optional[datetime] = Field(None, description="处理时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "ComplaintCreate",
    "ComplaintUpdate",
    "ComplaintResponse",
]
