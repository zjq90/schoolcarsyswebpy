import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 50)
    print("  校车后台管理系统启动中...")
    print("=" * 50)
    print("\n系统信息:")
    print("  - 技术栈: Python + FastAPI + SQLite + Bootstrap V4")
    print("  - 访问地址: http://localhost:8000")
    print("  - API文档: http://localhost:8000/docs")
    print("\n默认账号:")
    print("  - 管理员: admin / admin123")
    print("  - 司机: driver1~driver6 / 123456")
    print("  - 老师: teacher1~teacher3 / 123456")
    print("\n启动步骤:")
    print("  1. 安装依赖: pip install -r requirements.txt")
    print("  2. 启动服务: python start.py")
    print("  3. 访问系统: 浏览器打开 http://localhost:8000")
    print("  4. 初始化数据: 登录后访问 /test 页面点击初始化测试数据")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
