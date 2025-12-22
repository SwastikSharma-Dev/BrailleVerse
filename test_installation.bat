@echo off
REM Quick test script to verify installation

echo Testing Django Installation...
echo.

call C:\Users\swast\anaconda3\Scripts\activate.bat
call conda activate drf

echo Checking Python version...
python --version

echo.
echo Checking Django version...
python -c "import django; print('Django version:', django.get_version())"

echo.
echo Running Django tests...
python manage.py test braille_app

echo.
echo Running Django check...
python manage.py check

echo.
echo ======================================
echo If all tests passed, you're ready!
echo Run start_server.bat to launch the website
echo ======================================

pause
