import sys
import os

def check_environment():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("="*50)
    print("检查Python环境...")
    print("="*50)
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")

    venv_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv_packages')
    if os.path.exists(venv_packages):
        print(f"\n添加本地包目录: {venv_packages}")
        sys.path.insert(0, venv_packages)

    print("\n当前sys.path:")
    for p in sys.path:
        print(f"  - {p}")

    print("\n" + "="*50)
    print("测试导入必要的包...")
    print("="*50)

    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'pydantic',
        'jinja2', 'jose', 'passlib', 'bcrypt'
    ]

    all_ok = True
    for pkg in required_packages:
        try:
            if pkg == 'jose':
                from jose import JWTError, jwt
                print(f"  [OK] {pkg} (python-jose)")
            else:
                __import__(pkg)
                print(f"  [OK] {pkg}")
        except ImportError as e:
            print(f"  [ERROR] {pkg}: {e}")
            all_ok = False

    return all_ok

def run_server():
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    print(f"\n项目目录: {project_root}")
    
    try:
        from main import app
        print("[OK] 应用加载成功")
        
        import uvicorn
        print("\n" + "="*50)
        print("启动FastAPI服务器...")
        print("="*50)
        print("访问地址: http://localhost:8080/")
        print("API文档: http://localhost:8080/api/docs")
        print("按 Ctrl+C 停止服务器\n")
        
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        print(f"[ERROR] 启动失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    all_ok = check_environment()
    
    if all_ok:
        print("\n所有必要的包已安装!")
        print("\n尝试启动服务器...")
        run_server()
    else:
        print("\n" + "="*50)
        print("缺少必要的包")
        print("="*50)
        print("\n请手动安装以下包:")
        print("  pip install fastapi uvicorn sqlalchemy pydantic python-multipart jinja2 aiofiles python-jose[cryptography] passlib[bcrypt] bcrypt")

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
