"""
短信验证码工具函数
===================

包含验证码生成、存储和验证功能。

注意：在生产环境中，应该使用真正的短信服务提供商。
这里使用内存存储验证码，仅用于演示和测试。
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from app.config import settings

_sms_code_store: Dict[str, Tuple[str, datetime]] = {}


def generate_verify_code(length: int = None) -> str:
    """
    生成短信验证码

    Args:
        length: 验证码长度，默认使用配置中的长度

    Returns:
        str: 数字验证码字符串
    """
    if length is None:
        length = settings.SMS_CODE_LENGTH
    return "".join(random.choices(string.digits, k=length))


def send_sms_code(phone: str, code: str = None) -> str:
    """
    发送短信验证码

    注意：这是一个模拟函数。在生产环境中，
    应该调用真实的短信服务API（如阿里云、腾讯云等）。

    Args:
        phone: 手机号
        code: 验证码，不传则自动生成

    Returns:
        str: 生成的验证码
    """
    if code is None:
        code = generate_verify_code()

    expire_minutes = settings.SMS_CODE_EXPIRE_MINUTES
    expire_time = datetime.now() + timedelta(minutes=expire_minutes)

    _sms_code_store[phone] = (code, expire_time)

    print(f"[模拟短信] 手机号: {phone}, 验证码: {code}, 有效期: {expire_minutes}分钟")

    return code


def verify_sms_code(phone: str, code: str) -> Tuple[bool, str]:
    """
    验证短信验证码

    Args:
        phone: 手机号
        code: 用户输入的验证码

    Returns:
        Tuple[bool, str]: (是否验证通过, 提示消息)
    """
    if phone not in _sms_code_store:
        return False, "验证码不存在或已过期"

    stored_code, expire_time = _sms_code_store[phone]

    if datetime.now() > expire_time:
        del _sms_code_store[phone]
        return False, "验证码已过期"

    if stored_code != code:
        return False, "验证码错误"

    del _sms_code_store[phone]
    return True, "验证成功"


def clear_expired_codes():
    """
    清理过期的验证码

    可以定期调用此函数来清理内存中的过期验证码。
    """
    now = datetime.now()
    expired_phones = [
        phone for phone, (_, expire_time) in _sms_code_store.items()
        if now > expire_time
    ]
    for phone in expired_phones:
        del _sms_code_store[phone]
