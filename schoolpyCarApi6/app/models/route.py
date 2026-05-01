"""
路线规划模型
=============

路线规划表，存储校车的路线信息。
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Time
from sqlalchemy.sql import func
from app.database import Base


class Route(Base):
    """
    路线规划表

    Attributes:
        id: 路线ID，主键
        route_no: 路线编号
        route_name: 路线名称
        start_point: 起点
        end_point: 终点
        waypoints: 途经点列表（JSON格式）
        estimated_duration: 预计时长（分钟）
        distance: 距离（公里）
        departure_time: 发车时间
        arrival_time: 预计到达时间
        student_count: 学生数量
        status: 状态：1-启用，0-禁用
        description: 路线描述
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_no = Column(String(20), unique=True, nullable=True, comment="路线编号")
    route_name = Column(String(100), nullable=False, comment="路线名称")
    start_point = Column(String(200), nullable=False, comment="起点")
    end_point = Column(String(200), nullable=False, comment="终点")
    waypoints = Column(Text, nullable=True, comment="途经点列表(JSON)")
    estimated_duration = Column(Integer, nullable=True, comment="预计时长(分钟)")
    distance = Column(Integer, nullable=True, comment="距离(公里)")
    departure_time = Column(Time, nullable=True, comment="发车时间")
    arrival_time = Column(Time, nullable=True, comment="预计到达时间")
    student_count = Column(Integer, default=0, comment="学生数量")
    status = Column(Integer, default=1, comment="状态: 1-启用, 0-禁用")
    description = Column(String(500), nullable=True, comment="路线描述")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Route(id={self.id}, route_name={self.route_name})>"
