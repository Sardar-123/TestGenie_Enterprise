# TestGenie Azure App Service Deployment Guide
## Quick Deployment Option

This guide will help you deploy TestGenie to Azure App Service in the fastest way possible.

## Prerequisites ✅

- Azure subscription with App Service access
- Azure DevOps account
- Your TestGenie code ready (SQLite version)

## Step 1: Prepare Your Application for Azure

### 1.1 Create Azure-Ready Requirements File
Your app needs specific dependencies for Azure deployment:

```bash
# Run this to create production requirements
pip freeze > requirements.txt
```

### 1.2 Verify Application Entry Point
Azure App Service will look for:
- `app.py` or 
- `application.py` or
- A startup command in `web.config`

## Step 2: Azure App Service Deployment

### Option A: Deploy from VS Code (Recommended)

1. **Install Azure Extension**
   - Open VS Code
   - Install "Azure App Service" extension
   - Sign in to your Azure account

2. **Deploy Application**
   - Right-click on your project folder
   - Select "Deploy to Web App..."
   - Choose "Create new Web App"
   - Select your subscription and resource group
   - Choose Python runtime (3.11 or 3.12)
   - Wait for deployment to complete

### Option B: Deploy via Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name testgenie-rg --location "East US"

# Create App Service plan
az appservice plan create --name testgenie-plan --resource-group testgenie-rg --sku FREE --is-linux

# Create web app
az webapp create --name testgenie-enterprise --resource-group testgenie-rg --plan testgenie-plan --runtime "PYTHON:3.11"

# Deploy code
az webapp deployment source config-zip --resource-group testgenie-rg --name testgenie-enterprise --src testgenie.zip
```

### Option C: Deploy from Azure DevOps

1. **Create Azure DevOps Project**
2. **Push code to Azure Repos**
3. **Create Build Pipeline**
4. **Create Release Pipeline**
5. **Deploy to App Service**

## Step 3: Configure Environment Variables

In Azure App Service, set these application settings:

```
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-here
DATABASE_URL=sqlite:///testgenie.db
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
OPENAI_API_KEY=your-openai-key-if-using
```

## Step 4: Configure Startup Command

Set the startup command in Azure App Service:

```bash
python enterprise_test_platform_sqlite.py
```

## Step 5: Test Deployment

1. **Access your application**
   - URL: `https://testgenie-enterprise.azurewebsites.net`
   - Check all features work
   - Test AI integration
   - Verify database persistence

2. **Monitor Application**
   - Check App Service logs
   - Monitor performance
   - Set up alerts

## Database Considerations

### Current: SQLite
- ✅ **Pros**: Simple, no additional cost, works immediately
- ⚠️ **Limitations**: Data resets on app restart, not scalable

### Upgrade Options:
1. **Azure SQL Database** (Recommended for production)
2. **PostgreSQL on Azure**
3. **Azure Cosmos DB**

## Next Steps

1. **Custom Domain**: Add your own domain name
2. **SSL Certificate**: Enable HTTPS (free with App Service)
3. **Scaling**: Configure auto-scaling rules
4. **Monitoring**: Set up Application Insights
5. **CI/CD**: Automate deployments with Azure DevOps

## Troubleshooting

### Common Issues:
1. **App won't start**: Check startup command and logs
2. **500 errors**: Verify environment variables
3. **AI not working**: Check API keys in configuration
4. **Database issues**: Verify SQLite file permissions

### Useful Commands:
```bash
# View logs
az webapp log tail --name testgenie-enterprise --resource-group testgenie-rg

# Restart app
az webapp restart --name testgenie-enterprise --resource-group testgenie-rg

# Scale app
az webapp scale --name testgenie-enterprise --resource-group testgenie-rg --instances 2
```

## Security Best Practices

1. **Environment Variables**: Never commit secrets to code
2. **HTTPS Only**: Enable HTTPS redirect
3. **Authentication**: Consider Azure AD integration
4. **Network Security**: Configure access restrictions if needed

---

🚀 **Ready to deploy? Let's start with Step 1!**
