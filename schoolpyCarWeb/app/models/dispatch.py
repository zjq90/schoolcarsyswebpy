"""
调度数据模型
定义跨校调度信息
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Dispatch(Base):
    """
    调度表
    存储跨校车辆调度信息（教育局管理员使用）
    """
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True, comment="调度ID，主键")
    dispatch_code = Column(String(50), unique=True, index=True, comment="调度编码")
    dispatch_type = Column(String(50), default="temporary", comment="调度类型：temporary(临时调度) / regular(定期调度) / emergency(应急调度)")
    
    # 原所属信息
    from_school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="调出学校ID")
    from_vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, comment="调出车辆ID")
    from_driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True, comment="调出司机ID")
    
    # 目标学校信息
    to_school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, comment="调入学校ID")
    
    # 时间安排
    start_date = Column(Date, comment="调度开始日期")
    end_date = Column(Date, comment="调度结束日期")
    departure_time = Column(Time, comment="发车时间")
    return_time = Column(Time, comment="返回时间")
    
    # 调度原因
    reason = Column(Text, comment="调度原因")
    dispatch_route = Column(Text, comment="调度路线")
    
    # 调度人
    dispatcher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="调度人ID（教育局管理员）")
    
    status = Column(String(20), default="pending", comment="状态：pending(待执行) / in_progress(执行中) / completed(已完成) / cancelled(已取消)")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    from_school = relationship("School", foreign_keys=[from_school_id])
    to_school = relationship("School", foreign_keys=[to_school_id])
    vehicle = relationship("Vehicle")
    driver = relationship("Driver")
    dispatcher = relationship("User")

    def __repr__(self):
        return f"<Dispatch(id={self.id}, code={self.dispatch_code})>"
