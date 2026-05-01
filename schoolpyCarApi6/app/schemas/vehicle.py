"""
车辆数据模型
=============

包含车辆相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class VehicleCreate(BaseModel):
    """
    车辆创建模型

    Attributes:
        plate_no: 车牌号
        vehicle_no: 车辆编号
        vehicle_type: 车辆类型
        brand: 品牌
        model: 型号
        color: 颜色
        seat_count: 座位数
        buy_date: 购买日期
        last_maintenance_date: 最后保养日期
        next_maintenance_date: 下次保养日期
        mileage: 行驶里程(公里)
    """

    plate_no: str = Field(..., max_length=20, description="车牌号")
    vehicle_no: Optional[str] = Field(None, max_length=20, description="车辆编号")
    vehicle_type: Optional[str] = Field(None, max_length=50, description="车辆类型")
    brand: Optional[str] = Field(None, max_length=50, description="品牌")
    model: Optional[str] = Field(None, max_length=50, description="型号")
    color: Optional[str] = Field(None, max_length=20, description="颜色")
    seat_count: Optional[int] = Field(None, description="座位数")
    buy_date: Optional[date] = Field(None, description="购买日期")
    last_maintenance_date: Optional[date] = Field(None, description="最后保养日期")
    next_maintenance_date: Optional[date] = Field(None, description="下次保养日期")
    mileage: int = Field(0, description="行驶里程(公里)")


class VehicleUpdate(BaseModel):
    """
    车辆更新模型

    Attributes:
        plate_no: 车牌号
        vehicle_no: 车辆编号
        vehicle_type: 车辆类型
        brand: 品牌
        model: 型号
        color: 颜色
        seat_count: 座位数
        buy_date: 购买日期
        last_maintenance_date: 最后保养日期
        next_maintenance_date: 下次保养日期
        mileage: 行驶里程(公里)
        status: 状态：1-可用，0-维修中，2-报废
    """

    plate_no: Optional[str] = Field(None, max_length=20, description="车牌号")
    vehicle_no: Optional[str] = Field(None, max_length=20, description="车辆编号")
    vehicle_type: Optional[str] = Field(None, max_length=50, description="车辆类型")
    brand: Optional[str] = Field(None, max_length=50, description="品牌")
    model: Optional[str] = Field(None, max_length=50, description="型号")
    color: Optional[str] = Field(None, max_length=20, description="颜色")
    seat_count: Optional[int] = Field(None, description="座位数")
    buy_date: Optional[date] = Field(None, description="购买日期")
    last_maintenance_date: Optional[date] = Field(None, description="最后保养日期")
    next_maintenance_date: Optional[date] = Field(None, description="下次保养日期")
    mileage: Optional[int] = Field(None, description="行驶里程(公里)")
    status: Optional[int] = Field(None, description="状态: 1-可用, 0-维修中, 2-报废")


class VehicleResponse(BaseModel):
    """
    车辆响应模型

    Attributes:
        id: 车辆ID
        plate_no: 车牌号
        vehicle_no: 车辆编号
        vehicle_type: 车辆类型
        brand: 品牌
        model: 型号
        color: 颜色
        seat_count: 座位数
        buy_date: 购买日期
        last_maintenance_date: 最后保养日期
        next_maintenance_date: 下次保养日期
        mileage: 行驶里程(公里)
        status: 状态：1-可用，0-维修中，2-报废
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="车辆ID")
    plate_no: str = Field(..., description="车牌号")
    vehicle_no: Optional[str] = Field(None, description="车辆编号")
    vehicle_type: Optional[str] = Field(None, description="车辆类型")
    brand: Optional[str] = Field(None, description="品牌")
    model: Optional[str] = Field(None, description="型号")
    color: Optional[str] = Field(None, description="颜色")
    seat_count: Optional[int] = Field(None, description="座位数")
    buy_date: Optional[date] = Field(None, description="购买日期")
    last_maintenance_date: Optional[date] = Field(None, description="最后保养日期")
    next_maintenance_date: Optional[date] = Field(None, description="下次保养日期")
    mileage: int = Field(..., description="行驶里程(公里)")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
]
