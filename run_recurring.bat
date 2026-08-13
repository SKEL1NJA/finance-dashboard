@echo off
cd /d C:\Users\khann\OneDrive\Desktop\finance-dashboard
call venv\Scripts\activate.bat
python manage.py process_recurring >> recurring_log.txt 2>&1