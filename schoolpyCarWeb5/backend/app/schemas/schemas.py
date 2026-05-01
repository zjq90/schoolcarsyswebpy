"""
Pydantic模型定义
用于数据验证和序列化
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ==================== 用户模型 ====================
class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    role: str = Field(default="admin", description="角色")
    status: bool = Field(default=True, description="状态")


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserUpdate(BaseModel):
    """用户更新模型"""
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 校车模型 ====================
class BusBase(BaseModel):
    """校车基础模型"""
    plate_number: str = Field(..., max_length=20, description="车牌号")
    bus_number: str = Field(..., max_length=20, description="校车编号")
    model: Optional[str] = Field(None, max_length=50, description="车型")
    capacity: int = Field(default=40, ge=1, description="核载人数")
    driver_id: Optional[int] = Field(None, description="司机ID")
    status: str = Field(default="idle", description="状态")
    current_latitude: Optional[float] = Field(None, description="当前纬度")
    current_longitude: Optional[float] = Field(None, description="当前经度")


class BusCreate(BusBase):
    """校车创建模型"""
    pass


class BusUpdate(BaseModel):
    """校车更新模型"""
    plate_number: Optional[str] = None
    bus_number: Optional[str] = None
    model: Optional[str] = None
    capacity: Optional[int] = None
    driver_id: Optional[int] = None
    status: Optional[str] = None
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None


class BusResponse(BusBase):
    """校车响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 司机模型 ====================
class DriverBase(BaseModel):
    """司机基础模型"""
    name: str = Field(..., max_length=50, description="姓名")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    id_card: Optional[str] = Field(None, max_length=18, description="身份证号")
    license_number: Optional[str] = Field(None, max_length=50, description="驾驶证号")
    license_type: Optional[str] = Field(None, max_length=10, description="准驾车型")
    status: bool = Field(default=True, description="状态")


class DriverCreate(DriverBase):
    """司机创建模型"""
    pass


class DriverUpdate(BaseModel):
    """司机更新模型"""
    name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    license_number: Optional[str] = None
    license_type: Optional[str] = None
    status: Optional[bool] = None


class DriverResponse(DriverBase):
    """司机响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 学生模型 ====================
class StudentBase(BaseModel):
    """学生基础模型"""
    name: str = Field(..., max_length=50, description="姓名")
    student_number: Optional[str] = Field(None, max_length=20, description="学号")
    class_name: Optional[str] = Field(None, max_length=50, description="班级")
    school: Optional[str] = Field(None, max_length=100, description="学校")
    parent_name: Optional[str] = Field(None, max_length=50, description="家长姓名")
    parent_phone: Optional[str] = Field(None, max_length=20, description="家长联系电话")
    bus_id: Optional[int] = Field(None, description="所属校车ID")
    status: bool = Field(default=True, description="状态")


class StudentCreate(StudentBase):
    """学生创建模型"""
    pass


class StudentUpdate(BaseModel):
    """学生更新模型"""
    name: Optional[str] = None
    student_number: Optional[str] = None
    class_name: Optional[str] = None
    school: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    bus_id: Optional[int] = None
    status: Optional[bool] = None


class StudentResponse(StudentBase):
    """学生响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 报警级别模型 ====================
class AlarmLevelBase(BaseModel):
    """报警级别基础模型"""
    level: int = Field(..., ge=1, le=3, description="级别：1-一级，2-二级，3-三级")
    name: str = Field(..., max_length=50, description="级别名称")
    color: Optional[str] = Field(None, max_length=20, description="颜色")
    description: Optional[str] = Field(None, description="级别描述")
    response_mechanism: Optional[str] = Field(None, description="响应机制描述")


class AlarmLevelCreate(AlarmLevelBase):
    """报警级别创建模型"""
    pass


class AlarmLevelUpdate(BaseModel):
    """报警级别更新模型"""
    level: Optional[int] = None
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    response_mechanism: Optional[str] = None


