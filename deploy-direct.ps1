# Direct Azure Deployment via Local Git
# Run this script if you want to deploy directly without Azure DevOps pipelines

Write-Host "🚀 Setting up Direct Azure Deployment" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "Since you don't have Azure DevOps permissions, we'll use direct deployment methods." -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 Available Options:" -ForegroundColor Cyan
Write-Host "1. Azure Portal Deployment Center (Recommended)" -ForegroundColor White
Write-Host "2. Local Git Deployment" -ForegroundColor White  
Write-Host "3. VS Code Azure Extension" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Which method would you like to use? (1/2/3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🌟 Azure Portal Deployment Center" -ForegroundColor Green
        Write-Host "=================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Steps to follow:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://portal.azure.com" -ForegroundColor White
        Write-Host "2. Navigate to App Service: cts-vibeappso2111-5" -ForegroundColor White
        Write-Host "3. Click 'Deployment Center' in the left menu" -ForegroundColor White
        Write-Host "4. Choose 'External Git' as source" -ForegroundColor White
        Write-Host "5. Repository URL: https://dev.azure.com/Vibects5/2148336/_git/2148336" -ForegroundColor White
        Write-Host "6. Branch: master" -ForegroundColor White
        Write-Host "7. Click Save and let Azure deploy!" -ForegroundColor White
        Write-Host ""
        Write-Host "🔧 Don't forget to set environment variables in App Service Configuration!" -ForegroundColor Red
        Start-Process "https://portal.azure.com"
    }
    "2" {
        Write-Host ""
        Write-Host "🔧 Local Git Deployment Setup" -ForegroundColor Green
        Write-Host "=============================" -ForegroundColor Green
        Write-Host ""
        Write-Host "First, you need to get the Git URL from Azure Portal:" -ForegroundColor Yellow
        Write-Host "1. Go to App Service: cts-vibeappso2111-5" -ForegroundColor White
        Write-Host "2. Deployment Center → Local Git" -ForegroundColor White
        Write-Host "3. Copy the Git URL" -ForegroundColor White
        Write-Host "4. Set deployment credentials" -ForegroundColor White
        Write-Host ""
        $gitUrl = Read-Host "Paste the Azure Git URL here"
        
        if ($gitUrl) {
            Write-Host ""
            Write-Host "Adding Azure as remote repository..." -ForegroundColor Yellow
            git remote add azure $gitUrl
            
            Write-Host ""
            Write-Host "Ready to deploy! Run this command when ready:" -ForegroundColor Green
            Write-Host "git push azure master" -ForegroundColor Cyan
        }
    }
    "3" {
        Write-Host ""
        Write-Host "💻 VS Code Azure Extension" -ForegroundColor Green
        Write-Host "==========================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Steps:" -ForegroundColor Yellow
        Write-Host "1. Install Azure App Service extension in VS Code" -ForegroundColor White
        Write-Host "2. Open this project in VS Code" -ForegroundColor White
        Write-Host "3. Sign in to Azure" -ForegroundColor White
        Write-Host "4. Right-click project → 'Deploy to Web App'" -ForegroundColor White
        Write-Host "5. Select your subscription and app service" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening VS Code..." -ForegroundColor Yellow
        code .
    }
    default {
        Write-Host ""
        Write-Host "Please choose 1, 2, or 3" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🌐 Your deployed app will be accessible at:" -ForegroundColor Green
Write-Host "https://cts-vibeappso2111-5.azurewebsites.net" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 For detailed instructions, check: DIRECT_AZURE_DEPLOYMENT.md" -ForegroundColor Yellow
