import sys
import os

# 添加本地包目录到路径
venv_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv_packages')
if os.path.exists(venv_packages):
    sys.path.insert(0, venv_packages)

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 现在可以导入了
from scripts.init_test_data import init_test_data

print("="*50)
print("初始化测试数据...")
print("="*50)
init_test_data()

print("\n" + "="*50)
print("启动FastAPI服务器...")
print("="*50)
print("访问地址: http://localhost:8080/")
print("API文档: http://localhost:8080/api/docs")
print("按 Ctrl+C 停止服务器\n")

import uvicorn
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8080,
    reload=True
)