class AlarmLevelResponse(AlarmLevelBase):
    """报警级别响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 报警类型模型 ====================
class AlarmTypeBase(BaseModel):
    """报警类型基础模型"""
    name: str = Field(..., max_length=50, description="类型名称")
    level_id: int = Field(..., description="所属级别ID")
    description: Optional[str] = Field(None, description="类型描述")
    trigger_condition: Optional[str] = Field(None, description="触发条件")
    is_auto: bool = Field(default=False, description="是否自动触发")


class AlarmTypeCreate(AlarmTypeBase):
    """报警类型创建模型"""
    pass


class AlarmTypeUpdate(BaseModel):
    """报警类型更新模型"""
    name: Optional[str] = None
    level_id: Optional[int] = None
    description: Optional[str] = None
    trigger_condition: Optional[str] = None
    is_auto: Optional[bool] = None


class AlarmTypeResponse(AlarmTypeBase):
    """报警类型响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 报警记录模型 ====================
class AlarmBase(BaseModel):
    """报警基础模型"""
    alarm_number: str = Field(..., max_length=50, description="报警编号")
    type_id: int = Field(..., description="报警类型ID")
    level_id: int = Field(..., description="报警级别ID")
    bus_id: int = Field(..., description="校车ID")
    driver_id: Optional[int] = Field(None, description="司机ID")
    latitude: Optional[float] = Field(None, description="纬度")
    longitude: Optional[float] = Field(None, description="经度")
    location_name: Optional[str] = Field(None, max_length=255, description="位置名称")
    status: str = Field(default="pending", description="状态")
    is_read: bool = Field(default=False, description="是否已读")
    description: Optional[str] = Field(None, description="报警描述")
    remark: Optional[str] = Field(None, description="备注")


class AlarmCreate(AlarmBase):
    """报警创建模型"""
    pass


class AlarmTrigger(BaseModel):
    """报警触发模型"""
    type_id: int = Field(..., description="报警类型ID")
    bus_id: int = Field(..., description="校车ID")
    latitude: Optional[float] = Field(None, description="纬度")
    longitude: Optional[float] = Field(None, description="经度")
    location_name: Optional[str] = Field(None, description="位置名称")
    description: Optional[str] = Field(None, description="报警描述")


class AlarmUpdate(BaseModel):
    """报警更新模型"""
    status: Optional[str] = None
    is_read: Optional[bool] = None
    remark: Optional[str] = None


class AlarmResponse(AlarmBase):
    """报警响应模型"""
    id: int
    triggered_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 报警响应模型 ====================
class AlarmResponseBase(BaseModel):
    """报警响应基础模型"""
    alarm_id: int = Field(..., description="报警ID")
    operator_id: int = Field(..., description="操作人ID")
    action: Optional[str] = Field(None, max_length=50, description="动作")
    description: Optional[str] = Field(None, description="动作描述")
    notify_police: bool = Field(default=False, description="是否通知警方")
    notify_school: bool = Field(default=False, description="是否通知学校")
    notify_parents: bool = Field(default=False, description="是否通知家长")
    notify_driver: bool = Field(default=False, description="是否通知司机")


class AlarmResponseCreate(AlarmResponseBase):
    """报警响应创建模型"""
    pass


class AlarmResponseUpdate(BaseModel):
    """报警响应更新模型"""
    action: Optional[str] = None
    description: Optional[str] = None
    notify_police: Optional[bool] = None
    notify_school: Optional[bool] = None
    notify_parents: Optional[bool] = None
    notify_driver: Optional[bool] = None


class AlarmResponseResponse(AlarmResponseBase):
    """报警响应响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 位置记录模型 ====================
class LocationBase(BaseModel):
    """位置基础模型"""
    bus_id: int = Field(..., description="校车ID")
    latitude: float = Field(..., description="纬度")
    longitude: float = Field(..., description="经度")
    location_name: Optional[str] = Field(None, max_length=255, description="位置名称")
    speed: float = Field(default=0, ge=0, description="速度")
    direction: int = Field(default=0, ge=0, le=360, description="方向")


class LocationCreate(LocationBase):
    """位置创建模型"""
    pass


class LocationResponse(LocationBase):
    """位置响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
