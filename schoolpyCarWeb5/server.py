"""
校车后台管理系统 - 简单启动脚本
直接运行: python server.py
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("校车后台管理系统启动中...")
print(f"项目根目录: {project_root}")
print("=" * 60)

# 验证导入
try:
    print("\n[1/3] 验证配置模块...")
    from backend.app.config import settings
    print(f"  ✓ 静态文件目录: {settings.STATIC_DIR}")
    print(f"  ✓ 模板目录: {settings.TEMPLATES_DIR}")
except Exception as e:
    print(f"  ✗ 配置模块导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n[2/3] 验证数据库模块...")
    from backend.app.database import engine, Base
    print(f"  ✓ 数据库引擎: {engine}")
except Exception as e:
    print(f"  ✗ 数据库模块导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n[3/3] 验证FastAPI应用...")
    from backend.app.main import app
    print(f"  ✓ 应用标题: {app.title}")
    print(f"  ✓ 路由数量: {len(app.routes)}")
except Exception as e:
    print(f"  ✗ FastAPI应用导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("所有模块验证通过！")
print("=" * 60)
print(f"\n访问地址: http://127.0.0.1:8000")
print(f"API文档: http://127.0.0.1:8000/docs")
print("\n按 Ctrl+C 停止服务器\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
