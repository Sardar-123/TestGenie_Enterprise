@echo off
REM Azure App Service Deployment Script for Windows

echo 🚀 Starting Azure deployment preparation...
echo.

REM Create deployment package
echo 📦 Creating deployment package...
powershell -Command "Compress-Archive -Path '.\*' -DestinationPath '.\testgenie-deploy.zip' -Force -Exclude 'venv\*','__pycache__\*','*.pyc','.git\*','*.db','testgenie-deploy.zip'"

echo ✅ Deployment package created: testgenie-deploy.zip
echo.
echo 📋 Next steps:
echo 1. Upload testgenie-deploy.zip to Azure App Service
echo 2. Set environment variables in Azure portal:
echo    - FLASK_ENV=production
echo    - SECRET_KEY=your-secret-key
echo    - AZURE_OPENAI_API_KEY=your-key
echo    - AZURE_OPENAI_ENDPOINT=your-endpoint
echo 3. Configure startup command: python application.py
echo 4. Test your deployment
echo.
echo 🌐 Your app will be available at: https://your-app-name.azurewebsites.net
echo.
pause
