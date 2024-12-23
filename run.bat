@echo off
REM Lấy thư mục chứa file .bat hiện tại
set current_dir=%~dp0

REM Chuyển đến thư mục hiện tại (đảm bảo không phụ thuộc đường dẫn cố định)
cd /d "%current_dir%"\\CODE

REM Chạy file Python
python ToolKhaoSat.py


