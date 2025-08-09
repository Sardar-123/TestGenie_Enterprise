@echo off
echo 🚀 Direct Azure Deployment Helper
echo =================================
echo.
echo Since you don't have Azure DevOps permissions, let's use direct deployment!
echo.
echo 📋 Choose your deployment method:
echo.
echo 1. Azure Portal Deployment Center (Recommended)
echo 2. Local Git Deployment  
echo 3. VS Code Azure Extension
echo.
echo 🌟 RECOMMENDED: Azure Portal Deployment Center
echo ===============================================
echo.
echo Steps:
echo 1. Go to: https://portal.azure.com
echo 2. Find App Service: cts-vibeappso2111-5
echo 3. Go to "Deployment Center"
echo 4. Choose "External Git"
echo 5. Repository URL: https://dev.azure.com/Vibects5/2148336/_git/2148336
echo 6. Branch: master
echo 7. Save and deploy!
echo.
echo 🔧 BEFORE deployment, set these in App Service Configuration:
echo AZURE_OPENAI_API_KEY=your_key
echo AZURE_OPENAI_ENDPOINT=your_endpoint  
echo FLASK_ENV=production
echo SCM_DO_BUILD_DURING_DEPLOYMENT=true
echo.
echo 🌐 Your app will be at: https://cts-vibeappso2111-5.azurewebsites.net
echo.
echo Would you like to try the Azure Portal method? (It's the easiest!)
echo.
pause
