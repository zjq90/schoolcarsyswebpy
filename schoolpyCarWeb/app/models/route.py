"""
路线数据模型
定义校车行驶路线信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Route(Base):
    """
    路线表
    存储校车行驶路线信息
    """
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True, comment="路线ID，主键")
    route_code = Column(String(50), unique=True, index=True, comment="路线编码")
    route_name = Column(String(100), nullable=False, comment="路线名称")
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="所属学校ID")
    
    # 出发和目的地
    start_address = Column(String(255), comment="出发起始地址")
    end_address = Column(String(255), comment="目的地址（学校）")
    
    # 主行驶路线
    main_route = Column(Text, comment="主行驶路线（详细描述）")
    main_route_stops = Column(Text, comment="主路线途经站点（JSON格式存储站点列表）")
    
    # 应急行驶路线
    emergency_route = Column(Text, comment="应急行驶路线")
    emergency_route_stops = Column(Text, comment="应急路线途经站点")
    
    # 备用行驶路线
    backup_route = Column(Text, comment="备用行驶路线")
    backup_route_stops = Column(Text, comment="备用路线途经站点")
    
    # 时间安排
    departure_time = Column(Time, comment="发车时间")
    estimated_duration = Column(Integer, comment="预计行驶时长（分钟）")
    return_departure_time = Column(Time, comment="返程发车时间")
    return_estimated_duration = Column(Integer, comment="返程预计时长（分钟）")
    
    # 车辆和司机
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True, comment="指定车辆ID")
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True, comment="指定司机ID")
    
    status = Column(String(20), default="active", comment="状态：active(启用) / inactive(停用)")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    school = relationship("School", back_populates="routes")
    students = relationship("Student", back_populates="route")

    def __repr__(self):
        return f"<Route(id={self.id}, name={self.route_name})>"
