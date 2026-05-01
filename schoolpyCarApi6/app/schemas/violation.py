"""
违章记录数据模型
=================

包含违章记录相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ViolationCreate(BaseModel):
    """
    违章记录创建模型

    Attributes:
        driver_id: 司机ID
        vehicle_id: 车辆ID
        violation_no: 违章编号
        violation_type: 违章类型：1-超速，2-闯红灯，3-违规停车，4-其他
        violation_time: 违章时间
        violation_address: 违章地点
        latitude: 违章地点纬度
        longitude: 违章地点经度
        description: 违章描述
        fine_amount: 罚款金额（分）
        deduct_points: 扣分
    """

    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    violation_no: Optional[str] = Field(None, max_length=50, description="违章编号")
    violation_type: int = Field(4, description="违章类型: 1-超速, 2-闯红灯, 3-违规停车, 4-其他")
    violation_time: datetime = Field(..., description="违章时间")
    violation_address: str = Field(..., max_length=200, description="违章地点")
    latitude: Optional[float] = Field(None, description="违章地点纬度")
    longitude: Optional[float] = Field(None, description="违章地点经度")
    description: Optional[str] = Field(None, description="违章描述")
    fine_amount: int = Field(0, description="罚款金额(分)")
    deduct_points: int = Field(0, description="扣分")


class ViolationUpdate(BaseModel):
    """
    违章记录更新模型

    Attributes:
        status: 状态：1-未处理，2-已处理，3-已申诉
        handle_time: 处理时间
        remark: 备注
    """

    status: Optional[int] = Field(None, description="状态: 1-未处理, 2-已处理, 3-已申诉")
    handle_time: Optional[datetime] = Field(None, description="处理时间")
    remark: Optional[str] = Field(None, description="备注")


class ViolationResponse(BaseModel):
    """
    违章记录响应模型

    Attributes:
        id: 违章ID
        driver_id: 司机ID
        vehicle_id: 车辆ID
        violation_no: 违章编号
        violation_type: 违章类型
        violation_time: 违章时间
        violation_address: 违章地点
        latitude: 违章地点纬度
        longitude: 违章地点经度
        description: 违章描述
        fine_amount: 罚款金额（分）
        deduct_points: 扣分
        status: 状态
        handle_time: 处理时间
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="违章ID")
    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    violation_no: Optional[str] = Field(None, description="违章编号")
    violation_type: int = Field(..., description="违章类型")
    violation_time: datetime = Field(..., description="违章时间")
    violation_address: str = Field(..., description="违章地点")
    latitude: Optional[float] = Field(None, description="违章地点纬度")
    longitude: Optional[float] = Field(None, description="违章地点经度")
    description: Optional[str] = Field(None, description="违章描述")
    fine_amount: int = Field(..., description="罚款金额(分)")
    deduct_points: int = Field(..., description="扣分")
    status: int = Field(..., description="状态")
    handle_time: Optional[datetime] = Field(None, description="处理时间")
    remark: Optional[str] = Field(None, description="备注")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "ViolationCreate",
    "ViolationUpdate",
    "ViolationResponse",
]
