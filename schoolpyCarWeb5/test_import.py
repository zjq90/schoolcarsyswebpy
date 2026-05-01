import sys
sys.path.insert(0, "d:/Aijava/javaproject/260422/SolcodePython/shcoolcarSysweb/v5/schoolpyCarWeb5")

try:
    from backend.app.schemas import AlarmResponse
    print("SUCCESS: AlarmResponse imported")
except Exception as e:
    print(f"ERROR: {e}")

try:
    from backend.app.schemas import AlarmSchema
    print("SUCCESS: AlarmSchema imported")
except Exception as e:
    print(f"ERROR: {e}")
