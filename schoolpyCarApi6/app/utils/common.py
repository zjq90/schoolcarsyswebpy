"""
通用工具函数
=============

包含通用的工具函数，如时间处理、响应封装等。
"""

import random
import string
from datetime import datetime
from typing import Any, Dict, Optional


def get_current_time() -> datetime:
    """
    获取当前时间

    Returns:
        datetime: 当前时间
    """
    return datetime.now()


def generate_random_string(length: int = 10) -> str:
    """
    生成随机字符串

    Args:
        length: 字符串长度

    Returns:
        str: 随机字符串（包含字母和数字）
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


def generate_random_number(length: int = 6) -> str:
    """
    生成随机数字字符串

    Args:
        length: 数字长度

    Returns:
        str: 随机数字字符串
    """
    return "".join(random.choices(string.digits, k=length))


def create_success_response(
    data: Any = None,
    message: str = "success",
    code: int = 200
) -> Dict[str, Any]:
    """
    创建成功响应

    Args:
        data: 响应数据
        message: 响应消息
        code: 状态码

    Returns:
        Dict[str, Any]: 响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def create_error_response(
    message: str = "error",
    code: int = 400,
    data: Any = None
) -> Dict[str, Any]:
    """
    创建错误响应

    Args:
        message: 错误消息
        code: 状态码
        data: 附加数据

    Returns:
        Dict[str, Any]: 响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def format_phone(phone: str) -> str:
    """
    格式化手机号

    移除手机号中的空格、横线等分隔符。

    Args:
        phone: 原始手机号

    Returns:
        str: 格式化后的手机号
    """
    return phone.strip().replace("-", "").replace(" ", "").replace("+86", "")


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式

    简单验证手机号是否为11位数字。

    Args:
        phone: 手机号

    Returns:
        bool: 是否符合格式
    """
    phone = format_phone(phone)
    return len(phone) == 11 and phone.isdigit()


def calculate_page_offset(page: int, page_size: int) -> int:
    """
    计算分页偏移量

    Args:
        page: 页码（从1开始）
        page_size: 每页数量

    Returns:
        int: 偏移量
    """
    return (page - 1) * page_size


def calculate_total_pages(total: int, page_size: int) -> int:
    """
    计算总页数

    Args:
        total: 总记录数
        page_size: 每页数量

    Returns:
        int: 总页数
    """
    if total == 0:
        return 0
    return (total + page_size - 1) // page_size
