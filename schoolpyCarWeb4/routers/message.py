"""
校车管理系统 - 消息推送和状态API路由
提供学生、消息推送和校车状态相关的RESTful API接口
"""
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, HTTPException

from models.message import (
    StudentCreate, StudentUpdate, StudentResponse,
    MessagePushCreate, MessagePushResponse, MessagePushWithStudent,
    BusStatusCreate, BusStatusResponse, BusStatusWithDetails,
    BusDepartureRequest, BusArrivalRequest, BusAbnormalRequest
)
from dao.message_dao import StudentDAO, MessagePushDAO, BusStatusDAO
from dao.maintenance_dao import VehicleDAO
from dao.driver_dao import DriverDAO

# 创建路由
router = APIRouter(prefix="/api/messages", tags=["消息推送和状态"])


# ============ 学生管理 ============

@router.get("/students/", response_model=List[StudentResponse])
def get_students():
    """
    获取所有学生列表
    """
    students = StudentDAO.get_all()
    return students


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    """
    根据ID获取学生信息
    """
    student = StudentDAO.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return student


@router.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate):
    """
    创建新学生
    """
    student_id = StudentDAO.create(
        name=student.name,
        student_no=student.student_no,
        class_name=student.class_name,
        card_id=student.card_id,
        parent_phone=student.parent_phone,
        status=student.status
    )
    return StudentDAO.get_by_id(student_id)


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    """
    更新学生信息
    """
    # 检查学生是否存在
    existing = StudentDAO.get_by_id(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="学生不存在")
    
    # 构建更新字段
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    if update_data:
        StudentDAO.update(student_id, **update_data)
    
    return StudentDAO.get_by_id(student_id)


