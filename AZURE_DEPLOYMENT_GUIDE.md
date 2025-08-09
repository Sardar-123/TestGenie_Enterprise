# Azure Deployment Guide for TestGenie Enterprise

## 🚀 Azure Services Available
- **Azure DevOps** - Source control, CI/CD pipelines, work item tracking
- **Azure App Services** - Web application hosting platform
- **Azure SQL Database** - Managed database service (optional upgrade from SQLite)

## 📋 Deployment Options

### Option 1: Quick Azure App Service Deployment
**Best for**: Immediate deployment with minimal changes
- Keep SQLite database (file-based)
- Deploy directly to Azure App Service
- Simple and fast setup

### Option 2: Enterprise Azure Deployment
**Best for**: Production-ready enterprise solution
- Migrate to Azure SQL Database
- Use Azure Key Vault for secrets
- Implement Azure Application Insights
- Set up Azure DevOps CI/CD pipeline

## 🛠️ Prerequisites Checklist

### Azure Resources Needed
- [ ] Azure App Service plan
- [ ] Azure App Service (Web App)
- [ ] Azure DevOps organization/project
- [ ] Azure SQL Database (optional)
- [ ] Azure Key Vault (recommended)
- [ ] Azure Application Insights (recommended)

### Local Preparation
- [ ] Git repository initialized
- [ ] Environment variables configured
- [ ] Database migration scripts ready
- [ ] Azure CLI installed
- [ ] VS Code Azure extensions

## 🚀 Quick Start - Option 1 (SQLite + App Service)

### Step 1: Prepare for Git
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial TestGenie Enterprise commit"
```

### Step 2: Azure App Service Configuration
- Runtime: Python 3.11
- Operating System: Linux
- Startup Command: `python enterprise_test_platform_sqlite.py`
- Environment Variables: Azure OpenAI keys

### Step 3: Deploy via VS Code
- Install Azure App Service extension
- Right-click project → Deploy to Web App
- Select/create App Service
- Deploy!

## 🏢 Enterprise Setup - Option 2 (Full Azure Stack)

### Database Migration
1. **Azure SQL Database**
   - Create Azure SQL server and database
   - Update connection string
   - Run migration scripts

2. **Key Vault Integration**
   - Store API keys securely
   - Configure managed identity
   - Update app configuration

### CI/CD Pipeline Setup
1. **Azure DevOps Repository**
   - Push code to Azure Repos
   - Set up branch policies
   - Configure pull request workflows

2. **Build Pipeline**
   - Python application build
   - Run tests
   - Create deployment artifacts

3. **Release Pipeline**
   - Deploy to staging environment
   - Run integration tests
   - Deploy to production

## 📁 Required Files for Azure Deployment

### Web.config (for Windows App Service)
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="D:\home\python\python.exe"
                  arguments="D:\home\site\wwwroot\enterprise_test_platform_sqlite.py"
                  stdoutLogEnabled="true"
                  stdoutLogFile="D:\home\LogFiles\python.log"
                  startupTimeLimit="60"
                  requestTimeout="00:04:00">
    </httpPlatform>
  </system.webServer>
</configuration>
```

### startup.sh (for Linux App Service)
```bash
#!/bin/bash
pip install -r requirements.txt
python enterprise_test_platform_sqlite.py
```

## 🔧 Environment Configuration

### Application Settings (Azure App Service)
```
FLASK_ENV=production
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
OPENAI_API_KEY=<your-openai-key>
DATABASE_URL=<azure-sql-connection-string>  # If using Azure SQL
```

### Local Development vs Azure
- **Local**: Uses `.env` file and SQLite
- **Azure**: Uses App Settings and Azure SQL/SQLite

## 📊 Monitoring & Analytics
- **Application Insights**: Track performance and errors
- **Log Analytics**: Centralized logging
- **Azure Monitor**: Infrastructure monitoring
- **Health Checks**: Automated availability monitoring

## 🔒 Security Best Practices
- Use Azure Key Vault for secrets
- Enable Azure AD authentication (optional)
- Configure HTTPS only
- Set up CORS policies
- Enable Application Gateway (for enterprise)

## 🚦 Next Steps

Choose your deployment approach:
1. **Quick Deploy**: Start with Option 1 for immediate results
2. **Enterprise Setup**: Use Option 2 for production-ready deployment
3. **Hybrid Approach**: Start with Option 1, then migrate to Option 2

Would you like me to help you with a specific deployment option?
