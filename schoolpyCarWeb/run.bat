@echo off
chcp 65001 >nul
setlocal

set PYTHONPATH=%~dp0venv_packages;%PYTHONPATH%
set PYTHONIOENCODING=utf-8

echo ==================================================
echo 校车管理系统启动脚本
echo ==================================================
echo.
echo Python路径: %PYTHONPATH%
echo.

cd /d "%~dp0"

python start_server.py

pause
