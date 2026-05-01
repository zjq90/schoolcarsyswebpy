"""
司机端API路由
==============

包含司机端所有的API接口:
- 登录/注册
- 上下班打卡
- 车辆绑定
- 调度消息
- 推送消息
- 反馈提交
- 紧急状况申请
- 路线规划
- 违章查询
"""

from typing import Optional, List
from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.config import settings
from app.models import (
    User, Driver, Vehicle, DriverVehicle, Attendance,
    Message, MessageCategory, Feedback, Emergency,
    Dispatch, Route, Violation
)
from app.schemas import (
    UserLogin, UserLoginByCode, Token,
    DriverCreate, DriverUpdate, DriverResponse,
    CheckInRequest, VehicleBindRequest,
    VehicleResponse,
    MessageResponse, MessageListResponse, MessageCategoryResponse,
    FeedbackCreate, FeedbackResponse,
    EmergencyCreate, EmergencyResponse,
    DispatchResponse,
    RouteResponse,
    ViolationResponse,
    AttendanceResponse,
    CommonResponse,
)
from app.utils.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_active_user,
)
from app.utils.sms import send_sms_code, verify_sms_code
from app.utils.common import (
    create_success_response, create_error_response,
    validate_phone, format_phone,
    calculate_page_offset, calculate_total_pages,
)


router = APIRouter(prefix="/api/driver", tags=["司机端"])


