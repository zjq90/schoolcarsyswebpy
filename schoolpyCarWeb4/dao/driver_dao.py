"""
校车管理系统 - 司机数据访问层
提供司机和评分相关的数据库操作
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime

from database.db import execute_query, execute_update, get_table_count
from config import SCORE_RULES


class DriverDAO:
    """
    司机数据访问类
    """

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有司机列表
        """
        query = "SELECT * FROM drivers ORDER BY created_at DESC"
        return execute_query(query)

    @staticmethod
    def get_by_id(driver_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取司机信息
        """
        query = "SELECT * FROM drivers WHERE id = ?"
        return execute_query(query, (driver_id,), fetchone=True)

    @staticmethod
    def create(name: str, phone: str = None, license_no: str = None,
               hire_date: date = None, status: str = "active") -> int:
        """
        创建新司机
        """
        query = """
            INSERT INTO drivers (name, phone, license_no, hire_date, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        return execute_update(query, (name, phone, license_no, hire_date, status))

    @staticmethod
    def update(driver_id: int, **kwargs) -> bool:
        """
        更新司机信息
        """
        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        query = f"""
            UPDATE drivers SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = list(kwargs.values()) + [driver_id]
        return execute_update(query, tuple(params)) > 0

    @staticmethod
    def delete(driver_id: int) -> bool:
        """
        删除司机
        """
        query = "DELETE FROM drivers WHERE id = ?"
        return execute_update(query, (driver_id,)) > 0

    @staticmethod
    def get_count() -> int:
        """
        获取司机总数
        """
        return get_table_count("drivers")


class DriverScoreDAO:
    """
    司机评分数据访问类
    """

    @staticmethod
    def calculate_score(violation_count: int, complaint_count: int,
                        safe_driving_hours: float) -> float:
        """
        根据评分规则计算信用分
        公式: 基础分 - 违章*扣分 - 投诉*扣分 + 安全驾驶*加分
        """
        score = (
            SCORE_RULES['base_score']
            - violation_count * SCORE_RULES['violation_penalty']
            - complaint_count * SCORE_RULES['complaint_penalty']
            + safe_driving_hours * SCORE_RULES['safe_hour_bonus']
        )
        # 限制分数在0-100之间
        return max(0.0, min(100.0, score))

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        获取所有评分记录，关联司机姓名
        """
        query = """
            SELECT ds.*, d.name as driver_name
            FROM driver_scores ds
            LEFT JOIN drivers d ON ds.driver_id = d.id
            ORDER BY ds.score_date DESC
        """
        return execute_query(query)

    @staticmethod
    def get_by_id(score_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取评分记录
        """
        query = """
            SELECT ds.*, d.name as driver_name
            FROM driver_scores ds
            LEFT JOIN drivers d ON ds.driver_id = d.id
            WHERE ds.id = ?
        """
        return execute_query(query, (score_id,), fetchone=True)

    @staticmethod
    def get_by_driver(driver_id: int, limit: int = 30) -> List[Dict[str, Any]]:
        """
        获取指定司机的评分记录
        """
        query = """
            SELECT ds.*, d.name as driver_name
            FROM driver_scores ds
            LEFT JOIN drivers d ON ds.driver_id = d.id
            WHERE ds.driver_id = ?
            ORDER BY ds.score_date DESC
            LIMIT ?
        """
        return execute_query(query, (driver_id, limit))

    @staticmethod
    def create(driver_id: int, score_date: date, violation_count: int = 0,
               complaint_count: int = 0, safe_driving_hours: float = 0.0,
               notes: str = None) -> int:
        """
        创建评分记录（自动计算信用分）
        """
        credit_score = DriverScoreDAO.calculate_score(
            violation_count, complaint_count, safe_driving_hours
        )
        query = """
            INSERT INTO driver_scores
            (driver_id, score_date, violation_count, complaint_count, 
             safe_driving_hours, credit_score, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        return execute_update(query, (
            driver_id, score_date, violation_count, complaint_count,
            safe_driving_hours, credit_score, notes
        ))

    @staticmethod
    def get_by_date(score_date: date) -> List[Dict[str, Any]]:
        """
        获取指定日期的所有评分记录
        """
        query = """
            SELECT ds.*, d.name as driver_name
            FROM driver_scores ds
            LEFT JOIN drivers d ON ds.driver_id = d.id
            WHERE ds.score_date = ?
            ORDER BY ds.driver_id
        """
        return execute_query(query, (score_date,))

    @staticmethod
    def get_average_score(driver_id: int, days: int = 30) -> Optional[float]:
        """
        获取指定司机最近N天的平均信用分
        """
        query = """
            SELECT AVG(credit_score) as avg_score
            FROM driver_scores
            WHERE driver_id = ?
            AND score_date >= DATE('now', '-' || ? || ' days')
        """
        result = execute_query(query, (driver_id, days), fetchone=True)
        return result['avg_score'] if result and result['avg_score'] else None

    @staticmethod
    def get_count() -> int:
        """
        获取评分记录总数
        """
        return get_table_count("driver_scores")
