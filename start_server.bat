@echo off
REM Braille Display Website - Startup Script
REM This script activates the conda environment and starts the Django server

echo ======================================
echo Braille Display Website
echo ======================================
echo.

REM Activate conda environment
echo Activating conda environment 'drf'...
call C:\Users\swast\anaconda3\Scripts\activate.bat
call conda activate drf

echo.
echo Checking Django installation...
python -c "import django; print('Django version:', django.get_version())"

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo ======================================
echo Starting Django development server...
echo ======================================
echo.
echo Open your browser to: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