@router.post("/login/password", response_model=CommonResponse[Token])
def login_by_password(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    司机端 - 密码登录

    使用手机号和密码进行登录。

    Args:
        login_data: 登录数据（手机号、密码）
        db: 数据库会话

    Returns:
        CommonResponse[Token]: 包含JWT令牌的响应
    """
    phone = format_phone(login_data.phone)

    if not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式不正确"
        )

    user = db.query(User).filter(
        User.phone == phone,
        User.user_type == settings.USER_TYPE_DRIVER
    ).first()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )

    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )

    user.last_login_time = datetime.now()
    db.commit()

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "phone": user.phone,
            "user_type": user.user_type,
        }
    )

    token_data = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return create_success_response(data=token_data, message="登录成功")


@router.post("/login/code", response_model=CommonResponse[Token])
def login_by_code(login_data: UserLoginByCode, db: Session = Depends(get_db)):
    """
    司机端 - 验证码登录

    使用手机号和验证码进行登录。如果用户不存在，会自动注册。

    Args:
        login_data: 登录数据（手机号、验证码）
        db: 数据库会话

    Returns:
        CommonResponse[Token]: 包含JWT令牌的响应
    """
    phone = format_phone(login_data.phone)

    if not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式不正确"
        )

    is_valid, message = verify_sms_code(phone, login_data.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    user = db.query(User).filter(
        User.phone == phone,
        User.user_type == settings.USER_TYPE_DRIVER
    ).first()

    if not user:
        user = User(
            phone=phone,
            user_type=settings.USER_TYPE_DRIVER,
            nickname=f"司机{phone[-4:]}",
            status=1,
        )
        db.add(user)
        db.flush()

        driver = Driver(
            user_id=user.id,
            status=1,
        )
        db.add(driver)

    user.last_login_time = datetime.now()
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "phone": user.phone,
            "user_type": user.user_type,
        }
    )

    token_data = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return create_success_response(data=token_data, message="登录成功")


@router.post("/send-code", response_model=CommonResponse)
def send_login_code(phone: str = Query(..., description="手机号")):
    """
    司机端 - 发送短信验证码

    发送登录用的短信验证码（模拟发送，实际会打印到控制台）。

    Args:
        phone: 手机号

    Returns:
        CommonResponse: 发送结果
    """
    phone = format_phone(phone)

    if not validate_phone(phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式不正确"
        )

    code = send_sms_code(phone)

    return create_success_response(
        data={"code": code, "expire_minutes": settings.SMS_CODE_EXPIRE_MINUTES},
        message="验证码发送成功"
    )


@router.get("/info", response_model=CommonResponse[DriverResponse])
def get_driver_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取司机信息

    获取当前登录司机的详细信息。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[DriverResponse]: 司机信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    return create_success_response(data=DriverResponse.model_validate(driver))


@router.put("/info", response_model=CommonResponse[DriverResponse])
def update_driver_info(
    update_data: DriverUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 更新司机信息

    更新当前登录司机的详细信息。

    Args:
        update_data: 更新数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[DriverResponse]: 更新后的司机信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(driver, key, value)

    db.commit()
    db.refresh(driver)

    return create_success_response(data=DriverResponse.model_validate(driver), message="更新成功")


@router.post("/check-in", response_model=CommonResponse[AttendanceResponse])
def check_in(
    check_in_data: CheckInRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 上班打卡

    司机上班打卡，绑定车辆。

    Args:
        check_in_data: 打卡数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[AttendanceResponse]: 打卡记录
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == check_in_data.vehicle_id,
        Vehicle.status == 1
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="车辆不存在或不可用"
        )

    today = datetime.now().date()
    existing_attendance = db.query(Attendance).filter(
        Attendance.driver_id == driver.id,
        Attendance.attendance_date >= datetime.combine(today, datetime.min.time()),
        Attendance.attendance_date < datetime.combine(today + timedelta(days=1), datetime.min.time()),
        Attendance.check_in_time.isnot(None),
        Attendance.check_out_time.is_(None)
    ).first()

    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="今日已打卡上班，请先打卡下班"
        )

    now = datetime.now()
    attendance = Attendance(
        driver_id=driver.id,
        vehicle_id=vehicle.id,
        attendance_date=now,
        check_in_time=now,
        check_in_latitude=check_in_data.latitude,
        check_in_longitude=check_in_data.longitude,
        check_in_address=check_in_data.address,
        status=1,
    )
    db.add(attendance)

    existing_binding = db.query(DriverVehicle).filter(
        DriverVehicle.driver_id == driver.id,
        DriverVehicle.status == 1
    ).first()

    if existing_binding:
        if existing_binding.vehicle_id != vehicle.id:
            existing_binding.status = 0
            existing_binding.unbind_time = now
            new_binding = DriverVehicle(
                driver_id=driver.id,
                vehicle_id=vehicle.id,
                bind_time=now,
                status=1,
            )
            db.add(new_binding)
    else:
        new_binding = DriverVehicle(
            driver_id=driver.id,
            vehicle_id=vehicle.id,
            bind_time=now,
            status=1,
        )
        db.add(new_binding)

    db.commit()
    db.refresh(attendance)

    return create_success_response(data=AttendanceResponse.model_validate(attendance), message="打卡成功")


@router.post("/check-out", response_model=CommonResponse[AttendanceResponse])
def check_out(
    check_out_data: CheckInRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 下班打卡

    司机下班打卡。

    Args:
        check_out_data: 打卡数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[AttendanceResponse]: 打卡记录
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    today = datetime.now().date()
    attendance = db.query(Attendance).filter(
        Attendance.driver_id == driver.id,
        Attendance.attendance_date >= datetime.combine(today, datetime.min.time()),
        Attendance.attendance_date < datetime.combine(today + timedelta(days=1), datetime.min.time()),
        Attendance.check_in_time.isnot(None),
        Attendance.check_out_time.is_(None)
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="今日未打卡上班"
        )

    now = datetime.now()
    attendance.check_out_time = now
    attendance.check_out_latitude = check_out_data.latitude
    attendance.check_out_longitude = check_out_data.longitude
    attendance.check_out_address = check_out_data.address

    binding = db.query(DriverVehicle).filter(
        DriverVehicle.driver_id == driver.id,
        DriverVehicle.status == 1
    ).first()

    if binding:
        binding.status = 0
        binding.unbind_time = now

    db.commit()
    db.refresh(attendance)

    return create_success_response(data=AttendanceResponse.model_validate(attendance), message="打卡成功")


@router.get("/today-attendance", response_model=CommonResponse[AttendanceResponse])
def get_today_attendance(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取今日打卡记录

    获取今日的打卡记录。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[AttendanceResponse]: 打卡记录
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    today = datetime.now().date()
    attendance = db.query(Attendance).filter(
        Attendance.driver_id == driver.id,
        Attendance.attendance_date >= datetime.combine(today, datetime.min.time()),
        Attendance.attendance_date < datetime.combine(today + timedelta(days=1), datetime.min.time()),
    ).order_by(Attendance.created_at.desc()).first()

    if not attendance:
        return create_success_response(data=None, message="今日暂无打卡记录")

    return create_success_response(data=AttendanceResponse.model_validate(attendance))


@router.get("/current-vehicle", response_model=CommonResponse[VehicleResponse])
def get_current_vehicle(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取当前绑定车辆

    获取当前司机绑定的车辆信息。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[VehicleResponse]: 车辆信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    binding = db.query(DriverVehicle).filter(
        DriverVehicle.driver_id == driver.id,
        DriverVehicle.status == 1
    ).first()

    if not binding:
        return create_success_response(data=None, message="暂无绑定车辆")

    vehicle = db.query(Vehicle).filter(Vehicle.id == binding.vehicle_id).first()

    if not vehicle:
        return create_success_response(data=None, message="车辆信息不存在")

    return create_success_response(data=VehicleResponse.model_validate(vehicle))


@router.get("/messages", response_model=CommonResponse[MessageListResponse])
def get_messages(
    category_id: Optional[int] = Query(None, description="消息分类ID"),
    is_read: Optional[int] = Query(None, description="是否已读: 0-未读, 1-已读"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取消息列表

    获取当前司机的消息列表，支持按分类和已读状态筛选。

    Args:
        category_id: 消息分类ID
        is_read: 是否已读
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[MessageListResponse]: 消息列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        return create_success_response(data=MessageListResponse(unread_count=0, messages=[]))

    query = db.query(Message).filter(
        Message.message_type == settings.MESSAGE_TYPE_DRIVER,
        Message.receiver_id == driver.id,
    )

    if category_id is not None:
        query = query.filter(Message.category_id == category_id)

    if is_read is not None:
        query = query.filter(Message.is_read == is_read)

    unread_count = db.query(Message).filter(
        Message.message_type == settings.MESSAGE_TYPE_DRIVER,
        Message.receiver_id == driver.id,
        Message.is_read == 0
    ).count()

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    messages = query.order_by(Message.created_at.desc()).offset(offset).limit(page_size).all()

    message_responses = []
    for msg in messages:
        msg_resp = MessageResponse.model_validate(msg)
        if msg.category_id:
            category = db.query(MessageCategory).filter(MessageCategory.id == msg.category_id).first()
            if category:
                msg_resp.category_name = category.name
        message_responses.append(msg_resp)

    result = MessageListResponse(
        unread_count=unread_count,
        messages=message_responses,
    )

    return create_success_response(data=result)


@router.get("/messages/{message_id}", response_model=CommonResponse[MessageResponse])
def get_message_detail(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取消息详情

    获取指定消息的详细信息，并标记为已读。

    Args:
        message_id: 消息ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[MessageResponse]: 消息详情
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    message = db.query(Message).filter(
        Message.id == message_id,
        Message.message_type == settings.MESSAGE_TYPE_DRIVER,
        Message.receiver_id == driver.id,
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    if message.is_read == 0:
        message.is_read = 1
        message.read_time = datetime.now()
        db.commit()
        db.refresh(message)

    msg_resp = MessageResponse.model_validate(message)
    if message.category_id:
        category = db.query(MessageCategory).filter(MessageCategory.id == message.category_id).first()
        if category:
            msg_resp.category_name = category.name

    return create_success_response(data=msg_resp)


@router.get("/message-categories", response_model=CommonResponse[List[MessageCategoryResponse]])
def get_message_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取消息分类列表

    获取司机端所有的消息分类。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[List[MessageCategoryResponse]]: 消息分类列表
    """
    categories = db.query(MessageCategory).filter(
        MessageCategory.message_type == settings.MESSAGE_TYPE_DRIVER,
        MessageCategory.status == 1
    ).order_by(MessageCategory.sort_order).all()

    result = [MessageCategoryResponse.model_validate(cat) for cat in categories]

    return create_success_response(data=result)


@router.get("/dispatches", response_model=CommonResponse)
def get_dispatches(
    status: Optional[int] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取调度消息列表

    获取当前司机的调度消息列表。

    Args:
        status: 状态筛选
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 调度消息列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        return create_success_response(data={"items": [], "total": 0})

    query = db.query(Dispatch).filter(Dispatch.driver_id == driver.id)

    if status is not None:
        query = query.filter(Dispatch.status == status)

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    dispatches = query.order_by(Dispatch.created_at.desc()).offset(offset).limit(page_size).all()

    result = []
    for dispatch in dispatches:
        resp = DispatchResponse.model_validate(dispatch)
        if dispatch.route_id:
            route = db.query(Route).filter(Route.id == dispatch.route_id).first()
            if route:
                resp.route_name = route.route_name
        result.append(resp)

    return create_success_response(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": calculate_total_pages(total, page_size),
    })


@router.put("/dispatches/{dispatch_id}/status", response_model=CommonResponse[DispatchResponse])
def update_dispatch_status(
    dispatch_id: int,
    new_status: int = Query(..., description="新状态: 1-待接收, 2-已接收, 3-执行中, 4-已完成, 5-已取消"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 更新调度状态

    更新调度消息的状态。

    Args:
        dispatch_id: 调度ID
        new_status: 新状态
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[DispatchResponse]: 调度信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    dispatch = db.query(Dispatch).filter(
        Dispatch.id == dispatch_id,
        Dispatch.driver_id == driver.id,
    ).first()

    if not dispatch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="调度消息不存在"
        )

    dispatch.status = new_status

    if new_status == 4:
        dispatch.actual_arrival_time = datetime.now()

    db.commit()
    db.refresh(dispatch)

    resp = DispatchResponse.model_validate(dispatch)
    if dispatch.route_id:
        route = db.query(Route).filter(Route.id == dispatch.route_id).first()
        if route:
            resp.route_name = route.route_name

    return create_success_response(data=resp, message="更新成功")


@router.post("/feedbacks", response_model=CommonResponse[FeedbackResponse])
def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 提交反馈

    司机提交处理结果反馈或车辆保养反馈。

    Args:
        feedback_data: 反馈数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[FeedbackResponse]: 反馈信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    import json
    images_json = json.dumps(feedback_data.images) if feedback_data.images else None

    feedback = Feedback(
        driver_id=driver.id,
        vehicle_id=feedback_data.vehicle_id,
        feedback_type=feedback_data.feedback_type,
        title=feedback_data.title,
        content=feedback_data.content,
        images=images_json,
        related_message_id=feedback_data.related_message_id,
        status=1,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return create_success_response(data=FeedbackResponse.model_validate(feedback), message="提交成功")


@router.get("/feedbacks", response_model=CommonResponse)
def get_feedbacks(
    feedback_type: Optional[int] = Query(None, description="反馈类型"),
    status: Optional[int] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取反馈列表

    获取当前司机的反馈列表。

    Args:
        feedback_type: 反馈类型筛选
        status: 状态筛选
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 反馈列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        return create_success_response(data={"items": [], "total": 0})

    query = db.query(Feedback).filter(Feedback.driver_id == driver.id)

    if feedback_type is not None:
        query = query.filter(Feedback.feedback_type == feedback_type)

    if status is not None:
        query = query.filter(Feedback.status == status)

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    feedbacks = query.order_by(Feedback.created_at.desc()).offset(offset).limit(page_size).all()

    result = [FeedbackResponse.model_validate(fb) for fb in feedbacks]

    return create_success_response(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": calculate_total_pages(total, page_size),
    })


@router.post("/emergencies", response_model=CommonResponse[EmergencyResponse])
def submit_emergency(
    emergency_data: EmergencyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 提交紧急状况申请

    司机提交紧急状况申请。

    Args:
        emergency_data: 紧急状况数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[EmergencyResponse]: 紧急状况信息
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    import json
    images_json = json.dumps(emergency_data.images) if emergency_data.images else None

    emergency = Emergency(
        driver_id=driver.id,
        vehicle_id=emergency_data.vehicle_id,
        emergency_type=emergency_data.emergency_type,
        title=emergency_data.title,
        content=emergency_data.content,
        latitude=emergency_data.latitude,
        longitude=emergency_data.longitude,
        location_address=emergency_data.location_address,
        images=images_json,
        status=1,
    )
    db.add(emergency)
    db.commit()
    db.refresh(emergency)

    return create_success_response(data=EmergencyResponse.model_validate(emergency), message="提交成功")


@router.get("/emergencies", response_model=CommonResponse)
def get_emergencies(
    status: Optional[int] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取紧急状况列表

    获取当前司机的紧急状况列表。

    Args:
        status: 状态筛选
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 紧急状况列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        return create_success_response(data={"items": [], "total": 0})

    query = db.query(Emergency).filter(Emergency.driver_id == driver.id)

    if status is not None:
        query = query.filter(Emergency.status == status)

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    emergencies = query.order_by(Emergency.created_at.desc()).offset(offset).limit(page_size).all()

    result = [EmergencyResponse.model_validate(em) for em in emergencies]

    return create_success_response(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": calculate_total_pages(total, page_size),
    })


@router.get("/routes", response_model=CommonResponse[List[RouteResponse]])
def get_routes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取路线列表

    获取所有可用的路线信息。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[List[RouteResponse]]: 路线列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    routes = db.query(Route).filter(
        Route.status == 1
    ).order_by(Route.route_name).all()

    result = [RouteResponse.model_validate(route) for route in routes]

    return create_success_response(data=result)


@router.get("/routes/{route_id}", response_model=CommonResponse[RouteResponse])
def get_route_detail(
    route_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取路线详情

    获取指定路线的详细信息。

    Args:
        route_id: 路线ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[RouteResponse]: 路线详情
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    route = db.query(Route).filter(
        Route.id == route_id,
        Route.status == 1
    ).first()

    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="路线不存在"
        )

    return create_success_response(data=RouteResponse.model_validate(route))


@router.get("/violations", response_model=CommonResponse)
def get_violations(
    status: Optional[int] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取违章记录列表

    获取当前司机的违章记录列表。

    Args:
        status: 状态筛选
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 违章记录列表
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        return create_success_response(data={"items": [], "total": 0})

    query = db.query(Violation).filter(Violation.driver_id == driver.id)

    if status is not None:
        query = query.filter(Violation.status == status)

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    violations = query.order_by(Violation.violation_time.desc()).offset(offset).limit(page_size).all()

    result = [ViolationResponse.model_validate(v) for v in violations]

    return create_success_response(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": calculate_total_pages(total, page_size),
    })


@router.get("/violations/{violation_id}", response_model=CommonResponse[ViolationResponse])
def get_violation_detail(
    violation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    司机端 - 获取违章详情

    获取指定违章的详细信息。

    Args:
        violation_id: 违章ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[ViolationResponse]: 违章详情
    """
    if current_user.user_type != settings.USER_TYPE_DRIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="司机信息不存在"
        )

    violation = db.query(Violation).filter(
        Violation.id == violation_id,
        Violation.driver_id == driver.id,
    ).first()

    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="违章记录不存在"
        )

    return create_success_response(data=ViolationResponse.model_validate(violation))
