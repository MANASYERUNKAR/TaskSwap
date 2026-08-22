@echo off
REM Run TaskSwap on localhost with non-secure development cookies.
set TASKSWAP_INSECURE_COOKIES=1
call .venv\Scripts\activate.bat
python manage.py runserver
