"""
工具函数模块
==============

包含通用工具函数:
- auth: 认证相关工具
  - JWT令牌生成与验证
  - 密码加密与验证
  - 用户认证依赖
- sms: 短信验证码工具
  - 验证码生成与存储
  - 验证码验证
- common: 通用工具
  - 时间处理
  - 随机字符串生成
  - 响应封装
"""

from app.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    get_current_user,
    get_current_active_user,
)
from app.utils.sms import (
    generate_verify_code,
    send_sms_code,
    verify_sms_code,
)
from app.utils.common import (
    get_current_time,
    generate_random_string,
    create_success_response,
    create_error_response,
)

__all__ = [
    "get_password_hash",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "get_current_active_user",
    "generate_verify_code",
    "send_sms_code",
    "verify_sms_code",
    "get_current_time",
    "generate_random_string",
    "create_success_response",
    "create_error_response",
]
