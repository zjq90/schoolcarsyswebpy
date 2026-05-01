"""
校车管理系统 - 配置文件
存储系统全局配置参数
"""
import os

# 项目基础目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE = {
    'path': os.path.join(BASE_DIR, 'database', 'school_bus.db'),
}

# 服务器配置
SERVER = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': True,
}

# 评分规则配置
SCORE_RULES = {
    'base_score': 100,           # 基础信用分
    'violation_penalty': 5,      # 每次违章扣分
    'complaint_penalty': 10,     # 每次投诉扣分
    'safe_hour_bonus': 0.5,      # 每安全驾驶1小时加分
}

# 消息推送配置
MESSAGE_CONFIG = {
    'message_types': [
        '上车刷卡',
        '下车刷卡',
        '校车发车',
        '校车到站',
        '异常通知'
    ],
}

# 状态类型配置
STATUS_TYPES = {
    'bus_status': ['发车', '到站', '正常', '异常'],
    'maintenance_types': ['年检', '保险', '维修', '油耗'],
}
