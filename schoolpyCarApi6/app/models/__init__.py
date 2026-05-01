"""
数据库模型模块
==============

包含所有数据库表的SQLAlchemy模型定义:
- User: 用户基础表（家长、司机、管理员）
- Parent: 家长信息表
- Student: 学生信息表
- ParentStudent: 家长与学生关联表
- Driver: 司机信息表
- Vehicle: 车辆信息表
- DriverVehicle: 司机与车辆绑定表
- Attendance: 司机上下班打卡记录
- Message: 消息推送表
- MessageCategory: 消息分类表
- Complaint: 投诉表
- Feedback: 反馈表（处理结果、车辆保养）
- Emergency: 紧急状况申请表
- Dispatch: 调度消息表
- Route: 路线规划表
- Violation: 违章记录表
"""

from app.models.user import User
from app.models.parent import Parent
from app.models.student import Student
from app.models.parent_student import ParentStudent
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.driver_vehicle import DriverVehicle
from app.models.attendance import Attendance
from app.models.message import Message
from app.models.message_category import MessageCategory
from app.models.complaint import Complaint
from app.models.feedback import Feedback
from app.models.emergency import Emergency
from app.models.dispatch import Dispatch
from app.models.route import Route
from app.models.violation import Violation

__all__ = [
    "User",
    "Parent",
    "Student",
    "ParentStudent",
    "Driver",
    "Vehicle",
    "DriverVehicle",
    "Attendance",
    "Message",
    "MessageCategory",
    "Complaint",
    "Feedback",
    "Emergency",
    "Dispatch",
    "Route",
    "Violation",
]
