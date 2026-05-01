"""
测试数据生成器模块
用于生成校车管理系统的测试数据
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import Vehicle, Geofence, Alert, AlertNotification
from database import get_db

# 测试数据配置
TEST_DATA_CONFIG = {
    'vehicle_count': 5,
    'trajectory_days': 7,
    'trajectory_points_per_hour': 12,
    'geofence_count': 3,
    'alert_count': 5
}

# 测试车辆数据
TEST_VEHICLES = [
    {
        'plate_number': '京A12345',
        'driver_name': '张三',
        'driver_phone': '13800138001',
        'driver_license': 'A1234567890',
        'vehicle_model': '宇通ZK6102BEV',
        'capacity': 45
    },
    {
        'plate_number': '京B67890',
        'driver_name': '李四',
        'driver_phone': '13800138002',
        'driver_license': 'B1234567890',
        'vehicle_model': '金龙XMQ6110',
        'capacity': 50
    },
    {
        'plate_number': '京C11111',
        'driver_name': '王五',
        'driver_phone': '13800138003',
        'driver_license': 'C1234567890',
        'vehicle_model': '黄海DD6109',
        'capacity': 40
    },
    {
        'plate_number': '京D22222',
        'driver_name': '赵六',
        'driver_phone': '13800138004',
        'driver_license': 'D1234567890',
        'vehicle_model': '中通LCK6105',
        'capacity': 48
    },
    {
        'plate_number': '京E33333',
        'driver_name': '钱七',
        'driver_phone': '13800138005',
        'driver_license': 'E1234567890',
        'vehicle_model': '亚星JS6101',
        'capacity': 42
    }
]

# 测试围栏数据
TEST_GEOFENCES = [
    {
        'name': '阳光小学',
        'fence_type': 'school',
        'center_lat': 39.9042,
        'center_lng': 116.4074,
        'radius': 500,
        'threshold': 3,
        'description': '阳光小学上下学区域'
    },
    {
        'name': '建国门危险路段',
        'fence_type': 'danger',
        'center_lat': 39.9087,
        'center_lng': 116.4341,
        'radius': 300,
        'threshold': 3,
        'description': '建国门附近交通繁忙危险路段'
    },
    {
        'name': '幸福社区',
        'fence_type': 'home',
        'center_lat': 39.9100,
        'center_lng': 116.3800,
        'radius': 1000,
        'threshold': 3,
        'description': '学生家庭所在社区区域'
    }
]


def generate_random_location(base_lat: float = 39.9042, base_lng: float = 116.4074, radius_km: float = 5.0) -> Dict[str, float]:
    """
    生成随机位置坐标
    
    Args:
        base_lat: 基准纬度
        base_lng: 基准经度
        radius_km: 半径（公里）
        
    Returns:
        包含latitude和longitude的字典
    """
    # 转换半径为度（近似值）
    lat_radius = radius_km / 111.0
    lng_radius = radius_km / (111.0 * abs(base_lat))
    
    # 生成随机偏移
    lat_offset = random.uniform(-lat_radius, lat_radius)
    lng_offset = random.uniform(-lng_radius, lng_radius)
    
    return {
        'latitude': base_lat + lat_offset,
        'longitude': base_lng + lng_offset
    }


def generate_test_vehicles(db: Session) -> List[Vehicle]:
    """
    生成测试车辆数据
    
    Args:
        db: 数据库会话
        
    Returns:
        创建的车辆列表
    """
    created_vehicles = []
    
    for i, vehicle_data in enumerate(TEST_VEHICLES):
        # 生成随机初始位置
        location = generate_random_location()
        
        # 创建设备ID
        device_id = f'DEV{str(i + 1).zfill(6)}'
        
        # 创建车辆
        vehicle = Vehicle(
            plate_number=vehicle_data['plate_number'],
            driver_name=vehicle_data['driver_name'],
            driver_phone=vehicle_data['driver_phone'],
            driver_license=vehicle_data['driver_license'],
            vehicle_model=vehicle_data['vehicle_model'],
            capacity=vehicle_data['capacity'],
            status='online',
            device_id=device_id,
            current_lat=location['latitude'],
            current_lng=location['longitude'],
            current_speed=random.uniform(0, 60),
            current_direction=random.randint(0, 360),
            last_online_time=datetime.now(),
            last_location_time=datetime.now()
        )
        
        db.add(vehicle)
        db.flush()
        created_vehicles.append(vehicle)
    
    db.commit()
    print(f"成功创建 {len(created_vehicles)} 辆测试车辆")
    return created_vehicles


def generate_test_geofences(db: Session) -> List[Geofence]:
    """
    生成测试围栏数据
    
    Args:
        db: 数据库会话
        
    Returns:
        创建的围栏列表
    """
    created_geofences = []
    
    for fence_data in TEST_GEOFENCES:
        geofence = Geofence(
            name=fence_data['name'],
            fence_type=fence_data['fence_type'],
            center_lat=fence_data['center_lat'],
            center_lng=fence_data['center_lng'],
            radius=fence_data['radius'],
            threshold=fence_data['threshold'],
            description=fence_data['description'],
            is_active=True
        )
        
        db.add(geofence)
        db.flush()
        created_geofences.append(geofence)
    
    db.commit()
    print(f"成功创建 {len(created_geofences)} 个测试围栏")
    return created_geofences


def generate_test_alerts(db: Session, vehicles: List[Vehicle] = None) -> List[Alert]:
    """
    生成测试预警数据
    
    Args:
        db: 数据库会话
        vehicles: 车辆列表（可选）
        
    Returns:
        创建的预警列表
    """
    if not vehicles:
        vehicles = db.query(Vehicle).limit(5).all()
    
    if not vehicles:
        print("没有可用的车辆，无法生成测试预警")
        return []
    
    created_alerts = []
    
    # 预警类型
    alert_types = ['geofence_violation', 'over_speed', 'deviation_route']
    severities = ['high', 'medium', 'low']
    
    for i in range(TEST_DATA_CONFIG['alert_count']):
        vehicle = random.choice(vehicles)
        
        alert = Alert(
            vehicle_id=vehicle.id,
            alert_type=random.choice(alert_types),
            severity=random.choice(severities),
            latitude=vehicle.current_lat + random.uniform(-0.01, 0.01),
            longitude=vehicle.current_lng + random.uniform(-0.01, 0.01),
            speed=vehicle.current_speed,
            direction=vehicle.current_direction,
            violation_count=random.randint(1, 5),
            geofence_id=random.randint(1, 3) if random.random() > 0.5 else None,
            fence_name=random.choice(['阳光小学', '建国门危险路段', '幸福社区']) if random.random() > 0.5 else None,
            message='测试预警消息',
            status='active' if i < 3 else 'resolved',
            created_at=datetime.now() - timedelta(hours=i * 2)
        )
        
        db.add(alert)
        db.flush()
        
        # 创建通知记录
        notification = AlertNotification(
            alert_id=alert.id,
            notify_type='driver',
            notify_target=vehicle.driver_phone,
            notify_content=f'测试预警通知：车辆{vehicle.plate_number}发生预警',
            notify_status='sent'
        )
        db.add(notification)
        
        created_alerts.append(alert)
    
    db.commit()
    print(f"成功创建 {len(created_alerts)} 条测试预警")
    return created_alerts


def generate_mock_gps_data(vehicle_id: int, device_id: str = None, 
                           base_lat: float = 39.9042, base_lng: float = 116.4074,
                           is_violation: bool = False) -> Dict[str, Any]:
    """
    生成模拟GPS数据（用于测试GPS接收端点）
    
    Args:
        vehicle_id: 车辆ID
        device_id: 设备ID
        base_lat: 基准纬度
        base_lng: 基准经度
        is_violation: 是否生成越界数据
        
    Returns:
        GPS数据字典
    """
    # 生成位置
    if is_violation:
        # 越界数据：离基准点较远
        location = generate_random_location(base_lat, base_lng, radius_km=10.0)
    else:
        # 正常数据：离基准点较近
        location = generate_random_location(base_lat, base_lng, radius_km=2.0)
    
    gps_data = {
        'device_id': device_id or f'DEV{str(vehicle_id).zfill(6)}',
        'vehicle_id': vehicle_id,
        'latitude': location['latitude'],
        'longitude': location['longitude'],
        'speed': random.uniform(0, 80),
        'direction': random.randint(0, 360),
        'altitude': random.uniform(20, 100),
        'satellites': random.randint(5, 12),
        'gps_accuracy': random.uniform(1, 10),
        'location_time': datetime.now().isoformat(),
        'data_source': 'gps'
    }
    
    return gps_data


def clear_all_test_data(db: Session) -> None:
    """
    清除所有测试数据
    
    Args:
        db: 数据库会话
    """
    # 删除通知记录
    db.query(AlertNotification).delete()
    
    # 删除预警记录
    db.query(Alert).delete()
    
    # 删除围栏
    db.query(Geofence).delete()
    
    # 删除车辆
    db.query(Vehicle).delete()
    
    db.commit()
    print("已清除所有测试数据")


def init_all_test_data(db: Session) -> Dict[str, int]:
    """
    初始化所有测试数据
    
    Args:
        db: 数据库会话
        
    Returns:
        包含各数据类型数量的字典
    """
    print("开始初始化测试数据...")
    
    # 创建车辆
    vehicles = generate_test_vehicles(db)
    
    # 创建围栏
    geofences = generate_test_geofences(db)
    
    # 创建预警
    alerts = generate_test_alerts(db, vehicles)
    
    result = {
        'vehicles': len(vehicles),
        'geofences': len(geofences),
        'alerts': len(alerts)
    }
    
    print(f"测试数据初始化完成：车辆 {result['vehicles']}, 围栏 {result['geofences']}, 预警 {result['alerts']}")
    return result


if __name__ == '__main__':
    # 测试代码
    from database import engine
    from models import Base
    
    # 创建表（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 初始化测试数据
        init_all_test_data(db)
    finally:
        db.close()
