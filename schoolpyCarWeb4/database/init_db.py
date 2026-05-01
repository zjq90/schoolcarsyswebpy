"""
校车管理系统 - 数据库初始化脚本
创建数据库表结构并生成测试数据
"""
import sqlite3
import os
from datetime import datetime, timedelta
import random

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "school_bus.db")

# 确保database目录存在
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def create_tables(conn):
    """
    创建数据库表
    """
    cursor = conn.cursor()

    # 司机表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(20),
        license_no VARCHAR(50),
        hire_date DATE,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 车辆表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number VARCHAR(20) NOT NULL UNIQUE,
        vehicle_type VARCHAR(50),
        capacity INTEGER,
        purchase_date DATE,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 司机评分表（每天一条记录）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS driver_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id INTEGER NOT NULL,
        score_date DATE NOT NULL,
        violation_count INTEGER DEFAULT 0,
        complaint_count INTEGER DEFAULT 0,
        safe_driving_hours DECIMAL(10,2) DEFAULT 0.00,
        credit_score DECIMAL(10,2) DEFAULT 100.00,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (driver_id) REFERENCES drivers(id)
    )
    ''')

    # 运维记录表（年检、保险、维修、油耗）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_type VARCHAR(20) NOT NULL,
        vehicle_id INTEGER NOT NULL,
        driver_id INTEGER,
        record_date DATE NOT NULL,
        amount DECIMAL(10,2) DEFAULT 0.00,
        description TEXT,
        status VARCHAR(20) DEFAULT 'completed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
        FOREIGN KEY (driver_id) REFERENCES drivers(id)
    )
    ''')

    # 学生表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        student_no VARCHAR(50) UNIQUE,
        class_name VARCHAR(50),
        card_id VARCHAR(50) UNIQUE,
        parent_phone VARCHAR(20),
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 消息推送记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message_push_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        message_type VARCHAR(30) NOT NULL,
        content TEXT NOT NULL,
        push_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'sent',
        receiver_phone VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    ''')

    # 校车状态记录表（发车、到站、异常）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bus_status_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        driver_id INTEGER,
        status_type VARCHAR(30) NOT NULL,
        status_value VARCHAR(50) NOT NULL,
        location VARCHAR(100),
        record_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
        FOREIGN KEY (driver_id) REFERENCES drivers(id)
    )
    ''')

    # 创建索引提高查询性能
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_driver_scores_date ON driver_scores(score_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_maintenance_records_date ON maintenance_records(record_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_message_push_time ON message_push_logs(push_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bus_status_time ON bus_status_logs(record_time)')

    conn.commit()
    print("数据库表创建成功！")


def generate_test_data(conn):
    """
    生成测试数据
    """
    cursor = conn.cursor()

    # 生成司机测试数据
    drivers = [
        ("张师傅", "13800138001", "A12345678", "2020-01-15", "active"),
        ("李师傅", "13800138002", "B23456789", "2021-03-20", "active"),
        ("王师傅", "13800138003", "C34567890", "2019-06-10", "active"),
        ("赵师傅", "13800138004", "D45678901", "2022-02-14", "active"),
        ("刘师傅", "13800138005", "E56789012", "2023-01-01", "active"),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO drivers (name, phone, license_no, hire_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', drivers)

    # 生成车辆测试数据
    vehicles = [
        ("京A12345", "金龙大巴", 45, "2020-05-10", "active"),
        ("京B23456", "宇通中巴", 30, "2021-08-15", "active"),
        ("京C34567", "福田小巴", 20, "2019-03-20", "active"),
        ("京D45678", "中通大巴", 50, "2022-11-05", "active"),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO vehicles (plate_number, vehicle_type, capacity, purchase_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', vehicles)

    # 生成学生测试数据
    students = [
        ("小明", "S001", "三年级1班", "CARD001", "13900139001", "active"),
        ("小红", "S002", "三年级2班", "CARD002", "13900139002", "active"),
        ("小华", "S003", "四年级1班", "CARD003", "13900139003", "active"),
        ("小丽", "S004", "四年级2班", "CARD004", "13900139004", "active"),
        ("小强", "S005", "五年级1班", "CARD005", "13900139005", "active"),
        ("小美", "S006", "五年级2班", "CARD006", "13900139006", "active"),
        ("小刚", "S007", "六年级1班", "CARD007", "13900139007", "active"),
        ("小芳", "S008", "六年级2班", "CARD008", "13900139008", "active"),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO students (name, student_no, class_name, card_id, parent_phone, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', students)

    # 生成司机评分记录（近30天的数据）
    today = datetime.now().date()
    cursor.execute("SELECT id FROM drivers")
    driver_ids = [row[0] for row in cursor.fetchall()]

    for driver_id in driver_ids:
        for i in range(30):
            score_date = today - timedelta(days=i)
            violation_count = random.randint(0, 2)
            complaint_count = random.randint(0, 1)
            safe_driving_hours = round(random.uniform(4.0, 8.0), 2)

            # 计算信用分：基础分100 - 违章*5 - 投诉*10 + 安全驾驶*0.5
            credit_score = max(0, min(100,
                100 - violation_count * 5 - complaint_count * 10 + safe_driving_hours * 0.5
            ))

            cursor.execute('''
                INSERT OR IGNORE INTO driver_scores
                (driver_id, score_date, violation_count, complaint_count, safe_driving_hours, credit_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (driver_id, score_date, violation_count, complaint_count, safe_driving_hours, credit_score))

    # 生成运维记录
    cursor.execute("SELECT id FROM vehicles")
    vehicle_ids = [row[0] for row in cursor.fetchall()]

    record_types = ["年检", "保险", "维修", "油耗"]
    for _ in range(50):
        record_type = random.choice(record_types)
        vehicle_id = random.choice(vehicle_ids)
        driver_id = random.choice(driver_ids) if random.random() > 0.3 else None
        record_date = today - timedelta(days=random.randint(0, 90))
        amount = round(random.uniform(100, 5000), 2)

        descriptions = {
            "年检": "车辆年度安全检查",
            "保险": "车辆交强险及商业保险续保",
            "维修": "常规保养及故障维修",
            "油耗": "燃油加注记录"
        }
        description = descriptions[record_type]

        cursor.execute('''
            INSERT INTO maintenance_records
            (record_type, vehicle_id, driver_id, record_date, amount, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (record_type, vehicle_id, driver_id, record_date, amount, description, "completed"))

    # 生成消息推送记录
    cursor.execute("SELECT id, parent_phone FROM students")
    students_data = cursor.fetchall()

    message_types = ["上车刷卡", "下车刷卡", "校车发车", "校车到站", "异常通知"]
    for _ in range(100):
        student_id, parent_phone = random.choice(students_data)
        message_type = random.choice(message_types)
        push_time = today - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(6, 18),
            minutes=random.randint(0, 59)
        )

        contents = {
            "上车刷卡": f"学生已刷卡上车，请知悉",
            "下车刷卡": f"学生已刷卡下车，请知悉",
            "校车发车": "校车已从学校发车",
            "校车到站": "校车已到达站点",
            "异常通知": "校车因道路拥堵可能延迟到达"
        }
        content = contents[message_type]

        cursor.execute('''
            INSERT INTO message_push_logs
            (student_id, message_type, content, push_time, status, receiver_phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, message_type, content, push_time, "sent", parent_phone))

    # 生成校车状态记录
    status_types = ["发车", "到站", "正常", "异常"]
    status_values = {
        "发车": ["已发车", "准时发车"],
        "到站": ["已到站", "准点到达"],
        "正常": ["正常运行", "状态良好"],
        "异常": ["绕行", "迟到", "临时停车", "道路拥堵"]
    }
    locations = ["学校", "站点A", "站点B", "站点C", "站点D", "站点E", "返回途中"]

    for _ in range(80):
        vehicle_id = random.choice(vehicle_ids)
        driver_id = random.choice(driver_ids) if random.random() > 0.2 else None
        status_type = random.choice(status_types)
        status_value = random.choice(status_values[status_type])
        location = random.choice(locations)
        record_time = today - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(6, 18),
            minutes=random.randint(0, 59)
        )

        cursor.execute('''
            INSERT INTO bus_status_logs
            (vehicle_id, driver_id, status_type, status_value, location, record_time, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (vehicle_id, driver_id, status_type, status_value, location, record_time, f"校车{status_value}"))

    conn.commit()
    print("测试数据生成成功！")


def init_database():
    """
    初始化数据库主函数
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        create_tables(conn)
        generate_test_data(conn)
        print("数据库初始化完成！")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
