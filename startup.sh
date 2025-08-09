# Azure App Service Startup Script for Linux
#!/bin/bash

echo "🚀 Starting TestGenie Enterprise on Azure App Service"
echo "=================================================="

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_azure.txt

# Set environment variables for production
export FLASK_ENV=production
export PYTHONUNBUFFERED=1

# Initialize database if needed
echo "🗄️ Checking database..."
python -c "
import os
if not os.path.exists('testgenie.db') or os.path.getsize('testgenie.db') == 0:
    print('Initializing database...')
    exec(open('init_db_simple.py').read())
else:
    print('Database already exists')
"

# Start the application
echo "🌐 Starting TestGenie server..."
python enterprise_test_platform_sqlite.py
