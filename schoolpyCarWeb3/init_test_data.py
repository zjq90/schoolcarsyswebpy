import sys
import os
from datetime import datetime, date, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import (
    User, UserRole, Bus, BusStatus, Route, RouteStatus,
    DriverBehavior, DriverBehaviorType, BehaviorSeverity,
    StudentBehavior, StudentBehaviorType,
    Capture, CaptureType, Duty, DutyStatus,
    TrafficData, TrafficCondition
)
from routers.auth import get_password_hash


def init_test_data():
    db = SessionLocal()
    
    try:
        init_db()
        print("数据库初始化完成")
        
        if db.query(User).count() > 0:
            print("测试数据已存在，跳过初始化")
            db.close()
            return
        
        print("开始创建测试数据...")
        
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            real_name="系统管理员",
            phone="13800138000",
            email="admin@school.com",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.flush()
        print(f"创建管理员用户: admin / admin123")
        
        driver_names = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]
        drivers = []
        for i, name in enumerate(driver_names):
            driver = User(
                username=f"driver{i+1}",
                password_hash=get_password_hash("123456"),
                real_name=name,
                phone=f"1390013800{i+1}",
                email=f"driver{i+1}@school.com",
                role=UserRole.DRIVER,
                is_active=True
            )
            db.add(driver)
            drivers.append(driver)
        db.flush()
        print(f"创建 {len(drivers)} 个司机用户")
        
        teacher_names = ["王老师", "李老师", "张老师"]
        teachers = []
        for i, name in enumerate(teacher_names):
            teacher = User(
                username=f"teacher{i+1}",
                password_hash=get_password_hash("123456"),
                real_name=name,
                phone=f"1370013800{i+1}",
                email=f"teacher{i+1}@school.com",
                role=UserRole.TEACHER,
                is_active=True
            )
            db.add(teacher)
            teachers.append(teacher)
        db.flush()
        print(f"创建 {len(teachers)} 个老师用户")
        
        bus_data = [
            ("京A12345", "宇通ZK6100", 45),
            ("京A12346", "宇通ZK6100", 45),
            ("京A12347", "金龙XMQ6110", 50),
            ("京A12348", "中通LCK6100", 45),
            ("京A12349", "安凯HFF6100", 48),
        ]
        buses = []
        for i, (plate, model, capacity) in enumerate(bus_data):
            bus = Bus(
                plate_number=plate,
                bus_model=model,
                capacity=capacity,
                status=BusStatus.IDLE,
                gps_latitude=f"39.{random.randint(800000, 950000)}",
                gps_longitude=f"116.{random.randint(300000, 500000)}"
            )
            db.add(bus)
            buses.append(bus)
        db.flush()
        print(f"创建 {len(buses)} 辆校车")
        
        route_data = [
            ("早晨一号线", "学校北门", "阳光小区"),
            ("早晨二号线", "学校北门", "幸福社区"),
            ("早晨三号线", "学校北门", "和谐家园"),
            ("下午一号线", "阳光小区", "学校北门"),
            ("下午二号线", "幸福社区", "学校北门"),
        ]
        routes = []
        for i, (name, start, end) in enumerate(route_data):
            route = Route(
                route_name=name,
                route_code=f"RT{1001 + i}",
                start_point=start,
                end_point=end,
                waypoints="途经站点：站点A, 站点B, 站点C",
                distance_km=random.randint(8, 25),
                estimated_duration_min=random.randint(20, 45),
                status=RouteStatus.PLANNED
            )
            db.add(route)
            routes.append(route)
        db.flush()
        print(f"创建 {len(routes)} 条路线")
        
        driver_behavior_types = list(DriverBehaviorType)
        severities = list(BehaviorSeverity)
        for i in range(15):
            behavior = DriverBehavior(
                bus_id=random.choice(buses).id,
                driver_id=random.choice(drivers).id if drivers else None,
                behavior_type=random.choice(driver_behavior_types),
                severity=random.choice(severities),
                confidence=random.randint(70, 99),
                location_lat=f"39.{random.randint(800000, 950000)}",
                location_lng=f"116.{random.randint(300000, 500000)}",
                description=f"检测到异常行为，置信度{random.randint(70, 99)}%",
                is_handled=random.choice([0, 1]),
                created_at=datetime.now() - timedelta(hours=random.randint(1, 72))
            )
            db.add(behavior)
        db.flush()
        print("创建 15 条司机行为检测记录")
        
        student_behavior_types = list(StudentBehaviorType)
        for i in range(12):
            behavior = StudentBehavior(
                bus_id=random.choice(buses).id,
                behavior_type=random.choice(student_behavior_types),
                confidence=random.randint(65, 98),
                student_count=random.randint(1, 5),
                location_lat=f"39.{random.randint(800000, 950000)}",
                location_lng=f"116.{random.randint(300000, 500000)}",
                description=f"检测到学生异常行为",
                is_handled=random.choice([0, 1]),
                created_at=datetime.now() - timedelta(hours=random.randint(1, 72))
            )
            db.add(behavior)
        db.flush()
        print("创建 12 条学生行为检测记录")
        
        capture_types = list(CaptureType)
        for i in range(10):
            capture = Capture(
                bus_id=random.choice(buses).id,
                capture_type=random.choice(capture_types),
                image_path=f"/uploads/capture_{i+1}.jpg",
                thumbnail_path=f"/uploads/thumb_{i+1}.jpg",
                location_lat=f"39.{random.randint(800000, 950000)}",
                location_lng=f"116.{random.randint(300000, 500000)}",
                description="异常事件抓拍",
                is_uploaded=random.choice([0, 1]),
                created_at=datetime.now() - timedelta(hours=random.randint(1, 72))
            )
            db.add(capture)
        db.flush()
        print("创建 10 条异常抓拍记录")
        
        today = date.today()
        for i in range(5):
            duty_date = today + timedelta(days=i)
            for shift in ["morning", "afternoon"]:
                driver = random.choice(drivers) if drivers else None
                bus = random.choice(buses) if buses else None
                route = random.choice(routes) if routes else None
                
                duty = Duty(
                    duty_date=duty_date,
                    shift_type=shift,
                    driver_id=driver.id if driver else None,
                    bus_id=bus.id if bus else None,
                    route_id=route.id if route else None,
                    status=DutyStatus.SCHEDULED,
                    assigned_by=admin_user.id,
                    is_changed=0
                )
                db.add(duty)
        db.flush()
        print("创建 10 条值班安排记录")
        
        conditions = list(TrafficCondition)
        locations = ["中关村大街", "五道口", "西二旗", "回龙观", "上地"]
        for i in range(8):
            route = random.choice(routes) if routes else None
            traffic = TrafficData(
                route_id=route.id if route else None,
                location_name=random.choice(locations),
                location_lat=f"39.{random.randint(800000, 950000)}",
                location_lng=f"116.{random.randint(300000, 500000)}",
                condition=random.choice(conditions),
                speed_kmh=random.randint(20, 80),
                delay_minutes=random.randint(0, 45),
                distance_km=random.uniform(1.0, 5.0),
                data_source="实时交通API",
                is_sent_to_bus=random.choice([0, 1]),
                created_at=datetime.now() - timedelta(hours=random.randint(1, 24))
            )
            db.add(traffic)
        db.flush()
        print("创建 8 条交通数据记录")
        
        db.commit()
        print("\n测试数据创建完成！")
        print("\n登录账号：")
        print("  管理员: admin / admin123")
        print("  司机: driver1 ~ driver6 / 123456")
        print("  老师: teacher1 ~ teacher3 / 123456")
        
    except Exception as e:
        print(f"创建测试数据时出错: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_test_data()
