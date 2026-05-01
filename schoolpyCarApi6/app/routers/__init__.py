"""
API路由模块
============

包含所有API路由定义:
- parent: 家长端API路由
  - 登录/注册
  - 学生绑定
  - 消息列表/详情
  - 消息分类查询
  - 投诉提交
- driver: 司机端API路由
  - 登录/注册
  - 上下班打卡
  - 车辆绑定
  - 调度消息
  - 推送消息
  - 反馈提交
  - 紧急状况申请
  - 路线规划
  - 违章查询
"""

from app.routers.parent import router as parent_router
from app.routers.driver import router as driver_router

__all__ = ["parent_router", "driver_router"]
