from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.school import router as school_router
from app.routers.vehicle import router as vehicle_router
from app.routers.driver import router as driver_router
from app.routers.student import router as student_router
from app.routers.route import router as route_router
from app.routers.policy import router as policy_router
from app.routers.dispatch import router as dispatch_router

__all__ = [
    "auth_router", "user_router", "school_router",
    "vehicle_router", "driver_router", "student_router",
    "route_router", "policy_router", "dispatch_router"
]
