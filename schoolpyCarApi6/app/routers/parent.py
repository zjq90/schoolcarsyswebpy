"""
家长端API路由
==============

包含家长端所有的API接口:
- 登录/注册
- 学生绑定
- 消息列表/详情
- 消息分类查询
- 投诉提交
"""

from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.config import settings
from app.models import (
    User, Parent, Student, ParentStudent, Message, MessageCategory, Complaint
)
from app.schemas import (
    UserLogin, UserLoginByCode, UserResponse, Token,
    ParentCreate, ParentUpdate, ParentResponse,
    StudentBindRequest, StudentWithRelationResponse,
    MessageResponse, MessageListResponse, MessageCategoryResponse,
    ComplaintCreate, ComplaintResponse,
    CommonResponse, PaginationParams,
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


router = APIRouter(prefix="/api/parent", tags=["家长端"])


@router.post("/login/password", response_model=CommonResponse[Token])
def login_by_password(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    家长端 - 密码登录

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
        User.user_type == settings.USER_TYPE_PARENT
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
    家长端 - 验证码登录

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
        User.user_type == settings.USER_TYPE_PARENT
    ).first()

    if not user:
        user = User(
            phone=phone,
            user_type=settings.USER_TYPE_PARENT,
            nickname=f"家长{phone[-4:]}",
            status=1,
        )
        db.add(user)
        db.flush()

        parent = Parent(
            user_id=user.id,
            status=1,
        )
        db.add(parent)

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
    家长端 - 发送短信验证码

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


@router.get("/info", response_model=CommonResponse[ParentResponse])
def get_parent_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 获取家长信息

    获取当前登录家长的详细信息。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[ParentResponse]: 家长信息
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    return create_success_response(data=ParentResponse.model_validate(parent))


@router.put("/info", response_model=CommonResponse[ParentResponse])
def update_parent_info(
    update_data: ParentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 更新家长信息

    更新当前登录家长的详细信息。

    Args:
        update_data: 更新数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[ParentResponse]: 更新后的家长信息
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(parent, key, value)

    db.commit()
    db.refresh(parent)

    return create_success_response(data=ParentResponse.model_validate(parent), message="更新成功")


@router.post("/student/bind", response_model=CommonResponse)
def bind_student(
    bind_data: StudentBindRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 绑定学生

    绑定学生到当前家长账号。

    Args:
        bind_data: 绑定数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 绑定结果
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    student = None
    if bind_data.student_no:
        student = db.query(Student).filter(
            Student.student_no == bind_data.student_no,
            Student.real_name == bind_data.real_name
        ).first()

    if not student:
        student = db.query(Student).filter(
            Student.real_name == bind_data.real_name
        ).first()

    if not student:
        student = Student(
            real_name=bind_data.real_name,
            student_no=bind_data.student_no,
            status=1,
        )
        db.add(student)
        db.flush()

    existing = db.query(ParentStudent).filter(
        ParentStudent.parent_id == parent.id,
        ParentStudent.student_id == student.id,
        ParentStudent.status == 1
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学生已绑定"
        )

    parent_student = ParentStudent(
        parent_id=parent.id,
        student_id=student.id,
        relation=bind_data.relation,
        status=1,
    )
    db.add(parent_student)
    db.commit()

    return create_success_response(message="绑定成功")


@router.get("/students", response_model=CommonResponse[List[StudentWithRelationResponse]])
def get_bound_students(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 获取绑定的学生列表

    获取当前家长绑定的所有学生信息。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[List[StudentWithRelationResponse]]: 学生列表
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        return create_success_response(data=[])

    bindings = db.query(ParentStudent).filter(
        ParentStudent.parent_id == parent.id,
        ParentStudent.status == 1
    ).all()

    result = []
    for binding in bindings:
        student = db.query(Student).filter(Student.id == binding.student_id).first()
        if student:
            student_data = StudentWithRelationResponse.model_validate(student)
            student_data.relation = binding.relation
            result.append(student_data)

    return create_success_response(data=result)


@router.delete("/student/{student_id}", response_model=CommonResponse)
def unbind_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 解绑学生

    解除与指定学生的绑定关系。

    Args:
        student_id: 学生ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 解绑结果
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    binding = db.query(ParentStudent).filter(
        ParentStudent.parent_id == parent.id,
        ParentStudent.student_id == student_id,
        ParentStudent.status == 1
    ).first()

    if not binding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="绑定关系不存在"
        )

    binding.status = 0
    db.commit()

    return create_success_response(message="解绑成功")


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
    家长端 - 获取消息列表

    获取当前家长的消息列表，支持按分类和已读状态筛选。

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
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        return create_success_response(data=MessageListResponse(unread_count=0, messages=[]))

    query = db.query(Message).filter(
        Message.message_type == settings.MESSAGE_TYPE_PARENT,
        Message.receiver_id == parent.id,
    )

    if category_id is not None:
        query = query.filter(Message.category_id == category_id)

    if is_read is not None:
        query = query.filter(Message.is_read == is_read)

    unread_count = db.query(Message).filter(
        Message.message_type == settings.MESSAGE_TYPE_PARENT,
        Message.receiver_id == parent.id,
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
    家长端 - 获取消息详情

    获取指定消息的详细信息，并标记为已读。

    Args:
        message_id: 消息ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[MessageResponse]: 消息详情
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    message = db.query(Message).filter(
        Message.id == message_id,
        Message.message_type == settings.MESSAGE_TYPE_PARENT,
        Message.receiver_id == parent.id,
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


@router.put("/messages/{message_id}/read", response_model=CommonResponse)
def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 标记消息已读

    将指定消息标记为已读。

    Args:
        message_id: 消息ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 操作结果
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    message = db.query(Message).filter(
        Message.id == message_id,
        Message.message_type == settings.MESSAGE_TYPE_PARENT,
        Message.receiver_id == parent.id,
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    message.is_read = 1
    message.read_time = datetime.now()
    db.commit()

    return create_success_response(message="标记成功")


@router.get("/message-categories", response_model=CommonResponse[List[MessageCategoryResponse]])
def get_message_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 获取消息分类列表

    获取家长端所有的消息分类。

    Args:
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[List[MessageCategoryResponse]]: 消息分类列表
    """
    categories = db.query(MessageCategory).filter(
        MessageCategory.message_type == settings.MESSAGE_TYPE_PARENT,
        MessageCategory.status == 1
    ).order_by(MessageCategory.sort_order).all()

    result = [MessageCategoryResponse.model_validate(cat) for cat in categories]

    return create_success_response(data=result)


@router.post("/complaints", response_model=CommonResponse[ComplaintResponse])
def submit_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 提交投诉

    家长提交投诉信息。

    Args:
        complaint_data: 投诉数据
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[ComplaintResponse]: 投诉信息
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    import json
    images_json = json.dumps(complaint_data.images) if complaint_data.images else None

    complaint = Complaint(
        parent_id=parent.id,
        student_id=complaint_data.student_id,
        title=complaint_data.title,
        content=complaint_data.content,
        images=images_json,
        complaint_type=complaint_data.complaint_type,
        status=1,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    resp = ComplaintResponse.model_validate(complaint)
    if complaint.student_id:
        student = db.query(Student).filter(Student.id == complaint.student_id).first()
        if student:
            resp.student_name = student.real_name

    return create_success_response(data=resp, message="提交成功")


@router.get("/complaints", response_model=CommonResponse)
def get_complaints(
    status: Optional[int] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 获取投诉列表

    获取当前家长的投诉列表。

    Args:
        status: 状态筛选
        page: 页码
        page_size: 每页数量
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse: 投诉列表
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        return create_success_response(data={"items": [], "total": 0})

    query = db.query(Complaint).filter(Complaint.parent_id == parent.id)

    if status is not None:
        query = query.filter(Complaint.status == status)

    total = query.count()
    offset = calculate_page_offset(page, page_size)
    complaints = query.order_by(Complaint.created_at.desc()).offset(offset).limit(page_size).all()

    result = []
    for complaint in complaints:
        resp = ComplaintResponse.model_validate(complaint)
        if complaint.student_id:
            student = db.query(Student).filter(Student.id == complaint.student_id).first()
            if student:
                resp.student_name = student.real_name
        result.append(resp)

    return create_success_response(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": calculate_total_pages(total, page_size),
    })


@router.get("/complaints/{complaint_id}", response_model=CommonResponse[ComplaintResponse])
def get_complaint_detail(
    complaint_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    家长端 - 获取投诉详情

    获取指定投诉的详细信息。

    Args:
        complaint_id: 投诉ID
        current_user: 当前登录用户
        db: 数据库会话

    Returns:
        CommonResponse[ComplaintResponse]: 投诉详情
    """
    if current_user.user_type != settings.USER_TYPE_PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问"
        )

    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()

    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家长信息不存在"
        )

    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.parent_id == parent.id,
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="投诉不存在"
        )

    resp = ComplaintResponse.model_validate(complaint)
    if complaint.student_id:
        student = db.query(Student).filter(Student.id == complaint.student_id).first()
        if student:
            resp.student_name = student.real_name

    return create_success_response(data=resp)
