"""
校车管理系统 - 数据库连接模块
提供SQLite数据库的连接和操作功能
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from config import DATABASE, BASE_DIR

# 数据库文件路径
DB_PATH = DATABASE['path']


@contextmanager
def get_connection():
    """
    数据库连接上下文管理器
    使用with语句自动管理连接的打开和关闭
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让返回结果可以像字典一样访问
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: tuple = None, fetchone: bool = False) -> Any:
    """
    执行查询语句（SELECT）
    
    Args:
        query: SQL查询语句
        params: 查询参数元组
        fetchone: 是否只获取第一条记录
    
    Returns:
        查询结果，fetchone=True时返回字典，否则返回字典列表
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        
        if fetchone:
            return dict(rows[0]) if rows else None
        
        # 将Row对象转换为字典列表
        result = []
        for row in rows:
            result.append(dict(row))
        return result


def execute_update(query: str, params: tuple = None) -> int:
    """
    执行更新语句（INSERT, UPDATE, DELETE）
    
    Args:
        query: SQL更新语句
        params: 更新参数元组
    
    Returns:
        受影响的行数或新插入的ID
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        
        # 如果是INSERT语句，返回新插入的ID
        if query.strip().upper().startswith('INSERT'):
            return cursor.lastrowid
        
        return cursor.rowcount


def execute_batch(query: str, params_list: List[tuple]) -> int:
    """
    批量执行更新语句
    
    Args:
        query: SQL更新语句
        params_list: 参数元组列表
    
    Returns:
        受影响的总行数
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount


def table_exists(table_name: str) -> bool:
    """
    检查表是否存在
    
    Args:
        table_name: 表名
    
    Returns:
        表是否存在
    """
    query = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """
    result = execute_query(query, (table_name,), fetchone=True)
    return result is not None


def get_table_count(table_name: str, condition: str = None, params: tuple = None) -> int:
    """
    获取表中记录数量
    
    Args:
        table_name: 表名
        condition: WHERE条件（不含WHERE关键字）
        params: 条件参数
    
    Returns:
        记录数量
    """
    query = f"SELECT COUNT(*) as cnt FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    
    result = execute_query(query, params, fetchone=True)
    return result['cnt'] if result else 0
