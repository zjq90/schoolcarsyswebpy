"""
打卡记录数据模型
=================

包含打卡记录相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AttendanceCreate(BaseModel):
    """
    打卡记录创建模型

    Attributes:
        driver_id: 司机ID
        vehicle_id: 车辆ID
        attendance_date: 打卡日期
        check_in_time: 上班打卡时间
        check_in_latitude: 上班打卡纬度
        check_in_longitude: 上班打卡经度
        check_in_address: 上班打卡地址
    """

    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    attendance_date: datetime = Field(..., description="打卡日期")
    check_in_time: Optional[datetime] = Field(None, description="上班打卡时间")
    check_in_latitude: Optional[float] = Field(None, description="上班打卡纬度")
    check_in_longitude: Optional[float] = Field(None, description="上班打卡经度")
    check_in_address: Optional[str] = Field(None, max_length=200, description="上班打卡地址")


class AttendanceUpdate(BaseModel):
    """
    打卡记录更新模型

    Attributes:
        check_out_time: 下班打卡时间
        check_out_latitude: 下班打卡纬度
        check_out_longitude: 下班打卡经度
        check_out_address: 下班打卡地址
        status: 状态：1-正常，2-迟到，3-早退，4-缺勤
        remark: 备注
    """

    check_out_time: Optional[datetime] = Field(None, description="下班打卡时间")
    check_out_latitude: Optional[float] = Field(None, description="下班打卡纬度")
    check_out_longitude: Optional[float] = Field(None, description="下班打卡经度")
    check_out_address: Optional[str] = Field(None, max_length=200, description="下班打卡地址")
    status: Optional[int] = Field(None, description="状态: 1-正常, 2-迟到, 3-早退, 4-缺勤")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class AttendanceResponse(BaseModel):
    """
    打卡记录响应模型

    Attributes:
        id: 记录ID
        driver_id: 司机ID
        vehicle_id: 车辆ID
        attendance_date: 打卡日期
        check_in_time: 上班打卡时间
        check_in_latitude: 上班打卡纬度
        check_in_longitude: 上班打卡经度
        check_in_address: 上班打卡地址
        check_out_time: 下班打卡时间
        check_out_latitude: 下班打卡纬度
        check_out_longitude: 下班打卡经度
        check_out_address: 下班打卡地址
        status: 状态
        remark: 备注
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="记录ID")
    driver_id: int = Field(..., description="司机ID")
    vehicle_id: int = Field(..., description="车辆ID")
    attendance_date: datetime = Field(..., description="打卡日期")
    check_in_time: Optional[datetime] = Field(None, description="上班打卡时间")
    check_in_latitude: Optional[float] = Field(None, description="上班打卡纬度")
    check_in_longitude: Optional[float] = Field(None, description="上班打卡经度")
    check_in_address: Optional[str] = Field(None, description="上班打卡地址")
    check_out_time: Optional[datetime] = Field(None, description="下班打卡时间")
    check_out_latitude: Optional[float] = Field(None, description="下班打卡纬度")
    check_out_longitude: Optional[float] = Field(None, description="下班打卡经度")
    check_out_address: Optional[str] = Field(None, description="下班打卡地址")
    status: int = Field(..., description="状态")
    remark: Optional[str] = Field(None, description="备注")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "AttendanceCreate",
    "AttendanceUpdate",
    "AttendanceResponse",
]
