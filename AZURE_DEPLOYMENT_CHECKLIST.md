# Azure App Service Quick Deployment Checklist
## TestGenie Enterprise - Ready for Azure!

### ✅ What's Ready for Deployment

**Files Created:**
- [ ] `application.py` (Azure entry point) ✅ 
- [ ] `requirements.txt` (Production dependencies) ✅
- [ ] `startup.py` (Azure startup config) ✅
- [ ] `deploy-azure.bat` (Deployment script) ✅
- [ ] Azure extensions installed ✅

### 🚀 Quick Deployment (Choose Your Method)

#### Option A: VS Code Deployment (Easiest)
1. [ ] Open VS Code in your project folder
2. [ ] Press `Ctrl+Shift+P` → "Azure: Sign In"
3. [ ] Press `Ctrl+Shift+P` → "Azure App Service: Create New Web App"
   - App name: `testgenie-enterprise-[yourname]`
   - Runtime: **Python 3.11**
   - Pricing: **Free (F1)** for testing
4. [ ] Right-click project folder → "Deploy to Web App"
5. [ ] Choose your new app → Deploy
6. [ ] Set environment variables (see below)

#### Option B: Deployment Package
1. [ ] Run `.\deploy-azure.bat` 
2. [ ] Upload `testgenie-deploy.zip` to Azure Portal
3. [ ] Configure settings (see below)

### ⚙️ Azure Configuration

**Environment Variables** (Azure Portal → App Service → Configuration):
```
FLASK_ENV = production
SECRET_KEY = your-super-secure-secret-key-123
AZURE_OPENAI_API_KEY = your-azure-openai-key
AZURE_OPENAI_ENDPOINT = https://your-resource.openai.azure.com/
```

**Startup Command** (General Settings):
```
python application.py
```

### 🧪 Test Your Deployment

- [ ] Visit: `https://testgenie-enterprise-[yourname].azurewebsites.net`
- [ ] Create a test project
- [ ] Generate AI test cases
- [ ] Verify all features work

### ✅ Local Environment Preparation
- [ ] Git repository initialized
- [ ] All sensitive data moved to environment variables
- [ ] `.gitignore` file configured
- [ ] Azure deployment files created
- [ ] Production requirements file ready

### ✅ Application Configuration
- [ ] Production configuration tested locally
- [ ] Database initialization script working
- [ ] AI service integration tested
- [ ] Static files properly configured

## 🚀 Deployment Steps

### Step 1: Initialize Git Repository
```bash
cd "C:\Users\2148336\OneDrive - Cognizant\Desktop\MVP"
git init
git add .
git commit -m "Initial TestGenie Enterprise commit"
```

### Step 2: Create Azure Resources
```bash
# Install Azure CLI if not already installed
az login

# Create resource group
az group create --name testgenie-rg --location "East US"

# Create App Service plan
az appservice plan create --name testgenie-plan --resource-group testgenie-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group testgenie-rg --plan testgenie-plan --name testgenie-enterprise --runtime "PYTHON|3.11"
```

### Step 3: Configure App Service Settings
```bash
# Set environment variables
az webapp config appsettings set --resource-group testgenie-rg --name testgenie-enterprise --settings \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    AZURE_OPENAI_API_KEY="your-azure-openai-key" \
    AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint" \
    OPENAI_API_KEY="your-openai-key"

# Set startup command
az webapp config set --resource-group testgenie-rg --name testgenie-enterprise --startup-file "startup.sh"
```

### Step 4: Deploy Application
```bash
# Option A: Deploy from local Git
az webapp deployment source config-local-git --name testgenie-enterprise --resource-group testgenie-rg
git remote add azure <deployment-url>
git push azure main

# Option B: Deploy via VS Code
# 1. Install Azure App Service extension
# 2. Right-click project folder
# 3. Select "Deploy to Web App..."
# 4. Choose your App Service
```

### Step 5: Verify Deployment
- [ ] App service URL accessible
- [ ] Database initialized properly
- [ ] AI integration working
- [ ] All pages loading correctly
- [ ] Test case creation working
- [ ] AI test generation working

## 🔧 Azure DevOps Setup (Optional)

### Step 1: Create Azure DevOps Project
1. Go to https://dev.azure.com
2. Create new organization (if needed)
3. Create new project "TestGenie Enterprise"

### Step 2: Setup Repository
```bash
# Add Azure DevOps remote
git remote add origin https://dev.azure.com/your-org/TestGenie-Enterprise/_git/TestGenie-Enterprise
git push -u origin main
```

### Step 3: Create Build Pipeline
1. Go to Pipelines > Create Pipeline
2. Select Azure Repos Git
3. Select your repository
4. Use the existing `azure-pipelines.yml` file
5. Update variables in the pipeline file:
   - `azureSubscription`
   - `appServiceName`
   - `resourceGroup`

### Step 4: Setup Service Connection
1. Go to Project Settings > Service connections
2. Create new Azure Resource Manager connection
3. Authorize with your Azure subscription
4. Use this connection name in your pipeline

## 🔒 Security Configuration

### Environment Variables to Set in Azure
```
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key>
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
OPENAI_API_KEY=<your-openai-key>
DATABASE_URL=<optional-azure-sql-connection-string>
```

### Security Features to Enable
- [ ] HTTPS only (App Service SSL settings)
- [ ] Custom domain (optional)
- [ ] Application Insights for monitoring
- [ ] Azure Key Vault for secrets (recommended)

## 📊 Post-Deployment Monitoring

### Application Insights Setup
```bash
# Create Application Insights
az monitor app-insights component create --app testgenie-insights --location "East US" --resource-group testgenie-rg

# Connect to App Service
az webapp config appsettings set --resource-group testgenie-rg --name testgenie-enterprise --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="<instrumentation-key>"
```

### Health Checks
- [ ] Application startup logs
- [ ] Database connectivity
- [ ] AI service availability
- [ ] Response times
- [ ] Error rates

## 🚨 Troubleshooting Common Issues

### Database Issues
- Ensure database file is writable in App Service
- Check SQLite limitations in App Service
- Consider migrating to Azure SQL for production

### AI Service Issues
- Verify API keys are set correctly
- Check endpoint URLs
- Monitor rate limits and quotas

### Performance Issues
- Enable Application Insights
- Check App Service plan scaling
- Monitor memory and CPU usage

## 📞 Support Resources
- **Azure Documentation**: https://docs.microsoft.com/azure/app-service/
- **Azure DevOps**: https://docs.microsoft.com/azure/devops/
- **Python on Azure**: https://docs.microsoft.com/azure/app-service/quickstart-python

---

**Ready to deploy?** Start with the Git repository initialization and follow the steps above! 🚀
