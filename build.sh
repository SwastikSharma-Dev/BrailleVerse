#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running migrations..."
python manage.py migrate --no-input

echo "Build complete!"

