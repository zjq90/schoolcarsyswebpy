"""
系统配置文件
"""

import os


class Settings:
    """
    系统配置类
    """
    
    PROJECT_NAME: str = "校车后台管理系统"
    PROJECT_VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "sqlite:///./schoolbus.db"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    def __init__(self):
        self.ALARM_LEVELS: dict = {
            1: {
                "name": "一级报警",
                "color": "red",
                "description": "事故、火灾、劫持等紧急情况",
                "response_mechanism": "一键报警 → 监控中心 → 警方联动"
            },
            2: {
                "name": "二级报警",
                "color": "orange",
                "description": "超速、偏离路线、长时间停留、有病情",
                "response_mechanism": "自动录音录像 → 推送至学校管理员"
            },
            3: {
                "name": "三级报警",
                "color": "blue",
                "description": "车门异常开启、学生滞留、一般违规行为",
                "response_mechanism": "提醒司机复核 → 推送家长确认"
            }
        }
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        self.STATIC_DIR = os.path.join(project_root, "frontend", "static")
        self.TEMPLATES_DIR = os.path.join(project_root, "frontend", "templates")


# 创建配置实例
settings = Settings()
