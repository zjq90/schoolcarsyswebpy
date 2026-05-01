"""
紧急状况数据模型
=================

包含紧急状况相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class EmergencyCreate(BaseModel):
    """
    紧急状况创建模型

    Attributes:
        vehicle_id: 车辆ID
        emergency_type: 紧急类型：1-车辆故障，2-交通事故，3-学生突发状况，4-其他
        title: 紧急情况标题
        content: 紧急情况描述
        latitude: 发生位置纬度
        longitude: 发生位置经度
        location_address: 发生位置地址
        images: 图片URL列表
    """

    vehicle_id: int = Field(..., description="车辆ID")
    emergency_type: int = Field(4, description="紧急类型: 1-车辆故障, 2-交通事故, 3-学生突发状况, 4-其他")
    title: str = Field(..., max_length=200, description="紧急情况标题")
    content: str = Field(..., description="紧急情况描述")
    latitude: Optional[float] = Field(None, description="发生位置纬度")
    longitude: Optional[float] = Field(None, description="发生位置经度")
    location_address: Optional[str] = Field(None, max_length=200, description="发生位置地址")
    images: Optional[list[str]] = Field(None, description="图片URL列表")


class EmergencyUpdate(BaseModel):
    """
    紧急状况更新模型

    Attributes:
        status: 状态：1-待处理，2-处理中，3-已处理，4-已关闭
        handler_remark: 处理备注
    """

    status: Optional[int] = Field(None, description="状态")
    handler_remark: Optional[str] = Field(None, description="处理备注")


class EmergencyResponse(BaseModel):
    """
    紧急状况响应模型

    Attributes:
        id: 申请ID
        driver_id: 司机ID
        vehicle_id: 车辆ID
        emergency_type: 紧急类型
        title: 紧急情况标题
        content: 紧急情况描述
        latitude: 发生位置纬度
        longitude: 发生位置经度
        location_address: 发生位置地址
        images: 图片URL列表
        status: 状态
        handler_id: 处理人ID
        handler_remark: 处理备注
        handle_time: 处理时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="申请ID")
    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    emergency_type: int = Field(..., description="紧急类型")
    title: str = Field(..., description="紧急情况标题")
    content: str = Field(..., description="紧急情况描述")
    latitude: Optional[float] = Field(None, description="发生位置纬度")
    longitude: Optional[float] = Field(None, description="发生位置经度")
    location_address: Optional[str] = Field(None, description="发生位置地址")
    images: Optional[list[str]] = Field(None, description="图片URL列表")
    status: int = Field(..., description="状态")
    handler_id: Optional[int] = Field(None, description="处理人ID")
    handler_remark: Optional[str] = Field(None, description="处理备注")
    handle_time: Optional[datetime] = Field(None, description="处理时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "EmergencyCreate",
    "EmergencyUpdate",
    "EmergencyResponse",
]
