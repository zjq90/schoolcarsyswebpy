"""
数据库模型定义
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.app.database import Base


class User(Base):
    """
    用户表模型
    存储系统用户信息，包括管理员、学校管理员等
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    real_name = Column(String(50), comment="真实姓名")
    phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    role = Column(String(20), default="admin", comment="角色：admin(超级管理员), school_admin(学校管理员)")
    status = Column(Boolean, default=True, comment="状态：True-启用，False-禁用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class Bus(Base):
    """
    校车门模型
    存储校车基本信息
    """
    __tablename__ = "buses"
    
    id = Column(Integer, primary_key=True, index=True, comment="校车ID")
    plate_number = Column(String(20), unique=True, index=True, nullable=False, comment="车牌号")
    bus_number = Column(String(20), unique=True, index=True, nullable=False, comment="校车编号")
    model = Column(String(50), comment="车型")
    capacity = Column(Integer, default=40, comment="核载人数")
    driver_id = Column(Integer, ForeignKey("drivers.id"), comment="司机ID")
    status = Column(String(20), default="idle", comment="状态：idle(空闲), running(运行中), maintenance(维护中)")
    current_latitude = Column(Float, comment="当前纬度")
    current_longitude = Column(Float, comment="当前经度")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联关系
    driver = relationship("Driver", back_populates="buses")


class Driver(Base):
    """
    司机表模型
    存储司机基本信息
    """
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True, comment="司机ID")
    name = Column(String(50), nullable=False, comment="姓名")
    phone = Column(String(20), comment="联系电话")
    id_card = Column(String(18), unique=True, comment="身份证号")
    license_number = Column(String(50), unique=True, comment="驾驶证号")
    license_type = Column(String(10), comment="准驾车型")
    status = Column(Boolean, default=True, comment="状态：True-在岗，False-离岗")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联关系
    buses = relationship("Bus", back_populates="driver")


class Student(Base):
    """
    学生表模型
    存储学生基本信息
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True, comment="学生ID")
    name = Column(String(50), nullable=False, comment="姓名")
    student_number = Column(String(20), unique=True, index=True, comment="学号")
    class_name = Column(String(50), comment="班级")
    school = Column(String(100), comment="学校")
    parent_name = Column(String(50), comment="家长姓名")
    parent_phone = Column(String(20), comment="家长联系电话")
    bus_id = Column(Integer, ForeignKey("buses.id"), comment="所属校车ID")
    status = Column(Boolean, default=True, comment="状态：True-在校，False-离校")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class AlarmLevel(Base):
    """
    报警级别表模型
    存储报警级别配置信息
    """
    __tablename__ = "alarm_levels"
    
    id = Column(Integer, primary_key=True, index=True, comment="级别ID")
    level = Column(Integer, unique=True, nullable=False, comment="级别：1-一级，2-二级，3-三级")
    name = Column(String(50), nullable=False, comment="级别名称")
    color = Column(String(20), comment="颜色：red, orange, blue")
    description = Column(Text, comment="级别描述")
    response_mechanism = Column(Text, comment="响应机制描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class AlarmType(Base):
    """
    报警类型表模型
    存储报警类型配置信息
    """
    __tablename__ = "alarm_types"
    
    id = Column(Integer, primary_key=True, index=True, comment="类型ID")
    name = Column(String(50), nullable=False, comment="类型名称")
    level_id = Column(Integer, ForeignKey("alarm_levels.id"), nullable=False, comment="所属级别ID")
    description = Column(Text, comment="类型描述")
    trigger_condition = Column(Text, comment="触发条件")
    is_auto = Column(Boolean, default=False, comment="是否自动触发：True-自动，False-手动")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class Alarm(Base):
    """
    报警记录表模型
    存储报警事件信息
    """
    __tablename__ = "alarms"
    
    id = Column(Integer, primary_key=True, index=True, comment="报警ID")
    alarm_number = Column(String(50), unique=True, index=True, nullable=False, comment="报警编号")
    type_id = Column(Integer, ForeignKey("alarm_types.id"), nullable=False, comment="报警类型ID")
    level_id = Column(Integer, ForeignKey("alarm_levels.id"), nullable=False, comment="报警级别ID")
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False, comment="校车ID")
    driver_id = Column(Integer, ForeignKey("drivers.id"), comment="司机ID")
    
    # 位置信息
    latitude = Column(Float, comment="纬度")
    longitude = Column(Float, comment="经度")
    location_name = Column(String(255), comment="位置名称")
    
    # 状态信息
    status = Column(String(20), default="pending", comment="状态：pending(待处理), processing(处理中), resolved(已解决), closed(已关闭)")
    is_read = Column(Boolean, default=False, comment="是否已读")
    
    # 时间信息
    triggered_at = Column(DateTime, default=datetime.now, comment="触发时间")
    resolved_at = Column(DateTime, comment="解决时间")
    
    # 附加信息
    description = Column(Text, comment="报警描述")
    remark = Column(Text, comment="备注")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联关系
    responses = relationship("AlarmResponse", back_populates="alarm")


class AlarmResponse(Base):
    """
    报警响应表模型
    存储报警响应过程信息
    """
    __tablename__ = "alarm_responses"
    
    id = Column(Integer, primary_key=True, index=True, comment="响应ID")
    alarm_id = Column(Integer, ForeignKey("alarms.id"), nullable=False, comment="报警ID")
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="操作人ID")
    
    # 响应动作
    action = Column(String(50), comment="动作：confirm(确认), notify(通知), dispatch(派单), resolve(解决), close(关闭)")
    description = Column(Text, comment="动作描述")
    
    # 通知对象
    notify_police = Column(Boolean, default=False, comment="是否通知警方")
    notify_school = Column(Boolean, default=False, comment="是否通知学校")
    notify_parents = Column(Boolean, default=False, comment="是否通知家长")
    notify_driver = Column(Boolean, default=False, comment="是否通知司机")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关联关系
    alarm = relationship("Alarm", back_populates="responses")


class Location(Base):
    """
    位置记录表模型
    存储校车位置历史记录
    """
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True, comment="记录ID")
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False, comment="校车ID")
    
    latitude = Column(Float, nullable=False, comment="纬度")
    longitude = Column(Float, nullable=False, comment="经度")
    location_name = Column(String(255), comment="位置名称")
    
    speed = Column(Float, default=0, comment="速度(km/h)")
    direction = Column(Integer, default=0, comment="方向(0-360度)")
    
    created_at = Column(DateTime, default=datetime.now, comment="记录时间")
