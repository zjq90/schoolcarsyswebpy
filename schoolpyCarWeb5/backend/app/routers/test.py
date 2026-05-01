"""
测试路由
用于生成测试数据和测试功能
"""

from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import (
    User, Bus, Driver, Student,
    AlarmLevel, AlarmType, Alarm, Location
)

router = APIRouter(prefix="/api/test", tags=["测试功能"])


@router.post("/generate-all")
def generate_all_test_data(db: Session = Depends(get_db)):
    """
    生成所有测试数据
    包括：用户、司机、校车、学生、报警级别、报警类型
    """
    
    # 生成报警级别
    generate_alarm_levels(db)
    
    # 生成报警类型
    generate_alarm_types(db)
    
    # 生成用户
    generate_users(db)
    
    # 生成司机
    generate_drivers(db)
    
    # 生成校车
    generate_buses(db)
    
    # 生成学生
    generate_students(db)
    
    # 生成位置记录
    generate_locations(db)
    
    return {
        "message": "所有测试数据生成成功",
        "timestamp": datetime.now().isoformat()
    }


def generate_alarm_levels(db: Session):
    """生成报警级别数据"""
    existing = db.query(AlarmLevel).count()
    if existing > 0:
        return
    
    levels = [
        {
            "level": 1,
            "name": "一级报警",
            "color": "red",
            "description": "事故、火灾、劫持等紧急情况",
            "response_mechanism": "一键报警 → 监控中心 → 警方联动"
        },
        {
            "level": 2,
            "name": "二级报警",
            "color": "orange",
            "description": "超速、偏离路线、长时间停留、有病情",
            "response_mechanism": "自动录音录像 → 推送至学校管理员"
        },
        {
            "level": 3,
            "name": "三级报警",
            "color": "blue",
            "description": "车门异常开启、学生滞留、一般违规行为",
            "response_mechanism": "提醒司机复核 → 推送家长确认"
        }
    ]
    
    for level_data in levels:
        level = AlarmLevel(**level_data)
        db.add(level)
    
    db.commit()


def generate_alarm_types(db: Session):
    """生成报警类型数据"""
    existing = db.query(AlarmType).count()
    if existing > 0:
        return
    
    # 获取级别ID
    level1 = db.query(AlarmLevel).filter(AlarmLevel.level == 1).first()
    level2 = db.query(AlarmLevel).filter(AlarmLevel.level == 2).first()
    level3 = db.query(AlarmLevel).filter(AlarmLevel.level == 3).first()
    
    types = [
        # 一级报警类型
        {
            "name": "交通事故",
            "level_id": level1.id if level1 else 1,
            "description": "校车发生交通事故",
            "trigger_condition": "一键报警按钮触发",
            "is_auto": False
        },
        {
            "name": "火灾警报",
            "level_id": level1.id if level1 else 1,
            "description": "校车发生火灾",
            "trigger_condition": "一键报警按钮触发或烟雾传感器",
            "is_auto": False
        },
        {
            "name": "劫持警报",
            "level_id": level1.id if level1 else 1,
            "description": "校车被劫持",
            "trigger_condition": "一键报警按钮触发",
            "is_auto": False
        },
        # 二级报警类型
        {
            "name": "超速行驶",
            "level_id": level2.id if level2 else 2,
            "description": "校车超速行驶",
            "trigger_condition": "车速超过限速阈值",
            "is_auto": True
        },
        {
            "name": "偏离路线",
            "level_id": level2.id if level2 else 2,
            "description": "校车偏离预设路线",
            "trigger_condition": "GPS位置偏离预设路线",
            "is_auto": True
        },
        {
            "name": "长时间停留",
            "level_id": level2.id if level2 else 2,
            "description": "校车长时间停留",
            "trigger_condition": "停车时间超过阈值",
            "is_auto": True
        },
        {
            "name": "学生病情",
            "level_id": level2.id if level2 else 2,
            "description": "车上有学生突发病情",
            "trigger_condition": "司机手动触发",
            "is_auto": False
        },
        # 三级报警类型
        {
            "name": "车门异常开启",
            "level_id": level3.id if level3 else 3,
            "description": "车门在行驶中异常开启",
            "trigger_condition": "车门传感器检测",
            "is_auto": True
        },
        {
            "name": "学生滞留",
            "level_id": level3.id if level3 else 3,
            "description": "学生滞留在校车上",
            "trigger_condition": "下车时间超过阈值仍有学生在车上",
            "is_auto": True
        },
        {
            "name": "一般违规行为",
            "level_id": level3.id if level3 else 3,
            "description": "一般违规行为",
            "trigger_condition": "司机或管理员手动记录",
            "is_auto": False
        }
    ]
    
    for type_data in types:
        alarm_type = AlarmType(**type_data)
        db.add(alarm_type)
    
    db.commit()


def generate_users(db: Session):
    """生成用户数据"""
    existing = db.query(User).count()
    if existing > 0:
        return
    
    import hashlib
    
    users = [
        {
            "username": "admin",
            "password": hashlib.md5("admin123".encode()).hexdigest(),
            "real_name": "系统管理员",
            "phone": "13800138000",
            "email": "admin@schoolbus.com",
            "role": "admin",
            "status": True
        },
        {
            "username": "school_admin",
            "password": hashlib.md5("school123".encode()).hexdigest(),
            "real_name": "学校管理员",
            "phone": "13800138001",
            "email": "school@schoolbus.com",
            "role": "school_admin",
            "status": True
        }
    ]
    
    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    db.commit()


