"""
路线规划数据模型
=================

包含路线规划相关的请求和响应模型。
"""

from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, time


class RouteCreate(BaseModel):
    """
    路线创建模型

    Attributes:
        route_no: 路线编号
        route_name: 路线名称
        start_point: 起点
        end_point: 终点
        waypoints: 途经点列表
        estimated_duration: 预计时长（分钟）
        distance: 距离（公里）
        departure_time: 发车时间
        arrival_time: 预计到达时间
        student_count: 学生数量
        description: 路线描述
    """

    route_no: Optional[str] = Field(None, max_length=20, description="路线编号")
    route_name: str = Field(..., max_length=100, description="路线名称")
    start_point: str = Field(..., max_length=200, description="起点")
    end_point: str = Field(..., max_length=200, description="终点")
    waypoints: Optional[list[Any]] = Field(None, description="途经点列表")
    estimated_duration: Optional[int] = Field(None, description="预计时长(分钟)")
    distance: Optional[int] = Field(None, description="距离(公里)")
    departure_time: Optional[time] = Field(None, description="发车时间")
    arrival_time: Optional[time] = Field(None, description="预计到达时间")
    student_count: int = Field(0, description="学生数量")
    description: Optional[str] = Field(None, max_length=500, description="路线描述")


class RouteUpdate(BaseModel):
    """
    路线更新模型

    Attributes:
        route_no: 路线编号
        route_name: 路线名称
        start_point: 起点
        end_point: 终点
        waypoints: 途经点列表
        estimated_duration: 预计时长（分钟）
        distance: 距离（公里）
        departure_time: 发车时间
        arrival_time: 预计到达时间
        student_count: 学生数量
        status: 状态：1-启用，0-禁用
        description: 路线描述
    """

    route_no: Optional[str] = Field(None, max_length=20, description="路线编号")
    route_name: Optional[str] = Field(None, max_length=100, description="路线名称")
    start_point: Optional[str] = Field(None, max_length=200, description="起点")
    end_point: Optional[str] = Field(None, max_length=200, description="终点")
    waypoints: Optional[list[Any]] = Field(None, description="途经点列表")
    estimated_duration: Optional[int] = Field(None, description="预计时长(分钟)")
    distance: Optional[int] = Field(None, description="距离(公里)")
    departure_time: Optional[time] = Field(None, description="发车时间")
    arrival_time: Optional[time] = Field(None, description="预计到达时间")
    student_count: Optional[int] = Field(None, description="学生数量")
    status: Optional[int] = Field(None, description="状态: 1-启用, 0-禁用")
    description: Optional[str] = Field(None, max_length=500, description="路线描述")


class RouteResponse(BaseModel):
    """
    路线响应模型

    Attributes:
        id: 路线ID
        route_no: 路线编号
        route_name: 路线名称
        start_point: 起点
        end_point: 终点
        waypoints: 途经点列表
        estimated_duration: 预计时长（分钟）
        distance: 距离（公里）
        departure_time: 发车时间
        arrival_time: 预计到达时间
        student_count: 学生数量
        status: 状态
        description: 路线描述
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="路线ID")
    route_no: Optional[str] = Field(None, description="路线编号")
    route_name: str = Field(..., description="路线名称")
    start_point: str = Field(..., description="起点")
    end_point: str = Field(..., description="终点")
    waypoints: Optional[list[Any]] = Field(None, description="途经点列表")
    estimated_duration: Optional[int] = Field(None, description="预计时长(分钟)")
    distance: Optional[int] = Field(None, description="距离(公里)")
    departure_time: Optional[time] = Field(None, description="发车时间")
    arrival_time: Optional[time] = Field(None, description="预计到达时间")
    student_count: int = Field(..., description="学生数量")
    status: int = Field(..., description="状态")
    description: Optional[str] = Field(None, description="路线描述")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


__all__ = [
    "RouteCreate",
    "RouteUpdate",
    "RouteResponse",
]
