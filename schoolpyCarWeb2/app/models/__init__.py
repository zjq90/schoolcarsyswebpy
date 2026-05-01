from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

# ==================== 枚举类型定义 ====================

class VehicleStatus(str, Enum):
    """车辆状态枚举"""
    ONLINE = "online"      # 在线
    OFFLINE = "offline"    # 离线
    RUNNING = "running"    # 运行中
    IDLE = "idle"          # 待机
    MAINTENANCE = "maintenance"  # 维护中


class GeofenceType(str, Enum):
    """电子围栏类型枚举"""
    SCHOOL = "school"      # 学校区域
    DANGER = "danger"      # 危险路段
    HOME = "home"          # 学生家庭区域
    OTHER = "other"        # 其他区域


class AlertStatus(str, Enum):
    """预警状态枚举"""
    ACTIVE = "active"      # 活跃
    RESOLVED = "resolved"  # 已处理
    IGNORED = "ignored"    # 已忽略


# ==================== 基础模型 ====================

class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    real_name: str
    phone: str
    role: str


class UserCreate(UserBase):
    """用户创建模型"""
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    create_time: datetime

    class Config:
        from_attributes = True


# ==================== 车辆相关模型 ====================

class VehicleBase(BaseModel):
    """车辆基础模型"""
    plate_number: str        # 车牌号
    vehicle_type: str        # 车辆类型
    capacity: int            # 核载人数
    driver_name: str         # 司机姓名
    driver_phone: str        # 司机电话
    status: VehicleStatus    # 车辆状态
    school: str              # 所属学校


class VehicleCreate(VehicleBase):
    """车辆创建模型"""
    pass


class VehicleUpdate(BaseModel):
    """车辆更新模型"""
    plate_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: Optional[VehicleStatus] = None
    school: Optional[str] = None


class VehicleResponse(VehicleBase):
    """车辆响应模型"""
    id: int
    create_time: datetime

    class Config:
        from_attributes = True


# ==================== 定位数据模型 ====================

class LocationDataBase(BaseModel):
    """定位数据基础模型"""
    vehicle_id: int          # 车辆ID
    latitude: float          # 纬度
    longitude: float         # 经度
    altitude: float          # 海拔高度（米）
    speed: float             # 速度（km/h）
    direction: float         # 方向（0-360度）
    satellite_count: int     # 卫星数量
    positioning_mode: str    # 定位模式（GPS/北斗/双模）
    signal_strength: int     # 信号强度（0-100）


class LocationDataCreate(LocationDataBase):
    """定位数据创建模型"""
    pass


class LocationDataResponse(LocationDataBase):
    """定位数据响应模型"""
    id: int
    create_time: datetime

    class Config:
        from_attributes = True


class RealTimeLocationResponse(BaseModel):
    """实时定位响应模型"""
    vehicle_id: int
    plate_number: str
    driver_name: str
    latitude: float
    longitude: float
    speed: float
    direction: float
    status: VehicleStatus
    last_update: datetime


# ==================== 历史轨迹模型 ====================

class TrajectoryHistoryResponse(BaseModel):
    """历史轨迹响应模型"""
    id: int
    vehicle_id: int
    plate_number: str
    latitude: float
    longitude: float
    altitude: float
    speed: float
    direction: float
    record_time: datetime


class TrajectoryQuery(BaseModel):
    """轨迹查询条件模型"""
    vehicle_id: int
    start_time: datetime
    end_time: datetime


# ==================== 电子围栏模型 ====================

class GeofenceBase(BaseModel):
    """电子围栏基础模型"""
    name: str                # 围栏名称
    fence_type: GeofenceType # 围栏类型
    description: str         # 描述
    latitude: float          # 中心纬度
    longitude: float         # 中心经度
    radius: float            # 半径（米）
    is_active: bool          # 是否启用
    alert_threshold: int     # 越界阈值（次数）


class GeofenceCreate(GeofenceBase):
    """电子围栏创建模型"""
    pass


class GeofenceUpdate(BaseModel):
    """电子围栏更新模型"""
    name: Optional[str] = None
    fence_type: Optional[GeofenceType] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[float] = None
    is_active: Optional[bool] = None
    alert_threshold: Optional[int] = None


class GeofenceResponse(GeofenceBase):
    """电子围栏响应模型"""
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


# ==================== 越界预警模型 ====================

class AlertBase(BaseModel):
    """预警基础模型"""
    vehicle_id: int          # 车辆ID
    geofence_id: int         # 围栏ID
    fence_name: str          # 围栏名称
    fence_type: GeofenceType # 围栏类型
    violation_count: int     # 越界次数
    latitude: float          # 越界位置纬度
    longitude: float         # 越界位置经度
    status: AlertStatus      # 预警状态
    severity: str            # 严重程度


class AlertResponse(AlertBase):
    """预警响应模型"""
    id: int
    create_time: datetime
    resolve_time: Optional[datetime] = None
    resolver: Optional[str] = None
    resolve_note: Optional[str] = None

    class Config:
        from_attributes = True


class AlertHandle(BaseModel):
    """预警处理模型"""
    alert_id: int
    resolver: str
    resolve_note: str


# ==================== 统计数据模型 ====================

class DashboardStats(BaseModel):
    """仪表盘统计数据模型"""
    total_vehicles: int         # 车辆总数
    online_vehicles: int        # 在线车辆数
    running_vehicles: int       # 运行中车辆数
    active_geofences: int       # 活跃围栏数
    active_alerts: int          # 活跃预警数
    today_trajectory_count: int # 今日轨迹记录数
