@echo off
echo Starting Flask App...
cd /d "%~dp0"
call venv\Scripts\activate
python app.py
start http://127.0.0.1:5000/
pause