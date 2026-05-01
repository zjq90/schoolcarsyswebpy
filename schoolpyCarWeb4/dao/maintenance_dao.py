"""
校车管理系统 - 运维记录数据访问层
提供车辆和运维记录相关的数据库操作
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime

from database.db import execute_query, execute_update, get_table_count


class VehicleDAO:
    """
    车辆数据访问类
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有车辆列表
        """
        query = "SELECT * FROM vehicles ORDER BY created_at DESC"
        return execute_query(query)

    @staticmethod
    def get_by_id(vehicle_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取车辆信息
        """
        query = "SELECT * FROM vehicles WHERE id = ?"
        return execute_query(query, (vehicle_id,), fetchone=True)

    @staticmethod
    def get_by_plate(plate_number: str) -> Optional[Dict[str, Any]]:
        """
        根据车牌号获取车辆信息
        """
        query = "SELECT * FROM vehicles WHERE plate_number = ?"
        return execute_query(query, (plate_number,), fetchone=True)

    @staticmethod
    def create(plate_number: str, vehicle_type: str = None, capacity: int = None,
               purchase_date: date = None, status: str = "active") -> int:
        """
        创建新车辆
        """
        query = """
            INSERT INTO vehicles (plate_number, vehicle_type, capacity, purchase_date, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        return execute_update(query, (plate_number, vehicle_type, capacity, purchase_date, status))

    @staticmethod
    def update(vehicle_id: int, **kwargs) -> bool:
        """
        更新车辆信息
        """
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        query = f"""
            UPDATE vehicles SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = list(kwargs.values()) + [vehicle_id]
        return execute_update(query, tuple(params)) > 0

    @staticmethod
    def delete(vehicle_id: int) -> bool:
        """
        删除车辆
        """
        query = "DELETE FROM vehicles WHERE id = ?"
        return execute_update(query, (vehicle_id,)) > 0

    @staticmethod
    def get_count() -> int:
        """
        获取车辆总数
        """
        return get_table_count("vehicles")


class MaintenanceDAO:
    """
    运维记录数据访问类
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有运维记录，关联车辆和司机信息
        """
        query = """
            SELECT mr.*, v.plate_number, d.name as driver_name
            FROM maintenance_records mr
            LEFT JOIN vehicles v ON mr.vehicle_id = v.id
            LEFT JOIN drivers d ON mr.driver_id = d.id
            ORDER BY mr.record_date DESC
        """
        return execute_query(query)

    @staticmethod
    def get_by_id(record_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取运维记录
        """
        query = """
            SELECT mr.*, v.plate_number, d.name as driver_name
            FROM maintenance_records mr
            LEFT JOIN vehicles v ON mr.vehicle_id = v.id
            LEFT JOIN drivers d ON mr.driver_id = d.id
            WHERE mr.id = ?
        """
        return execute_query(query, (record_id,), fetchone=True)

    @staticmethod
    def get_by_vehicle(vehicle_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定车辆的运维记录
        """
        query = """
            SELECT mr.*, v.plate_number, d.name as driver_name
            FROM maintenance_records mr
            LEFT JOIN vehicles v ON mr.vehicle_id = v.id
            LEFT JOIN drivers d ON mr.driver_id = d.id
            WHERE mr.vehicle_id = ?
            ORDER BY mr.record_date DESC
            LIMIT ?
        """
        return execute_query(query, (vehicle_id, limit))

    @staticmethod
    def get_by_type(record_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定类型的运维记录
        类型包括：年检、保险、维修、油耗
        """
        query = """
            SELECT mr.*, v.plate_number, d.name as driver_name
            FROM maintenance_records mr
            LEFT JOIN vehicles v ON mr.vehicle_id = v.id
            LEFT JOIN drivers d ON mr.driver_id = d.id
            WHERE mr.record_type = ?
            ORDER BY mr.record_date DESC
            LIMIT ?
        """
        return execute_query(query, (record_type, limit))

    @staticmethod
    def create(record_type: str, vehicle_id: int, record_date: date,
               driver_id: int = None, amount: float = 0.0,
               description: str = None, status: str = "completed") -> int:
        """
        创建运维记录
        """
        query = """
            INSERT INTO maintenance_records
            (record_type, vehicle_id, driver_id, record_date, amount, description, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        return execute_update(query, (
            record_type, vehicle_id, driver_id, record_date,
            amount, description, status
        ))

    @staticmethod
    def update(record_id: int, **kwargs) -> bool:
        """
        更新运维记录
        """
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        query = f"""
            UPDATE maintenance_records SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = list(kwargs.values()) + [record_id]
        return execute_update(query, tuple(params)) > 0

    @staticmethod
    def delete(record_id: int) -> bool:
        """
        删除运维记录
        """
        query = "DELETE FROM maintenance_records WHERE id = ?"
        return execute_update(query, (record_id,)) > 0

    @staticmethod
    def get_statistics_by_type(start_date: date = None, end_date: date = None) -> List[Dict[str, Any]]:
        """
        按类型统计运维金额
        """
        base_query = """
            SELECT record_type, COUNT(*) as record_count, SUM(amount) as total_amount
            FROM maintenance_records
            WHERE 1=1
        """
        params = []
        
        if start_date:
            base_query += " AND record_date >= ?"
            params.append(start_date)
        if end_date:
            base_query += " AND record_date <= ?"
            params.append(end_date)
        
        base_query += " GROUP BY record_type ORDER BY total_amount DESC"
        
        return execute_query(base_query, tuple(params) if params else None)

    @staticmethod
    def get_count() -> int:
        """
        获取运维记录总数
        """
        return get_table_count("maintenance_records")
