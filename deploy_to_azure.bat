@echo off
echo 🚀 TestGenie Azure Deployment Helper
echo =====================================

echo.
echo This script will help you deploy TestGenie to Azure App Service
echo.

echo Step 1: Initialize Git Repository
echo ----------------------------------
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial TestGenie Enterprise commit for Azure deployment"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo Step 2: Check Azure CLI
echo -----------------------
az --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Azure CLI not found. Please install Azure CLI first:
    echo https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
    pause
    exit /b 1
) else (
    echo ✅ Azure CLI is available
)

echo.
echo Step 3: Login to Azure
echo ----------------------
echo Please login to your Azure account...
az login

echo.
echo Step 4: Azure Resource Configuration
echo ------------------------------------
echo Please provide the following information:

set /p RESOURCE_GROUP="Resource Group Name (default: testgenie-rg): "
if "%RESOURCE_GROUP%"=="" set RESOURCE_GROUP=testgenie-rg

set /p APP_NAME="App Service Name (must be globally unique): "
if "%APP_NAME%"=="" (
    echo ❌ App Service name is required and must be globally unique
    pause
    exit /b 1
)

set /p LOCATION="Azure Region (default: East US): "
if "%LOCATION%"=="" set LOCATION="East US"

echo.
echo Creating Azure resources...
echo Resource Group: %RESOURCE_GROUP%
echo App Service: %APP_NAME%
echo Location: %LOCATION%

echo.
echo Step 5: Create Azure Resources
echo ------------------------------

echo Creating resource group...
az group create --name %RESOURCE_GROUP% --location "%LOCATION%"

echo Creating App Service plan...
az appservice plan create --name %APP_NAME%-plan --resource-group %RESOURCE_GROUP% --sku B1 --is-linux

echo Creating Web App...
az webapp create --resource-group %RESOURCE_GROUP% --plan %APP_NAME%-plan --name %APP_NAME% --runtime "PYTHON|3.11"

echo.
echo Step 6: Configure App Service
echo -----------------------------

echo Setting startup command...
az webapp config set --resource-group %RESOURCE_GROUP% --name %APP_NAME% --startup-file "startup.sh"

echo Setting basic app settings...
az webapp config appsettings set --resource-group %RESOURCE_GROUP% --name %APP_NAME% --settings ^
    FLASK_ENV=production ^
    PYTHONUNBUFFERED=1 ^
    SCM_DO_BUILD_DURING_DEPLOYMENT=true

echo.
echo ⚠️ IMPORTANT: Set your AI API keys
echo Please run the following commands with your actual API keys:
echo.
echo az webapp config appsettings set --resource-group %RESOURCE_GROUP% --name %APP_NAME% --settings ^
echo     AZURE_OPENAI_API_KEY="your-azure-openai-key" ^
echo     AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint" ^
echo     OPENAI_API_KEY="your-openai-key"
echo.

echo.
echo Step 7: Deploy Application
echo --------------------------

echo Setting up deployment source...
az webapp deployment source config-local-git --name %APP_NAME% --resource-group %RESOURCE_GROUP%

echo.
echo ✅ Azure resources created successfully!
echo.
echo Your app will be available at: https://%APP_NAME%.azurewebsites.net
echo.
echo Next steps:
echo 1. Set your AI API keys using the command above
echo 2. Deploy your code:
echo    git remote add azure https://%APP_NAME%.scm.azurewebsites.net:443/%APP_NAME%.git
echo    git push azure main
echo.
echo 3. Or deploy using VS Code Azure App Service extension
echo.

echo 📊 Deployment Summary
echo ---------------------
echo Resource Group: %RESOURCE_GROUP%
echo App Service: %APP_NAME%
echo URL: https://%APP_NAME%.azurewebsites.net
echo.

pause