@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    删除学生
    """
    existing = StudentDAO.get_by_id(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="学生不存在")
    
    success = StudentDAO.delete(student_id)
    if success:
        return {"message": "删除成功", "success": True}
    raise HTTPException(status_code=500, detail="删除失败")


# ============ 消息推送记录管理 ============

@router.get("/push-logs/", response_model=List[MessagePushWithStudent])
def get_message_push_logs(
    student_id: Optional[int] = None,
    message_type: Optional[str] = None,
    limit: int = 100
):
    """
    获取消息推送记录列表
    - student_id: 指定学生ID
    - message_type: 消息类型（上车刷卡、下车刷卡、校车发车、校车到站、异常通知）
    - limit: 返回记录数量
    """
    if student_id:
        logs = MessagePushDAO.get_by_student(student_id, limit)
    elif message_type:
        logs = MessagePushDAO.get_by_type(message_type, limit)
    else:
        logs = MessagePushDAO.get_all()
    return logs[:limit]


@router.get("/push-logs/recent")
def get_recent_push_logs(hours: int = 24):
    """
    获取最近N小时的消息推送记录
    """
    logs = MessagePushDAO.get_recent(hours)
    return {
        "hours": hours,
        "count": len(logs),
        "logs": logs
    }


@router.get("/push-logs/{log_id}", response_model=MessagePushWithStudent)
def get_message_push_log(log_id: int):
    """
    根据ID获取消息推送记录
    """
    log = MessagePushDAO.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="消息推送记录不存在")
    return log


@router.post("/swipe-card")
def student_swipe_card(
    card_id: str,
    swipe_type: str,  # "上车" 或 "下车"
    location: str = None
):
    """
    学生刷卡上下车接口
    - card_id: 学生卡号
    - swipe_type: 刷卡类型（"上车" 或 "下车"）
    - location: 刷卡位置（可选）
    
    流程：
    1. 根据卡号查询学生信息
    2. 记录学生刷卡事件
    3. 生成消息推送记录（模拟家长端推送）
    """
    # 根据卡号查询学生
    student = StudentDAO.get_by_card(card_id)
    if not student:
        raise HTTPException(status_code=404, detail="未找到对应学生信息")
    
    # 确定消息类型和内容
    if swipe_type == "上车":
        message_type = "上车刷卡"
        content = f"学生{student['name']}已刷卡上车，请知悉"
    elif swipe_type == "下车":
        message_type = "下车刷卡"
        content = f"学生{student['name']}已刷卡下车，请知悉"
    else:
        raise HTTPException(status_code=400, detail="刷卡类型错误，应为'上车'或'下车'")
    
    # 创建消息推送记录（模拟推送）
    push_time = datetime.now()
    log_id = MessagePushDAO.create(
        student_id=student['id'],
        message_type=message_type,
        content=content,
        push_time=push_time,
        status="sent",
        receiver_phone=student['parent_phone']
    )
    
    return {
        "message": "刷卡成功",
        "student": {
            "id": student['id'],
            "name": student['name'],
            "class_name": student['class_name']
        },
        "swipe_type": swipe_type,
        "location": location,
        "push_record_id": log_id,
        "push_time": push_time.isoformat(),
        "parent_phone": student['parent_phone']
    }


# ============ 校车状态管理 ============

@router.get("/bus-status/", response_model=List[BusStatusWithDetails])
def get_bus_status_logs(
    vehicle_id: Optional[int] = None,
    status_type: Optional[str] = None,
    limit: int = 100
):
    """
    获取校车状态记录列表
    - vehicle_id: 指定车辆ID
    - status_type: 状态类型（发车、到站、正常、异常）
    - limit: 返回记录数量
    """
    if vehicle_id:
        logs = BusStatusDAO.get_by_vehicle(vehicle_id, limit)
    elif status_type:
        logs = BusStatusDAO.get_by_type(status_type, limit)
    else:
        logs = BusStatusDAO.get_all()
    return logs[:limit]


@router.get("/bus-status/recent")
def get_recent_bus_status(hours: int = 24):
    """
    获取最近N小时的校车状态记录
    """
    logs = BusStatusDAO.get_recent(hours)
    return {
        "hours": hours,
        "count": len(logs),
        "logs": logs
    }


@router.get("/bus-status/{status_id}", response_model=BusStatusWithDetails)
def get_bus_status(status_id: int):
    """
    根据ID获取校车状态记录
    """
    status = BusStatusDAO.get_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="校车状态记录不存在")
    return status


@router.get("/vehicles/{vehicle_id}/current-status")
def get_vehicle_current_status(vehicle_id: int):
    """
    获取指定车辆的当前状态
    """
    # 检查车辆是否存在
    vehicle = VehicleDAO.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    current_status = BusStatusDAO.get_current_status(vehicle_id)
    
    return {
        "vehicle": {
            "id": vehicle['id'],
            "plate_number": vehicle['plate_number'],
            "vehicle_type": vehicle['vehicle_type']
        },
        "current_status": current_status
    }


@router.post("/bus-status/departure")
def record_bus_departure(request: BusDepartureRequest):
    """
    记录校车发车
    - vehicle_id: 车辆ID
    - driver_id: 司机ID（可选）
    - location: 发车位置，默认"学校"
    """
    vehicle = VehicleDAO.get_by_id(request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    driver_name = None
    if request.driver_id:
        driver = DriverDAO.get_by_id(request.driver_id)
        if driver:
            driver_name = driver['name']
    
    status_id = BusStatusDAO.create(
        vehicle_id=request.vehicle_id,
        driver_id=request.driver_id,
        status_type="发车",
        status_value="已发车",
        location=request.location,
        description=f"校车从{request.location}发车"
    )
    
    MessagePushDAO.create(
        message_type="校车发车",
        content=f"校车{vehicle['plate_number']}已从{request.location}发车",
        status="sent"
    )
    
    return {
        "message": "发车记录成功",
        "status_id": status_id,
        "vehicle": {
            "id": vehicle['id'],
            "plate_number": vehicle['plate_number']
        },
        "driver": {
            "id": request.driver_id,
            "name": driver_name
        } if request.driver_id else None,
        "location": request.location,
        "record_time": datetime.now().isoformat()
    }


@router.post("/bus-status/arrival")
def record_bus_arrival(request: BusArrivalRequest):
    """
    记录校车到站
    - vehicle_id: 车辆ID
    - driver_id: 司机ID（可选）
    - location: 到站位置，默认"学校"
    """
    vehicle = VehicleDAO.get_by_id(request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    status_id = BusStatusDAO.create(
        vehicle_id=request.vehicle_id,
        driver_id=request.driver_id,
        status_type="到站",
        status_value="已到站",
        location=request.location,
        description=f"校车到达{request.location}"
    )
    
    MessagePushDAO.create(
        message_type="校车到站",
        content=f"校车{vehicle['plate_number']}已到达{request.location}",
        status="sent"
    )
    
    return {
        "message": "到站记录成功",
        "status_id": status_id,
        "vehicle": {
            "id": vehicle['id'],
            "plate_number": vehicle['plate_number']
        },
        "location": request.location,
        "record_time": datetime.now().isoformat()
    }


@router.post("/bus-status/abnormal")
def record_bus_abnormal(request: BusAbnormalRequest):
    """
    记录校车异常状态
    - vehicle_id: 车辆ID
    - abnormal_type: 异常类型（绕行、迟到、临时停车、道路拥堵等）
    - driver_id: 司机ID（可选）
    - location: 位置（可选）
    - description: 详细描述（可选）
    
    异常状态会自动通知家长
    """
    vehicle = VehicleDAO.get_by_id(request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="车辆不存在")
    
    status_id = BusStatusDAO.create(
        vehicle_id=request.vehicle_id,
        driver_id=request.driver_id,
        status_type="异常",
        status_value=request.abnormal_type,
        location=request.location,
        description=request.description or f"校车出现{request.abnormal_type}情况"
    )
    
    MessagePushDAO.create(
        message_type="异常通知",
        content=f"校车{vehicle['plate_number']}出现{request.abnormal_type}情况，请留意",
        status="sent"
    )
    
    return {
        "message": "异常状态记录成功，已推送通知",
        "status_id": status_id,
        "vehicle": {
            "id": vehicle['id'],
            "plate_number": vehicle['plate_number']
        },
        "abnormal_type": request.abnormal_type,
        "location": request.location,
        "description": request.description,
        "record_time": datetime.now().isoformat()
    }
