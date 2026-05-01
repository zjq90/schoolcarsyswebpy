"""
初始化测试数据脚本
===================

用于初始化数据库并生成测试数据，方便功能测试。

运行方式: python -m scripts.init_test_data
"""

import sys
import os
from datetime import datetime, timedelta, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import (
    User, Parent, Student, ParentStudent,
    Driver, Vehicle, DriverVehicle, Attendance,
    MessageCategory, Message, Complaint,
    Feedback, Emergency, Dispatch, Route, Violation
)
from app.utils.auth import get_password_hash


def init_database():
    """初始化数据库表"""
    print("初始化数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表初始化完成!")


def create_test_data():
    """创建测试数据"""
    print("创建测试数据...")
    db = SessionLocal()

    try:
        parent_password = get_password_hash("123456")
        driver_password = get_password_hash("123456")

        parent_user1 = User(
            phone="13800138001",
            password_hash=parent_password,
            user_type="parent",
            nickname="张三爸爸",
            status=1,
        )
        db.add(parent_user1)
        db.flush()

        parent1 = Parent(
            user_id=parent_user1.id,
            real_name="张三",
            id_card="110101198001011234",
            address="北京市朝阳区xxx街道xxx号",
            emergency_contact="张母",
            emergency_phone="13800138002",
        )
        db.add(parent1)

        parent_user2 = User(
            phone="13800138003",
            password_hash=parent_password,
            user_type="parent",
            nickname="李四妈妈",
            status=1,
        )
        db.add(parent_user2)
        db.flush()

        parent2 = Parent(
            user_id=parent_user2.id,
            real_name="李四",
            id_card="110101198501011235",
            address="北京市海淀区xxx街道xxx号",
            emergency_contact="李父",
            emergency_phone="13800138004",
        )
        db.add(parent2)

        student1 = Student(
            student_no="S2024001",
            real_name="张小明",
            gender=1,
            school="北京市第一实验小学",
            class_name="三年级(1)班",
            grade="三年级",
            address="北京市朝阳区xxx街道xxx号",
            contact_phone="13800138001",
            status=1,
        )
        db.add(student1)

        student2 = Student(
            student_no="S2024002",
            real_name="李小红",
            gender=2,
            school="北京市第一实验小学",
            class_name="三年级(2)班",
            grade="三年级",
            address="北京市海淀区xxx街道xxx号",
            contact_phone="13800138003",
            status=1,
        )
        db.add(student2)

        db.flush()

        ps1 = ParentStudent(
            parent_id=parent1.id,
            student_id=student1.id,
            relation="父亲",
            status=1,
        )
        db.add(ps1)

        ps2 = ParentStudent(
            parent_id=parent2.id,
            student_id=student2.id,
            relation="母亲",
            status=1,
        )
        db.add(ps2)

        driver_user1 = User(
            phone="13900139001",
            password_hash=driver_password,
            user_type="driver",
            nickname="王师傅",
            status=1,
        )
        db.add(driver_user1)
        db.flush()

        driver1 = Driver(
            user_id=driver_user1.id,
            real_name="王建国",
            id_card="110101197501011236",
            driver_license_no="110101197501011236",
            driver_license_type="A1",
            phone="13900139001",
            address="北京市丰台区xxx街道xxx号",
            emergency_contact="王妻",
            emergency_phone="13900139002",
            status=1,
        )
        db.add(driver1)

        driver_user2 = User(
            phone="13900139003",
            password_hash=driver_password,
            user_type="driver",
            nickname="李师傅",
            status=1,
        )
        db.add(driver_user2)
        db.flush()

        driver2 = Driver(
            user_id=driver_user2.id,
            real_name="李卫东",
            id_card="110101197801011237",
            driver_license_no="110101197801011237",
            driver_license_type="A1",
            phone="13900139003",
            address="北京市西城区xxx街道xxx号",
            emergency_contact="李妻",
            emergency_phone="13900139004",
            status=1,
        )
        db.add(driver2)

        vehicle1 = Vehicle(
            plate_no="京A12345",
            vehicle_no="V001",
            vehicle_type="校车",
            brand="宇通",
            model="ZK6100",
            color="黄色",
            seat_count=45,
            mileage=50000,
            status=1,
        )
        db.add(vehicle1)

        vehicle2 = Vehicle(
            plate_no="京A67890",
            vehicle_no="V002",
            vehicle_type="校车",
            brand="金龙",
            model="XML6100",
            color="黄色",
            seat_count=40,
            mileage=30000,
            status=1,
        )
        db.add(vehicle2)

        db.flush()

        parent_categories = [
            {"name": "学生违规消息", "code": "PARENT_VIOLATION", "message_type": "parent", "description": "学生违规相关消息", "sort_order": 1},
            {"name": "学生上下学消息", "code": "PARENT_SCHOOL", "message_type": "parent", "description": "学生上下学接送消息", "sort_order": 2},
            {"name": "车辆状况提醒", "code": "PARENT_VEHICLE", "message_type": "parent", "description": "车辆状况相关提醒", "sort_order": 3},
            {"name": "投诉反馈", "code": "PARENT_COMPLAINT", "message_type": "parent", "description": "投诉处理反馈", "sort_order": 4},
        ]

        driver_categories = [
            {"name": "学生违规提醒", "code": "DRIVER_VIOLATION", "message_type": "driver", "description": "学生违规相关提醒", "sort_order": 1},
            {"name": "紧急状况提醒", "code": "DRIVER_EMERGENCY", "message_type": "driver", "description": "紧急状况相关提醒", "sort_order": 2},
            {"name": "路线规划提醒", "code": "DRIVER_ROUTE", "message_type": "driver", "description": "路线规划相关提醒", "sort_order": 3},
            {"name": "违章提醒", "code": "DRIVER_VIOLATION_RECORD", "message_type": "driver", "description": "违章相关提醒", "sort_order": 4},
            {"name": "车辆保养提醒", "code": "DRIVER_MAINTENANCE", "message_type": "driver", "description": "车辆保养相关提醒", "sort_order": 5},
        ]

        category_map = {}
        for cat_data in parent_categories + driver_categories:
            cat = MessageCategory(**cat_data, status=1)
            db.add(cat)
            db.flush()
            category_map[cat_data["code"]] = cat.id

        message1 = Message(
            title="张小明已安全上车",
            content="您好，您的孩子张小明已于今天早上7:30安全上车，请放心。车牌号：京A12345，司机：王师傅。",
            message_type="parent",
            category_id=category_map["PARENT_SCHOOL"],
            receiver_id=parent1.id,
            user_id=parent_user1.id,
            is_read=0,
        )
        db.add(message1)

        message2 = Message(
            title="车辆保养提醒",
            content="您好，您孩子乘坐的车辆京A12345将于下周三进行例行保养，请留意。",
            message_type="parent",
            category_id=category_map["PARENT_VEHICLE"],
            receiver_id=parent1.id,
            user_id=parent_user1.id,
            is_read=1,
            read_time=datetime.now() - timedelta(hours=2),
        )
        db.add(message2)

        message3 = Message(
            title="调度通知：明天提前发车",
            content="王师傅您好，明天（5月2日）因特殊活动，早班发车时间提前至6:30，请提前做好准备。",
            message_type="driver",
            category_id=category_map["DRIVER_ROUTE"],
            receiver_id=driver1.id,
            user_id=driver_user1.id,
            is_read=0,
        )
        db.add(message3)

        message4 = Message(
            title="车辆保养提醒",
            content="李师傅您好，您负责的车辆京A67890已行驶3万公里，建议进行保养检查。",
            message_type="driver",
            category_id=category_map["DRIVER_MAINTENANCE"],
            receiver_id=driver2.id,
            user_id=driver_user2.id,
            is_read=1,
            read_time=datetime.now() - timedelta(days=1),
        )
        db.add(message4)

        route1 = Route(
            route_no="R001",
            route_name="朝阳线",
            start_point="学校",
            end_point="朝阳公园",
            estimated_duration=45,
            distance=15,
            departure_time=time(7, 30),
            arrival_time=time(8, 15),
            student_count=20,
            status=1,
            description="接送朝阳区学生",
        )
        db.add(route1)

        route2 = Route(
            route_no="R002",
            route_name="海淀线",
            start_point="学校",
            end_point="中关村",
            estimated_duration=60,
            distance=20,
            departure_time=time(7, 0),
            arrival_time=time(8, 0),
            student_count=25,
            status=1,
            description="接送海淀区学生",
        )
        db.add(route2)

        db.flush()

        dispatch1 = Dispatch(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            route_id=route1.id,
            title="早班接送任务",
            content="请于今天早上7:30准时出发，执行朝阳线接送任务。",
            dispatch_time=datetime.now() - timedelta(hours=12),
            estimated_arrival_time=datetime.now() - timedelta(hours=11, minutes=15),
            status=4,
        )
        db.add(dispatch1)

        dispatch2 = Dispatch(
            driver_id=driver2.id,
            vehicle_id=vehicle2.id,
            route_id=route2.id,
            title="晚班接送任务",
            content="请于今天下午16:30准时出发，执行海淀线接送任务。",
            dispatch_time=datetime.now(),
            estimated_arrival_time=datetime.now() + timedelta(hours=1),
            status=1,
        )
        db.add(dispatch2)

        violation1 = Violation(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            violation_no="V20240501001",
            violation_type=1,
            violation_time=datetime.now() - timedelta(days=5),
            violation_address="北京市朝阳区建国路",
            fine_amount=20000,
            deduct_points=3,
            status=1,
        )
        db.add(violation1)

        complaint1 = Complaint(
            parent_id=parent1.id,
            student_id=student1.id,
            title="司机服务态度问题",
            content="今天早上接送孩子时，司机王师傅态度不好，希望能改进。",
            complaint_type=1,
            status=2,
            handler_remark="已与司机沟通，司机已认识到错误并道歉。",
            handle_time=datetime.now() - timedelta(hours=2),
        )
        db.add(complaint1)

        feedback1 = Feedback(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            feedback_type=2,
            title="车辆例行保养报告",
            content="已完成车辆例行保养，更换机油和机滤，检查刹车系统正常。",
            status=2,
            reviewer_remark="保养合格",
            review_time=datetime.now() - timedelta(days=2),
        )
        db.add(feedback1)

        emergency1 = Emergency(
            driver_id=driver2.id,
            vehicle_id=vehicle2.id,
            emergency_type=1,
            title="车辆轮胎故障",
            content="行驶中发现左后轮异响，已安全停靠路边，请安排维修。",
            latitude=39.9042,
            longitude=116.4074,
            location_address="北京市海淀区中关村大街",
            status=3,
            handler_remark="维修人员已到达现场处理。",
            handle_time=datetime.now() - timedelta(hours=1),
        )
        db.add(emergency1)

        now = datetime.now()
        today_start = datetime(now.year, now.month, now.day)
        attendance1 = Attendance(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            attendance_date=today_start,
            check_in_time=today_start + timedelta(hours=6, minutes=30),
            check_in_address="学校停车场",
            check_out_time=today_start + timedelta(hours=18),
            check_out_address="学校停车场",
            status=1,
        )
        db.add(attendance1)

        dv1 = DriverVehicle(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            bind_time=now - timedelta(days=30),
            status=0,
            unbind_time=now - timedelta(days=1),
        )
        db.add(dv1)

        dv2 = DriverVehicle(
            driver_id=driver1.id,
            vehicle_id=vehicle1.id,
            bind_time=now - timedelta(hours=12),
            status=1,
        )
        db.add(dv2)

        db.commit()

        print("=" * 50)
        print("测试数据创建完成!")
        print("=" * 50)
        print("\n【测试账号】")
        print("-" * 30)
        print("\n家长端账号:")
        print("  账号1: 13800138001 / 密码: 123456 (张三爸爸)")
        print("  账号2: 13800138003 / 密码: 123456 (李四妈妈)")
        print("\n司机端账号:")
        print("  账号1: 13900139001 / 密码: 123456 (王师傅)")
        print("  账号2: 13900139003 / 密码: 123456 (李师傅)")
        print("\n【API文档】")
        print("-" * 30)
        print("  Swagger UI: http://localhost:8000/docs")
        print("  ReDoc: http://localhost:8000/redoc")
        print("\n【启动命令】")
        print("-" * 30)
        print("  uvicorn app.main:app --reload")
        print("=" * 50)

    except Exception as e:
        print(f"创建测试数据失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    create_test_data()
