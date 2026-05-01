"""
调度消息数据模型
=================

包含调度消息相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DispatchCreate(BaseModel):
    """
    调度消息创建模型

    Attributes:
        driver_id: 司机ID
        vehicle_id: 车辆ID
        route_id: 路线ID
        title: 调度标题
        content: 调度内容
        dispatch_time: 调度时间
        estimated_arrival_time: 预计到达时间
    """

    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    route_id: Optional[int] = Field(None, description="路线ID")
    title: str = Field(..., max_length=200, description="调度标题")
    content: str = Field(..., description="调度内容")
    dispatch_time: datetime = Field(..., description="调度时间")
    estimated_arrival_time: Optional[datetime] = Field(None, description="预计到达时间")


class DispatchUpdate(BaseModel):
    """
    调度消息更新模型

    Attributes:
        status: 状态：1-待接收，2-已接收，3-执行中，4-已完成，5-已取消
        actual_arrival_time: 实际到达时间
        remark: 备注
    """

    status: Optional[int] = Field(None, description="状态: 1-待接收, 2-已接收, 3-执行中, 4-已完成, 5-已取消")
    actual_arrival_time: Optional[datetime] = Field(None, description="实际到达时间")
    remark: Optional[str] = Field(None, description="备注")


class DispatchResponse(BaseModel):
    """
    调度消息响应模型

    Attributes:
        id: 调度ID
        driver_id: 司机ID
        vehicle_id: 车辆ID
        route_id: 路线ID
        route_name: 路线名称
        title: 调度标题
        content: 调度内容
        dispatch_time: 调度时间
        estimated_arrival_time: 预计到达时间
        actual_arrival_time: 实际到达时间
        status: 状态
        dispatcher_id: 调度人ID
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="调度ID")
    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    route_id: Optional[int] = Field(None, description="路线ID")
    route_name: Optional[str] = Field(None, description="路线名称")
    title: str = Field(..., description="调度标题")
    content: str = Field(..., description="调度内容")
    dispatch_time: datetime = Field(..., description="调度时间")
    estimated_arrival_time: Optional[datetime] = Field(None, description="预计到达时间")
    actual_arrival_time: Optional[datetime] = Field(None, description="实际到达时间")
    status: int = Field(..., description="状态")
    dispatcher_id: Optional[int] = Field(None, description="调度人ID")
    remark: Optional[str] = Field(None, description="备注")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "DispatchCreate",
    "DispatchUpdate",
    "DispatchResponse",
]
