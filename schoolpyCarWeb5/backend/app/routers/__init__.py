"""
路由模块
"""

from .alarm import router as alarm_router
from .bus import router as bus_router
from .driver import router as driver_router
from .student import router as student_router
from .user import router as user_router
from .alarm_level import router as alarm_level_router
from .alarm_type import router as alarm_type_router
from .location import router as location_router
from .test import router as test_router

__all__ = [
    "alarm_router",
    "bus_router",
    "driver_router",
    "student_router",
    "user_router",
    "alarm_level_router",
    "alarm_type_router",
    "location_router",
    "test_router"
]
