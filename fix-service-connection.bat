@echo off
echo 🔍 Azure DevOps Service Connection Helper
echo ========================================
echo.
echo This error means the Azure service connection is missing.
echo.
echo 📋 Quick Fix Steps:
echo.
echo 1. Go to Azure DevOps Project Settings:
echo    https://dev.azure.com/Vibects5/2148336/_settings/
echo.
echo 2. Click "Service connections" in the left menu
echo.
echo 3. Click "New service connection" 
echo.
echo 4. Choose "Azure Resource Manager"
echo.
echo 5. Select "Service principal (automatic)"
echo.
echo 6. Fill in:
echo    - Subscription: cb6255866a-vibecode06-az
echo    - Resource Group: CTS-VibeAppso211
echo    - Service connection name: Azure-Service-Connection
echo.
echo 7. Check "Grant access permission to all pipelines"
echo.
echo 8. Click "Save"
echo.
echo ✅ Then re-run your pipeline!
echo.
echo 🌐 Pipeline URL: 
echo https://dev.azure.com/Vibects5/2148336/_build
echo.
pause
