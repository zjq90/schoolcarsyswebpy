"""
校车管理系统配置文件
包含数据库配置、JWT配置、权限配置等
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/schoolbus.db")

# JWT配置（用于登录认证）
SECRET_KEY = os.getenv("SECRET_KEY", "schoolbus-secret-key-2024-very-secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时过期

# 权限角色定义
ROLES = {
    "EDUCATION_BUREAU": "education_bureau",  # 教育局（最高权限）
    "SCHOOL_ADMIN": "school_admin",           # 学校管理员
}

# 权限定义
PERMISSIONS = {
    # 教育局权限
    "GLOBAL_MONITOR": "global_monitor",        # 全域监控
    "CROSS_SCHOOL_SCHEDULE": "cross_school_schedule",  # 跨校调度
    "POLICY_PUBLISH": "policy_publish",        # 政策发布
    "SYSTEM_MANAGE": "system_manage",          # 系统管理
    
    # 学校管理员权限
    "VEHICLE_MANAGE": "vehicle_manage",        # 车辆管理
    "DRIVER_MANAGE": "driver_manage",          # 司机管理
    "STUDENT_MANAGE": "student_manage",        # 学生管理
    "ROUTE_MANAGE": "route_manage",            # 路线管理
}

# 角色权限映射
ROLE_PERMISSIONS = {
    ROLES["EDUCATION_BUREAU"]: [
        PERMISSIONS["GLOBAL_MONITOR"],
        PERMISSIONS["CROSS_SCHOOL_SCHEDULE"],
        PERMISSIONS["POLICY_PUBLISH"],
        PERMISSIONS["SYSTEM_MANAGE"],
        PERMISSIONS["VEHICLE_MANAGE"],
        PERMISSIONS["DRIVER_MANAGE"],
        PERMISSIONS["STUDENT_MANAGE"],
        PERMISSIONS["ROUTE_MANAGE"],
    ],
    ROLES["SCHOOL_ADMIN"]: [
        PERMISSIONS["VEHICLE_MANAGE"],
        PERMISSIONS["DRIVER_MANAGE"],
        PERMISSIONS["STUDENT_MANAGE"],
        PERMISSIONS["ROUTE_MANAGE"],
    ],
}

# 静态文件配置
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"

# 确保数据目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
