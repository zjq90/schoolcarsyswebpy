"""
校车管理系统 - 消息推送和状态数据访问层
提供学生、消息推送和校车状态相关的数据库操作
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime

from database.db import execute_query, execute_update, get_table_count


class StudentDAO:
    """
    学生数据访问类
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有学生列表
        """
        query = "SELECT * FROM students ORDER BY created_at DESC"
        return execute_query(query)

    @staticmethod
    def get_by_id(student_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取学生信息
        """
        query = "SELECT * FROM students WHERE id = ?"
        return execute_query(query, (student_id,), fetchone=True)

    @staticmethod
    def get_by_card(card_id: str) -> Optional[Dict[str, Any]]:
        """
        根据卡号获取学生信息
        """
        query = "SELECT * FROM students WHERE card_id = ?"
        return execute_query(query, (card_id,), fetchone=True)

    @staticmethod
    def create(name: str, student_no: str = None, class_name: str = None,
               card_id: str = None, parent_phone: str = None,
               status: str = "active") -> int:
        """
        创建新学生
        """
        query = """
            INSERT INTO students (name, student_no, class_name, card_id, parent_phone, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        return execute_update(query, (name, student_no, class_name, card_id, parent_phone, status))

    @staticmethod
    def update(student_id: int, **kwargs) -> bool:
        """
        更新学生信息
        """
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        query = f"UPDATE students SET {set_clause} WHERE id = ?"
        params = list(kwargs.values()) + [student_id]
        return execute_update(query, tuple(params)) > 0

    @staticmethod
    def delete(student_id: int) -> bool:
        """
        删除学生
        """
        query = "DELETE FROM students WHERE id = ?"
        return execute_update(query, (student_id,)) > 0

    @staticmethod
    def get_count() -> int:
        """
        获取学生总数
        """
        return get_table_count("students")


class MessagePushDAO:
    """
    消息推送数据访问类
    处理学生刷卡上下车的消息推送记录
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有消息推送记录，关联学生姓名
        """
        query = """
            SELECT mp.*, s.name as student_name
            FROM message_push_logs mp
            LEFT JOIN students s ON mp.student_id = s.id
            ORDER BY mp.push_time DESC
        """
        return execute_query(query)

    @staticmethod
    def get_by_id(message_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取消息推送记录
        """
        query = """
            SELECT mp.*, s.name as student_name
            FROM message_push_logs mp
            LEFT JOIN students s ON mp.student_id = s.id
            WHERE mp.id = ?
        """
        return execute_query(query, (message_id,), fetchone=True)

    @staticmethod
    def get_by_student(student_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定学生的消息推送记录
        """
        query = """
            SELECT mp.*, s.name as student_name
            FROM message_push_logs mp
            LEFT JOIN students s ON mp.student_id = s.id
            WHERE mp.student_id = ?
            ORDER BY mp.push_time DESC
            LIMIT ?
        """
        return execute_query(query, (student_id, limit))

    @staticmethod
    def get_by_type(message_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定类型的消息推送记录
        类型包括：上车刷卡、下车刷卡、校车发车、校车到站、异常通知
        """
        query = """
            SELECT mp.*, s.name as student_name
            FROM message_push_logs mp
            LEFT JOIN students s ON mp.student_id = s.id
            WHERE mp.message_type = ?
            ORDER BY mp.push_time DESC
            LIMIT ?
        """
        return execute_query(query, (message_type, limit))

    @staticmethod
    def create(student_id: int = None, message_type: str = "",
               content: str = "", push_time: datetime = None,
               status: str = "sent", receiver_phone: str = None) -> int:
        """
        创建消息推送记录
        """
        query = """
            INSERT INTO message_push_logs
            (student_id, message_type, content, push_time, status, receiver_phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        actual_push_time = push_time or datetime.now()
        return execute_update(query, (
            student_id, message_type, content, actual_push_time,
            status, receiver_phone
        ))

    @staticmethod
    def get_recent(hours: int = 24) -> List[Dict[str, Any]]:
        """
        获取最近N小时的消息推送记录
        """
        query = """
            SELECT mp.*, s.name as student_name
            FROM message_push_logs mp
            LEFT JOIN students s ON mp.student_id = s.id
            WHERE mp.push_time >= DATETIME('now', '-' || ? || ' hours')
            ORDER BY mp.push_time DESC
        """
        return execute_query(query, (hours,))

    @staticmethod
    def get_count() -> int:
        """
        获取消息推送记录总数
        """
        return get_table_count("message_push_logs")


class BusStatusDAO:
    """
    校车状态数据访问类
    处理校车发车、到站、异常状态记录
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有校车状态记录，关联车辆和司机信息
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            ORDER BY bs.record_time DESC
        """
        return execute_query(query)

    @staticmethod
    def get_by_id(status_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取校车状态记录
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            WHERE bs.id = ?
        """
        return execute_query(query, (status_id,), fetchone=True)

    @staticmethod
    def get_by_vehicle(vehicle_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定车辆的状态记录
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            WHERE bs.vehicle_id = ?
            ORDER BY bs.record_time DESC
            LIMIT ?
        """
        return execute_query(query, (vehicle_id, limit))

    @staticmethod
    def get_by_type(status_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取指定类型的状态记录
        类型包括：发车、到站、正常、异常
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            WHERE bs.status_type = ?
            ORDER BY bs.record_time DESC
            LIMIT ?
        """
        return execute_query(query, (status_type, limit))

    @staticmethod
    def create(vehicle_id: int, status_type: str, status_value: str,
               driver_id: int = None, location: str = None,
               record_time: datetime = None, description: str = None) -> int:
        """
        创建校车状态记录
        """
        query = """
            INSERT INTO bus_status_logs
            (vehicle_id, driver_id, status_type, status_value, location, record_time, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        actual_record_time = record_time or datetime.now()
        return execute_update(query, (
            vehicle_id, driver_id, status_type, status_value,
            location, actual_record_time, description
        ))

    @staticmethod
    def get_recent(hours: int = 24) -> List[Dict[str, Any]]:
        """
        获取最近N小时的校车状态记录
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            WHERE bs.record_time >= DATETIME('now', '-' || ? || ' hours')
            ORDER BY bs.record_time DESC
        """
        return execute_query(query, (hours,))

    @staticmethod
    def get_current_status(vehicle_id: int) -> Optional[Dict[str, Any]]:
        """
        获取指定车辆的最新状态
        """
        query = """
            SELECT bs.*, v.plate_number, d.name as driver_name
            FROM bus_status_logs bs
            LEFT JOIN vehicles v ON bs.vehicle_id = v.id
            LEFT JOIN drivers d ON bs.driver_id = d.id
            WHERE bs.vehicle_id = ?
            ORDER BY bs.record_time DESC
            LIMIT 1
        """
        return execute_query(query, (vehicle_id,), fetchone=True)

    @staticmethod
    def get_count() -> int:
        """
        获取校车状态记录总数
        """
        return get_table_count("bus_status_logs")
