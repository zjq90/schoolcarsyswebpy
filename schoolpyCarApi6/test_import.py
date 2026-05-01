print("=" * 60)
print("测试模块导入...")
print("=" * 60)

try:
    from app.config import settings
    print("✓ app.config 导入成功")
except Exception as e:
    print(f"✗ app.config 导入失败: {e}")

try:
    from app.database import engine, Base, SessionLocal, get_db, init_db
    print("✓ app.database 导入成功")
except Exception as e:
    print(f"✗ app.database 导入失败: {e}")

try:
    from app.models import (
        User, Parent, Student, ParentStudent,
        Driver, Vehicle, DriverVehicle, Attendance,
        Message, MessageCategory, Complaint,
        Feedback, Emergency, Dispatch, Route, Violation
    )
    print("✓ app.models 导入成功")
except Exception as e:
    print(f"✗ app.models 导入失败: {e}")

try:
    from app.schemas import (
        UserLogin, UserLoginByPhone, UserLoginByCode, UserResponse, UserCreate,
        Token, TokenData,
        ParentCreate, ParentUpdate, ParentResponse, StudentBindRequest,
        StudentCreate, StudentUpdate, StudentResponse, StudentWithRelationResponse,
        DriverCreate, DriverUpdate, DriverResponse, CheckInRequest, VehicleBindRequest,
        VehicleCreate, VehicleUpdate, VehicleResponse,
        MessageCreate, MessageUpdate, MessageResponse, MessageListResponse, MessageCategoryResponse,
        ComplaintCreate, ComplaintUpdate, ComplaintResponse,
        FeedbackCreate, FeedbackUpdate, FeedbackResponse,
        EmergencyCreate, EmergencyUpdate, EmergencyResponse,
        DispatchCreate, DispatchUpdate, DispatchResponse,
        RouteCreate, RouteUpdate, RouteResponse,
        ViolationCreate, ViolationUpdate, ViolationResponse,
        AttendanceCreate, AttendanceUpdate, AttendanceResponse,
        CommonResponse, PaginationParams, PaginatedResponse,
    )
    print("✓ app.schemas 导入成功")
except Exception as e:
    print(f"✗ app.schemas 导入失败: {e}")

try:
    from app.utils.auth import (
        get_password_hash, verify_password,
        create_access_token, decode_access_token,
        get_current_user, get_current_active_user,
    )
    print("✓ app.utils.auth 导入成功")
except Exception as e:
    print(f"✗ app.utils.auth 导入失败: {e}")

try:
    from app.utils.sms import (
        generate_verify_code, send_sms_code, verify_sms_code,
    )
    print("✓ app.utils.sms 导入成功")
except Exception as e:
    print(f"✗ app.utils.sms 导入失败: {e}")

try:
    from app.utils.common import (
        get_current_time, generate_random_string, generate_random_number,
        create_success_response, create_error_response,
        format_phone, validate_phone,
        calculate_page_offset, calculate_total_pages,
    )
    print("✓ app.utils.common 导入成功")
except Exception as e:
    print(f"✗ app.utils.common 导入失败: {e}")

print("\n" + "=" * 60)
print("测试路由模块导入...")
print("=" * 60)

try:
    from app.routers.parent import router as parent_router
    print("✓ app.routers.parent 导入成功")
except Exception as e:
    print(f"✗ app.routers.parent 导入失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.routers.driver import router as driver_router
    print("✓ app.routers.driver 导入成功")
except Exception as e:
    print(f"✗ app.routers.driver 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试主应用导入...")
print("=" * 60)

try:
    from app.main import app
    print("✓ app.main 导入成功")
    print(f"  - 应用名称: {app.title}")
    print(f"  - 版本: {app.version}")
    print(f"  - 路由数量: {len(app.routes)}")
except Exception as e:
    print(f"✗ app.main 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("所有模块导入测试完成!")
print("=" * 60)