def generate_drivers(db: Session):
    """生成司机数据"""
    existing = db.query(Driver).count()
    if existing > 0:
        return
    
    drivers = [
        {
            "name": "张师傅",
            "phone": "13900139001",
            "id_card": "110101198001010001",
            "license_number": "A12345678901",
            "license_type": "A1",
            "status": True
        },
        {
            "name": "李师傅",
            "phone": "13900139002",
            "id_card": "110101198001010002",
            "license_number": "A12345678902",
            "license_type": "A1",
            "status": True
        },
        {
            "name": "王师傅",
            "phone": "13900139003",
            "id_card": "110101198001010003",
            "license_number": "A12345678903",
            "license_type": "A1",
            "status": True
        }
    ]
    
    for driver_data in drivers:
        driver = Driver(**driver_data)
        db.add(driver)
    
    db.commit()


def generate_buses(db: Session):
    """生成校车数据"""
    existing = db.query(Bus).count()
    if existing > 0:
        return
    
    # 获取司机
    drivers = db.query(Driver).all()
    
    buses = [
        {
            "plate_number": "京A12345",
            "bus_number": "XC001",
            "model": "宇通ZK6120",
            "capacity": 45,
            "status": "running",
            "current_latitude": 39.9042,
            "current_longitude": 116.4074
        },
        {
            "plate_number": "京A12346",
            "bus_number": "XC002",
            "model": "宇通ZK6120",
            "capacity": 45,
            "status": "idle",
            "current_latitude": 39.9142,
            "current_longitude": 116.4174
        },
        {
            "plate_number": "京A12347",
            "bus_number": "XC003",
            "model": "宇通ZK6850",
            "capacity": 35,
            "status": "running",
            "current_latitude": 39.9242,
            "current_longitude": 116.4274
        }
    ]
    
    for i, bus_data in enumerate(buses):
        if i < len(drivers):
            bus_data["driver_id"] = drivers[i].id
        bus = Bus(**bus_data)
        db.add(bus)
    
    db.commit()


def generate_students(db: Session):
    """生成学生数据"""
    existing = db.query(Student).count()
    if existing > 0:
        return
    
    # 获取校车
    buses = db.query(Bus).all()
    
    student_names = ["小明", "小红", "小刚", "小丽", "小强", "小美", "小宇", "小欣", "小泽", "小琳"]
    class_names = ["一年级1班", "一年级2班", "二年级1班", "二年级2班", "三年级1班"]
    
    for i in range(20):
        student_data = {
            "name": student_names[i % len(student_names)] + str(i + 1),
            "student_number": f"STU{20240001 + i}",
            "class_name": class_names[i % len(class_names)],
            "school": "北京市实验小学",
            "parent_name": f"家长{i + 1}",
            "parent_phone": f"1360000{str(1001 + i).zfill(4)}",
            "bus_id": buses[i % len(buses)].id if buses else None,
            "status": True
        }
        student = Student(**student_data)
        db.add(student)
    
    db.commit()


def generate_locations(db: Session):
    """生成位置记录数据"""
    existing = db.query(Location).count()
    if existing > 0:
        return
    
    # 获取校车
    buses = db.query(Bus).all()
    
    for bus in buses:
        # 为每个校车生成10条位置记录
        base_lat = bus.current_latitude or 39.9042
        base_lng = bus.current_longitude or 116.4074
        
        for i in range(10):
            # 生成模拟的位置变化
            lat_offset = random.uniform(-0.01, 0.01)
            lng_offset = random.uniform(-0.01, 0.01)
            
            location_data = {
                "bus_id": bus.id,
                "latitude": base_lat + lat_offset,
                "longitude": base_lng + lng_offset,
                "location_name": f"位置点{i + 1}",
                "speed": random.uniform(30, 60),
                "direction": random.randint(0, 360)
            }
            location = Location(**location_data)
            db.add(location)
    
    db.commit()


@router.post("/trigger-alarm")
def trigger_test_alarm(
    type_id: int = 1,
    bus_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    触发测试报警
    用于测试报警功能
    """
    import time
    
    # 检查报警类型是否存在
    alarm_type = db.query(AlarmType).filter(AlarmType.id == type_id).first()
    if not alarm_type:
        return {"error": "报警类型不存在"}
    
    # 检查校车是否存在
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        return {"error": "校车不存在"}
    
    # 生成报警编号
    alarm_number = f"TEST{int(time.time())}{random.randint(1000, 9999)}"
    
    # 创建报警记录
    db_alarm = Alarm(
        alarm_number=alarm_number,
        type_id=type_id,
        level_id=alarm_type.level_id,
        bus_id=bus_id,
        driver_id=bus.driver_id,
        latitude=bus.current_latitude,
        longitude=bus.current_longitude,
        location_name="测试位置",
        status="pending",
        is_read=False,
        description=f"测试报警 - {alarm_type.description}",
        triggered_at=datetime.now()
    )
    
    db.add(db_alarm)
    db.commit()
    db.refresh(db_alarm)
    
    return {
        "message": "测试报警触发成功",
        "alarm_id": db_alarm.id,
        "alarm_number": db_alarm.alarm_number,
        "level_id": db_alarm.level_id,
        "type_name": alarm_type.name,
        "bus_plate": bus.plate_number
    }


@router.get("/reset")
def reset_test_data(db: Session = Depends(get_db)):
    """
    重置测试数据
    清空所有数据（除了报警级别和报警类型）
    """
    # 删除报警记录
    db.query(Alarm).delete()
    # 删除位置记录
    db.query(Location).delete()
    # 删除学生
    db.query(Student).delete()
    # 删除校车
    db.query(Bus).delete()
    # 删除司机
    db.query(Driver).delete()
    # 删除用户（保留admin）
    db.query(User).filter(User.username != "admin").delete()
    
    db.commit()
    
    return {
        "message": "测试数据已重置",
        "timestamp": datetime.now().isoformat()
    }
