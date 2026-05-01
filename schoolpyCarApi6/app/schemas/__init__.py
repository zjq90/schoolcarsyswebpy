"""
Pydantic数据模型模块
====================

包含所有API请求和响应的数据验证模型:
- user: 用户相关模型（登录、注册、响应）
- parent: 家长相关模型
- student: 学生相关模型
- driver: 司机相关模型
- vehicle: 车辆相关模型
- message: 消息相关模型
- complaint: 投诉相关模型
- feedback: 反馈相关模型
- emergency: 紧急状况相关模型
- dispatch: 调度消息相关模型
- route: 路线规划相关模型
- violation: 违章相关模型
- attendance: 打卡相关模型
- common: 通用模型（分页、响应等）
"""

from app.schemas.user import (
    UserLogin,
    UserLoginByPhone,
    UserLoginByCode,
    UserResponse,
    UserCreate,
    Token,
    TokenData,
)
from app.schemas.parent import (
    ParentCreate,
    ParentUpdate,
    ParentResponse,
    StudentBindRequest,
)
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentWithRelationResponse,
)
from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverResponse,
    CheckInRequest,
    VehicleBindRequest,
)
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
)
from app.schemas.message import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessageListResponse,
    MessageCategoryResponse,
)
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
)
from app.schemas.emergency import (
    EmergencyCreate,
    EmergencyUpdate,
    EmergencyResponse,
)
from app.schemas.dispatch import (
    DispatchCreate,
    DispatchUpdate,
    DispatchResponse,
)
from app.schemas.route import (
    RouteCreate,
    RouteUpdate,
    RouteResponse,
)
from app.schemas.violation import (
    ViolationCreate,
    ViolationUpdate,
    ViolationResponse,
)
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
)
from app.schemas.common import (
    CommonResponse,
    PaginationParams,
    PaginatedResponse,
)

__all__ = [
    "UserLogin",
    "UserLoginByPhone",
    "UserLoginByCode",
    "UserResponse",
    "UserCreate",
    "Token",
    "TokenData",
    "ParentCreate",
    "ParentUpdate",
    "ParentResponse",
    "StudentBindRequest",
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "StudentWithRelationResponse",
    "DriverCreate",
    "DriverUpdate",
    "DriverResponse",
    "CheckInRequest",
    "VehicleBindRequest",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
    "MessageCreate",
    "MessageUpdate",
    "MessageResponse",
    "MessageListResponse",
    "MessageCategoryResponse",
    "ComplaintCreate",
    "ComplaintUpdate",
    "ComplaintResponse",
    "FeedbackCreate",
    "FeedbackUpdate",
    "FeedbackResponse",
    "EmergencyCreate",
    "EmergencyUpdate",
    "EmergencyResponse",
    "DispatchCreate",
    "DispatchUpdate",
    "DispatchResponse",
    "RouteCreate",
    "RouteUpdate",
    "RouteResponse",
    "ViolationCreate",
    "ViolationUpdate",
    "ViolationResponse",
    "AttendanceCreate",
    "AttendanceUpdate",
    "AttendanceResponse",
    "CommonResponse",
    "PaginationParams",
    "PaginatedResponse",
]
