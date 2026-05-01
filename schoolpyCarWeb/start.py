import sys
import os

def main():
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("="*50)
    print("校车管理系统 - 启动脚本")
    print("="*50)
    print("\n初始化测试数据...\n")

    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    try:
        from scripts.init_test_data import init_test_data
        init_test_data()
        print("\n[OK] 测试数据初始化完成")
    except Exception as e:
        print(f"\n[WARNING] 测试数据初始化跳过: {e}")

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
        reload=False
    )

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
