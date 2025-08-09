@echo off
echo 🔧 Azure DevOps Pipeline Configuration Helper
echo =============================================
echo.

echo Please provide the following information:
echo.

set /p SUBSCRIPTION_NAME="1. Your Azure Subscription Name: "
set /p APP_SERVICE_NAME="2. Your App Service Name (will be created): "
set /p RESOURCE_GROUP="3. Your Resource Group Name (default: testgenie-rg): "
if "%RESOURCE_GROUP%"=="" set RESOURCE_GROUP=testgenie-rg

echo.
echo 📝 Update your azure-pipelines.yml with these values:
echo ==================================================
echo.
echo variables:
echo   azureSubscription: '%SUBSCRIPTION_NAME%'
echo   appServiceName: '%APP_SERVICE_NAME%'
echo   resourceGroup: '%RESOURCE_GROUP%'
echo.
echo 🌐 Your app will be accessible at:
echo https://%APP_SERVICE_NAME%.azurewebsites.net
echo.
echo ✅ Copy these values and update your pipeline configuration!
echo.
pause
