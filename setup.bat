@echo off
SETLOCAL

python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python chua duoc cai dat, dang cai dat cho m ne
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.11.4/python-3.11.4.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait"
    echo Python cai thanh cong r cu
) ELSE (
    echo Python co san roi
)

echo Dang cap nhat pip...
python -m pip install --upgrade pip

echo Kiem tra phien ban Python va pip...
python --version
pip --version

echo Cai dat cac thu vien can thiet ne...
pip install selenium pyperclip webdriver-manager discord.py pyautogui

echo Cai xong r, gio chay run la dc, sau nay k can chay setup nx

ENDLOCAL
pause
