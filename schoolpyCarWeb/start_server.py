"""
启动脚本
用于解决Python路径问题并启动FastAPI服务器
"""
import sys
import os

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 添加本地包目录到路径
venv_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv_packages')
if os.path.exists(venv_packages) and venv_packages not in sys.path:
    sys.path.insert(0, venv_packages)
    print("已添加本地包目录:", venv_packages)

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print("已添加项目目录:", project_root)

# 打印当前Python路径
print("Python解释器:", sys.executable)
print("Python版本:", sys.version)

# 尝试导入所需的包
print("\n" + "="*50)
print("检查依赖包...")
print("="*50)

try:
    import fastapi
    print("[OK] fastapi:", fastapi.__version__)
except ImportError as e:
    print("[ERROR] fastapi导入失败:", e)

try:
    import sqlalchemy
    print("[OK] sqlalchemy:", sqlalchemy.__version__)
except ImportError as e:
    print("[ERROR] sqlalchemy导入失败:", e)

try:
    import uvicorn
    print("[OK] uvicorn:", uvicorn.__version__)
except ImportError as e:
    print("[ERROR] uvicorn导入失败:", e)

try:
    import pydantic
    print("[OK] pydantic:", pydantic.__version__)
except ImportError as e:
    print("[ERROR] pydantic导入失败:", e)

try:
    import jinja2
    print("[OK] jinja2:", jinja2.__version__)
except ImportError as e:
    print("[ERROR] jinja2导入失败:", e)

print("\n" + "="*50)
print("初始化测试数据...")
print("="*50)

try:
    from scripts.init_test_data import init_test_data
    init_test_data()
except Exception as e:
    print("\n[ERROR] 初始化测试数据失败:", e)
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("启动FastAPI服务器...")
print("="*50)
print("访问地址: http://localhost:8080/")
print("API文档: http://localhost:8080/api/docs")
print("按 Ctrl+C 停止服务器\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
