"""
司机数据模型
=============

包含司机相关的请求和响应模型。
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


class DriverCreate(BaseModel):
    """
    司机创建模型

    Attributes:
        real_name: 真实姓名
        id_card: 身份证号
        driver_license_no: 驾驶证号
        driver_license_type: 驾驶证类型
        driver_license_expiry: 驾驶证有效期
        phone: 联系电话
        address: 住址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
    """

    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    driver_license_no: Optional[str] = Field(None, max_length=50, description="驾驶证号")
    driver_license_type: Optional[str] = Field(None, max_length=20, description="驾驶证类型")
    driver_license_expiry: Optional[date] = Field(None, description="驾驶证有效期")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=200, description="住址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")


class DriverUpdate(BaseModel):
    """
    司机更新模型

    Attributes:
        real_name: 真实姓名
        id_card: 身份证号
        driver_license_no: 驾驶证号
        driver_license_type: 驾驶证类型
        driver_license_expiry: 驾驶证有效期
        phone: 联系电话
        address: 住址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
        status: 状态：1-在职，0-离职
    """

    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    driver_license_no: Optional[str] = Field(None, max_length=50, description="驾驶证号")
    driver_license_type: Optional[str] = Field(None, max_length=20, description="驾驶证类型")
    driver_license_expiry: Optional[date] = Field(None, description="驾驶证有效期")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=200, description="住址")
    emergency_contact: Optional[str] = Field(None, max_length=50, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    status: Optional[int] = Field(None, description="状态: 1-在职, 0-离职")


class DriverResponse(BaseModel):
    """
    司机响应模型

    Attributes:
        id: 司机ID
        user_id: 用户ID
        real_name: 真实姓名
        id_card: 身份证号
        driver_license_no: 驾驶证号
        driver_license_type: 驾驶证类型
        driver_license_expiry: 驾驶证有效期
        phone: 联系电话
        address: 住址
        emergency_contact: 紧急联系人
        emergency_phone: 紧急联系电话
        status: 状态：1-在职，0-离职
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="司机ID")
    user_id: int = Field(..., description="用户ID")
    real_name: Optional[str] = Field(None, description="真实姓名")
    id_card: Optional[str] = Field(None, description="身份证号")
    driver_license_no: Optional[str] = Field(None, description="驾驶证号")
    driver_license_type: Optional[str] = Field(None, description="驾驶证类型")
    driver_license_expiry: Optional[date] = Field(None, description="驾驶证有效期")
    phone: Optional[str] = Field(None, description="联系电话")
    address: Optional[str] = Field(None, description="住址")
    emergency_contact: Optional[str] = Field(None, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, description="紧急联系电话")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class CheckInRequest(BaseModel):
    """
    打卡请求模型

    Attributes:
        vehicle_id: 车辆ID
        latitude: 纬度
        longitude: 经度
        address: 地址
    """

    vehicle_id: int = Field(..., description="车辆ID")
    latitude: Optional[float] = Field(None, description="纬度")
    longitude: Optional[float] = Field(None, description="经度")
    address: Optional[str] = Field(None, max_length=200, description="地址")


class VehicleBindRequest(BaseModel):
    """
    车辆绑定请求模型

    Attributes:
        vehicle_id: 车辆ID
    """

    vehicle_id: int = Field(..., description="车辆ID")


__all__ = [
    "DriverCreate",
    "DriverUpdate",
    "DriverResponse",
    "CheckInRequest",
    "VehicleBindRequest",
]
