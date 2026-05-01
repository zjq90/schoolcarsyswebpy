"""
反馈数据模型
=============

包含反馈相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class FeedbackCreate(BaseModel):
    """
    反馈创建模型

    Attributes:
        vehicle_id: 车辆ID
        feedback_type: 反馈类型：1-处理结果反馈，2-车辆保养反馈
        title: 反馈标题
        content: 反馈内容
        images: 图片URL列表
        related_message_id: 关联消息ID
    """

    vehicle_id: Optional[int] = Field(None, description="车辆ID")
    feedback_type: int = Field(..., description="反馈类型: 1-处理结果反馈, 2-车辆保养反馈")
    title: str = Field(..., max_length=200, description="反馈标题")
    content: str = Field(..., description="反馈内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    related_message_id: Optional[int] = Field(None, description="关联消息ID")


class FeedbackUpdate(BaseModel):
    """
    反馈更新模型

    Attributes:
        status: 状态：1-待审核，2-已通过，3-已驳回
        reviewer_remark: 审核备注
    """

    status: Optional[int] = Field(None, description="状态")
    reviewer_remark: Optional[str] = Field(None, description="审核备注")


class FeedbackResponse(BaseModel):
    """
    反馈响应模型

    Attributes:
        id: 反馈ID
        driver_id: 司机ID
        vehicle_id: 车辆ID
        feedback_type: 反馈类型
        title: 反馈标题
        content: 反馈内容
        images: 图片URL列表
        related_message_id: 关联消息ID
        status: 状态
        reviewer_id: 审核人ID
        reviewer_remark: 审核备注
        review_time: 审核时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="反馈ID")
    driver_id: int = Field(..., description="司机ID")
    vehicle_id: Optional[int] = Field(None, description="车辆ID")
    feedback_type: int = Field(..., description="反馈类型")
    title: str = Field(..., description="反馈标题")
    content: str = Field(..., description="反馈内容")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    related_message_id: Optional[int] = Field(None, description="关联消息ID")
    status: int = Field(..., description="状态")
    reviewer_id: Optional[int] = Field(None, description="审核人ID")
    reviewer_remark: Optional[str] = Field(None, description="审核备注")
    review_time: Optional[datetime] = Field(None, description="审核时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "FeedbackCreate",
    "FeedbackUpdate",
    "FeedbackResponse",
]
