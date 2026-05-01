"""
初始化测试数据脚本
用于创建系统默认用户、学校、车辆、司机、学生、路线等测试数据
"""
import sys
import os
from datetime import date, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.school import School
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.student import Student
from app.models.route import Route
from app.models.policy import Policy
from app.utils.security import get_password_hash
from app.config import ROLES


def init_test_data():
    """
    初始化测试数据
    """
    print("=" * 50)
    print("开始初始化测试数据...")
    print("=" * 50)
    
    # 初始化数据库
    init_db()
    
    db = SessionLocal()
    
    try:
        # 1. 创建学校
        print("\n[1/7] 创建学校数据...")
        schools = [
            School(
                school_name="第一实验小学",
                school_code="SCH001",
                address="北京市朝阳区建国路88号",
                principal="张校长",
                contact_phone="010-12345678",
                description="一所拥有50年历史的优质小学"
            ),
            School(
                school_name="第二实验中学",
                school_code="SCH002",
                address="北京市海淀区中关村大街1号",
                principal="李校长",
                contact_phone="010-87654321",
                description="现代化示范性中学"
            ),
            School(
                school_name="第三幼儿园",
                school_code="SCH003",
                address="北京市西城区西单北大街100号",
                principal="王园长",
                contact_phone="010-11112222",
                description="省级示范幼儿园"
            )
        ]
        
        for school in schools:
            existing = db.query(School).filter(School.school_code == school.school_code).first()
            if not existing:
                db.add(school)
                print(f"  ✓ 创建学校: {school.school_name}")
            else:
                print(f"  - 学校已存在: {school.school_name}")
        
        db.commit()
        
        # 重新获取学校以获取ID
        school1 = db.query(School).filter(School.school_code == "SCH001").first()
        school2 = db.query(School).filter(School.school_code == "SCH002").first()
        school3 = db.query(School).filter(School.school_code == "SCH003").first()
        
        # 2. 创建用户
        print("\n[2/7] 创建用户数据...")
        
        # 教育局管理员
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                password=get_password_hash("123456"),
                real_name="教育局管理员",
                role=ROLES["EDUCATION_BUREAU"],
                phone="13800138080",
                email="admin@schoolbus.com",
                is_active=True
            )
            db.add(admin_user)
            print(f"  ✓ 创建教育局管理员: admin / 123456")
        else:
            print(f"  - 教育局管理员已存在: admin")
        
        # 学校管理员
        school_admins = [
            {
                "username": "school1",
                "password": "123456",
                "real_name": "第一实验小学管理员",
                "school": school1,
                "phone": "13800138001"
            },
            {
                "username": "school2",
                "password": "123456",
                "real_name": "第二实验中学管理员",
                "school": school2,
                "phone": "13800138002"
            },
            {
                "username": "school3",
                "password": "123456",
                "real_name": "第三幼儿园管理员",
                "school": school3,
                "phone": "13800138003"
            }
        ]
        
        for admin_data in school_admins:
            existing = db.query(User).filter(User.username == admin_data["username"]).first()
            if not existing:
                new_admin = User(
                    username=admin_data["username"],
                    password=get_password_hash(admin_data["password"]),
                    real_name=admin_data["real_name"],
                    role=ROLES["SCHOOL_ADMIN"],
                    phone=admin_data["phone"],
                    school_id=admin_data["school"].id,
                    is_active=True
                )
                db.add(new_admin)
                print(f"  ✓ 创建学校管理员: {admin_data['username']} / 123456")
            else:
                print(f"  - 学校管理员已存在: {admin_data['username']}")
        
        db.commit()
        
        # 3. 创建车辆
        print("\n[3/7] 创建车辆数据...")
        
        vehicles = [
            # 学校1的车辆
            {
                "vehicle_code": "V001",
                "license_plate": "京A12345",
                "vehicle_model": "宇通ZK6858H",
                "seat_count": 45,
                "purchase_date": date(2022, 3, 15),
                "school": school1,
                "campus": "主校区",
                "status": "available"
            },
            {
                "vehicle_code": "V002",
                "license_plate": "京A12346",
                "vehicle_model": "宇通ZK6858H",
                "seat_count": 45,
                "purchase_date": date(2022, 6, 20),
                "school": school1,
                "campus": "主校区",
                "status": "in_use"
            },
            {
                "vehicle_code": "V003",
                "license_plate": "京A12347",
                "vehicle_model": "金龙XMQ6802",
                "seat_count": 35,
                "purchase_date": date(2023, 1, 10),
                "school": school1,
                "campus": "东校区",
                "status": "available"
            },
            # 学校2的车辆
            {
                "vehicle_code": "V004",
                "license_plate": "京B56789",
                "vehicle_model": "宇通ZK6938H",
                "seat_count": 55,
                "purchase_date": date(2021, 9, 1),
                "school": school2,
                "campus": "主校区",
                "status": "available"
            },
            {
                "vehicle_code": "V005",
                "license_plate": "京B56790",
                "vehicle_model": "宇通ZK6938H",
                "seat_count": 55,
                "purchase_date": date(2021, 11, 15),
                "school": school2,
                "campus": "南校区",
                "status": "maintenance"
            },
            # 学校3的车辆
            {
                "vehicle_code": "V006",
                "license_plate": "京C11111",
                "vehicle_model": "长安校车SC6605",
                "seat_count": 25,
                "purchase_date": date(2023, 5, 20),
                "school": school3,
                "campus": "主校区",
                "status": "available"
            }
        ]
        
        for v_data in vehicles:
            existing = db.query(Vehicle).filter(Vehicle.vehicle_code == v_data["vehicle_code"]).first()
            if not existing:
                new_vehicle = Vehicle(
                    vehicle_code=v_data["vehicle_code"],
                    license_plate=v_data["license_plate"],
                    vehicle_model=v_data["vehicle_model"],
                    seat_count=v_data["seat_count"],
                    purchase_date=v_data["purchase_date"],
                    school_id=v_data["school"].id,
                    campus=v_data["campus"],
                    status=v_data["status"],
                    insurance_expire=date.today() + timedelta(days=365),
                    inspection_expire=date.today() + timedelta(days=180)
                )
                db.add(new_vehicle)
                print(f"  ✓ 创建车辆: {v_data['license_plate']} - {v_data['vehicle_model']}")
            else:
                print(f"  - 车辆已存在: {v_data['license_plate']}")
        
        db.commit()
        
        # 重新获取车辆
        vehicle1 = db.query(Vehicle).filter(Vehicle.vehicle_code == "V001").first()
        vehicle2 = db.query(Vehicle).filter(Vehicle.vehicle_code == "V002").first()
        vehicle4 = db.query(Vehicle).filter(Vehicle.vehicle_code == "V004").first()
        vehicle6 = db.query(Vehicle).filter(Vehicle.vehicle_code == "V006").first()
        
        # 4. 创建司机
        print("\n[4/7] 创建司机数据...")
        
        drivers = [
            {
                "driver_code": "D001",
                "real_name": "张师傅",
                "id_card": "110101198001011234",
                "phone": "13900000001",
                "gender": "男",
                "birthday": date(1980, 1, 1),
                "driving_years": 20,
                "health_status": "良好",
                "license_number": "110101198001011234",
                "license_type": "A1",
                "license_expire": date(2028, 1, 1),
                "qualification_cert": "QC001",
                "qualification_expire": date(2027, 6, 1),
                "school": school1,
                "status": "available"
            },
            {
                "driver_code": "D002",
                "real_name": "李师傅",
                "id_card": "110101198505052345",
                "phone": "13900000002",
                "gender": "男",
                "birthday": date(1985, 5, 5),
                "driving_years": 15,
                "health_status": "良好",
                "license_number": "110101198505052345",
                "license_type": "A1",
                "license_expire": date(2029, 5, 5),
                "qualification_cert": "QC002",
                "qualification_expire": date(2028, 10, 1),
                "school": school1,
                "status": "on_duty"
            },
            {
                "driver_code": "D003",
                "real_name": "王师傅",
                "id_card": "110101197808083456",
                "phone": "13900000003",
                "gender": "男",
                "birthday": date(1978, 8, 8),
                "driving_years": 22,
                "health_status": "良好",
                "license_number": "110101197808083456",
                "license_type": "A1A2",
                "license_expire": date(2027, 8, 8),
                "qualification_cert": "QC003",
                "qualification_expire": date(2026, 12, 1),
                "school": school2,
                "status": "available"
            },
            {
                "driver_code": "D004",
                "real_name": "赵师傅",
                "id_card": "110101198203034567",
                "phone": "13900000004",
                "gender": "男",
                "birthday": date(1982, 3, 3),
                "driving_years": 18,
                "health_status": "良好",
                "license_number": "110101198203034567",
                "license_type": "A1",
                "license_expire": date(2028, 3, 3),
                "qualification_cert": "QC004",
                "qualification_expire": date(2027, 9, 1),
                "school": school3,
                "status": "available"
            }
        ]
        
        for d_data in drivers:
            existing = db.query(Driver).filter(Driver.driver_code == d_data["driver_code"]).first()
            if not existing:
                new_driver = Driver(**{k: v for k, v in d_data.items() if k != "school"})
                new_driver.school_id = d_data["school"].id
                db.add(new_driver)
                print(f"  ✓ 创建司机: {d_data['real_name']}")
            else:
                print(f"  - 司机已存在: {d_data['real_name']}")
        
        db.commit()
        
        # 重新获取司机
        driver1 = db.query(Driver).filter(Driver.driver_code == "D001").first()
        driver2 = db.query(Driver).filter(Driver.driver_code == "D002").first()
        driver3 = db.query(Driver).filter(Driver.driver_code == "D003").first()
        driver4 = db.query(Driver).filter(Driver.driver_code == "D004").first()
        
        # 更新车辆的司机关联
        if vehicle1 and driver1:
            vehicle1.driver_id = driver1.id
        if vehicle2 and driver2:
            vehicle2.driver_id = driver2.id
        if vehicle4 and driver3:
            vehicle4.driver_id = driver3.id
        if vehicle6 and driver4:
            vehicle6.driver_id = driver4.id
        db.commit()
        
        # 5. 创建路线
        print("\n[5/7] 创建路线数据...")
        
        routes = [
            {
                "route_code": "R001",
                "route_name": "城东线路",
                "school": school1,
                "start_address": "朝阳区国贸商圈",
                "end_address": "第一实验小学",
                "main_route": "国贸→大望路→四惠→高碑店→传媒大学→定福庄→学校",
                "main_route_stops": '[{"name": "国贸站", "time": "06:30"}, {"name": "大望路站", "time": "06:35"}, {"name": "四惠站", "time": "06:40"}, {"name": "学校", "time": "07:00"}]',
                "emergency_route": "国贸→三环→红领巾桥→朝阳路→学校",
                "backup_route": "国贸→京通快速→双桥→学校",
                "departure_time": None,
                "estimated_duration": 30,
                "vehicle": vehicle1,
                "driver": driver1,
                "status": "active"
            },
            {
                "route_code": "R002",
                "route_name": "城西线路",
                "school": school1,
                "start_address": "海淀区中关村",
                "end_address": "第一实验小学",
                "main_route": "中关村→海淀黄庄→人民大学→魏公村→国家图书馆→动物园→西直门→东直门→学校",
                "main_route_stops": '[{"name": "中关村站", "time": "06:20"}, {"name": "人民大学站", "time": "06:30"}, {"name": "西直门站", "time": "06:45"}, {"name": "学校", "time": "07:05"}]',
                "emergency_route": "中关村→四环→健翔桥→京藏高速→北五环→学校",
                "departure_time": None,
                "estimated_duration": 45,
                "vehicle": vehicle2,
                "driver": driver2,
                "status": "active"
            },
            {
                "route_code": "R003",
                "route_name": "中学专线",
                "school": school2,
                "start_address": "海淀区五道口",
                "end_address": "第二实验中学",
                "main_route": "五道口→学院路→北太平庄→马甸→安贞桥→和平西桥→学校",
                "main_route_stops": '[{"name": "五道口站", "time": "06:25"}, {"name": "学院路站", "time": "06:35"}, {"name": "学校", "time": "06:55"}]',
                "departure_time": None,
                "estimated_duration": 30,
                "vehicle": vehicle4,
                "driver": driver3,
                "status": "active"
            }
        ]
        
        for r_data in routes:
            existing = db.query(Route).filter(Route.route_code == r_data["route_code"]).first()
            if not existing:
                new_route = Route(
                    route_code=r_data["route_code"],
                    route_name=r_data["route_name"],
                    school_id=r_data["school"].id,
                    start_address=r_data["start_address"],
                    end_address=r_data["end_address"],
                    main_route=r_data["main_route"],
                    main_route_stops=r_data["main_route_stops"],
                    emergency_route=r_data.get("emergency_route"),
                    backup_route=r_data.get("backup_route"),
                    estimated_duration=r_data["estimated_duration"],
                    vehicle_id=r_data["vehicle"].id if r_data.get("vehicle") else None,
                    driver_id=r_data["driver"].id if r_data.get("driver") else None,
                    status=r_data["status"]
                )
                db.add(new_route)
                print(f"  ✓ 创建路线: {r_data['route_name']}")
            else:
                print(f"  - 路线已存在: {r_data['route_name']}")
        
        db.commit()
        
        # 重新获取路线
        route1 = db.query(Route).filter(Route.route_code == "R001").first()
        route2 = db.query(Route).filter(Route.route_code == "R002").first()
        route3 = db.query(Route).filter(Route.route_code == "R003").first()
        
        # 6. 创建学生
        print("\n[6/7] 创建学生数据...")
        
        students = [
            # 路线1的学生
            {
                "student_code": "S001",
                "real_name": "小明",
                "gender": "男",
                "birthday": date(2015, 3, 15),
                "id_card": "110101201503151234",
                "school": school1,
                "grade": "三年级",
                "class_name": "3班",
                "parent_name": "明爸爸",
                "parent_phone": "13600000001",
                "home_address": "朝阳区国贸附近小区",
                "pickup_address": "国贸公交站",
                "dropoff_address": "学校正门",
                "route": route1,
                "status": "active"
            },
            {
                "student_code": "S002",
                "real_name": "小红",
                "gender": "女",
                "birthday": date(2015, 6, 20),
                "id_card": "110101201506202345",
                "school": school1,
                "grade": "三年级",
                "class_name": "1班",
                "parent_name": "红妈妈",
                "parent_phone": "13600000002",
                "home_address": "朝阳区四惠附近",
                "pickup_address": "四惠地铁站",
                "dropoff_address": "学校正门",
                "route": route1,
                "status": "active"
            },
            {
                "student_code": "S003",
                "real_name": "小刚",
                "gender": "男",
                "birthday": date(2016, 1, 10),
                "id_card": "110101201601103456",
                "school": school1,
                "grade": "二年级",
                "class_name": "2班",
                "parent_name": "刚爸爸",
                "parent_phone": "13600000003",
                "home_address": "朝阳区传媒大学附近",
                "pickup_address": "传媒大学北门",
                "dropoff_address": "学校正门",
                "route": route1,
                "status": "active"
            },
            # 路线2的学生
            {
                "student_code": "S004",
                "real_name": "小丽",
                "gender": "女",
                "birthday": date(2014, 9, 5),
                "id_card": "110101201409054567",
                "school": school1,
                "grade": "四年级",
                "class_name": "1班",
                "parent_name": "丽妈妈",
                "parent_phone": "13600000004",
                "home_address": "海淀区中关村",
                "pickup_address": "中关村地铁站",
                "dropoff_address": "学校正门",
                "route": route2,
                "status": "active"
            },
            {
                "student_code": "S005",
                "real_name": "小强",
                "gender": "男",
                "birthday": date(2014, 12, 25),
                "id_card": "110101201412255678",
                "school": school1,
                "grade": "四年级",
                "class_name": "2班",
                "parent_name": "强爸爸",
                "parent_phone": "13600000005",
                "home_address": "海淀区人民大学附近",
                "pickup_address": "人民大学东门",
                "dropoff_address": "学校正门",
                "route": route2,
                "status": "active"
            },
            # 路线3的学生
            {
                "student_code": "S006",
                "real_name": "小华",
                "gender": "男",
                "birthday": date(2012, 8, 15),
                "id_card": "110101201208156789",
                "school": school2,
                "grade": "初二年级",
                "class_name": "3班",
                "parent_name": "华爸爸",
                "parent_phone": "13600000006",
                "home_address": "海淀区五道口",
                "pickup_address": "五道口地铁站",
                "dropoff_address": "学校正门",
                "route": route3,
                "status": "active"
            },
            {
                "student_code": "S007",
                "real_name": "小美",
                "gender": "女",
                "birthday": date(2013, 4, 10),
                "id_card": "110101201304107890",
                "school": school2,
                "grade": "初一年级",
                "class_name": "1班",
                "parent_name": "美妈妈",
                "parent_phone": "13600000007",
                "home_address": "海淀区学院路",
                "pickup_address": "学院路公交站",
                "dropoff_address": "学校正门",
                "route": route3,
                "status": "active"
            }
        ]
        
        for s_data in students:
            existing = db.query(Student).filter(Student.student_code == s_data["student_code"]).first()
            if not existing:
                new_student = Student(
                    student_code=s_data["student_code"],
                    real_name=s_data["real_name"],
                    gender=s_data["gender"],
                    birthday=s_data["birthday"],
                    id_card=s_data["id_card"],
                    school_id=s_data["school"].id,
                    grade=s_data["grade"],
                    class_name=s_data["class_name"],
                    parent_name=s_data["parent_name"],
                    parent_phone=s_data["parent_phone"],
                    home_address=s_data["home_address"],
                    pickup_address=s_data["pickup_address"],
                    dropoff_address=s_data["dropoff_address"],
                    route_id=s_data["route"].id if s_data.get("route") else None,
                    status=s_data["status"]
                )
                db.add(new_student)
                print(f"  ✓ 创建学生: {s_data['real_name']} - {s_data['grade']}")
            else:
                print(f"  - 学生已存在: {s_data['real_name']}")
        
        db.commit()
        
        # 7. 创建政策
        print("\n[7/7] 创建政策数据...")
        
        # 获取教育局管理员
        edu_admin = db.query(User).filter(User.username == "admin").first()
        
        policies = [
            {
                "policy_code": "POL001",
                "title": "关于加强校车安全管理的通知",
                "content": "为进一步加强校车安全管理，保障学生上下学交通安全，根据《校车安全管理条例》等相关规定，现就有关事项通知如下：\n\n一、提高思想认识，加强组织领导\n二、落实安全责任，完善管理制度\n三、加强车辆维护，确保车况良好\n四、规范司机管理，提高安全意识\n五、加强日常监管，落实安全措施",
                "policy_type": "notice",
                "publisher": edu_admin,
                "publish_date": date(2024, 1, 15),
                "effective_date": date(2024, 2, 1),
                "is_published": True,
                "is_top": True,
                "status": "published"
            },
            {
                "policy_code": "POL002",
                "title": "校车司机从业资格管理规定",
                "content": "第一章 总则\n\n第一条 为加强校车司机管理，规范校车司机从业行为，保障学生乘车安全，制定本规定。\n\n第二章 从业资格\n\n第二条 校车司机应当符合下列条件：\n（一）取得相应准驾车型驾驶证并具有3年以上驾驶经历；\n（二）年龄不超过60周岁；\n（三）无致人死亡或者重伤的交通事故责任记录；\n（四）无酒后驾驶或者醉酒驾驶机动车记录；\n（五）身心健康，无传染性疾病，无癫痫、精神病等可能危及行车安全的疾病病史。",
                "policy_type": "regulation",
                "publisher": edu_admin,
                "publish_date": date(2024, 2, 1),
                "effective_date": date(2024, 3, 1),
                "is_published": True,
                "is_top": False,
                "status": "published"
            }
        ]
        
        for p_data in policies:
            existing = db.query(Policy).filter(Policy.policy_code == p_data["policy_code"]).first()
            if not existing:
                new_policy = Policy(
                    policy_code=p_data["policy_code"],
                    title=p_data["title"],
                    content=p_data["content"],
                    policy_type=p_data["policy_type"],
                    publisher_id=p_data["publisher"].id,
                    publish_date=p_data["publish_date"],
                    effective_date=p_data["effective_date"],
                    is_published=p_data["is_published"],
                    is_top=p_data["is_top"],
                    status=p_data["status"]
                )
                db.add(new_policy)
                print(f"  ✓ 创建政策: {p_data['title']}")
            else:
                print(f"  - 政策已存在: {p_data['title']}")
        
        db.commit()
        
        print("\n" + "=" * 50)
        print("测试数据初始化完成！")
        print("=" * 50)
        print("\n【默认登录账号】")
        print(f"  教育局管理员: admin / 123456")
        print(f"  第一实验小学管理员: school1 / 123456")
        print(f"  第二实验中学管理员: school2 / 123456")
        print(f"  第三幼儿园管理员: school3 / 123456")
        print("\n【创建的数据统计】")
        print(f"  学校数量: {db.query(School).count()}")
        print(f"  用户数量: {db.query(User).count()}")
        print(f"  车辆数量: {db.query(Vehicle).count()}")
        print(f"  司机数量: {db.query(Driver).count()}")
        print(f"  学生数量: {db.query(Student).count()}")
        print(f"  路线数量: {db.query(Route).count()}")
        print(f"  政策数量: {db.query(Policy).count()}")
        
    except Exception as e:
        print(f"\n❌ 初始化数据失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_test_data()
