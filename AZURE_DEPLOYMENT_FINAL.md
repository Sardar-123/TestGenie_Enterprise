# TestGenie Azure Deployment Configuration
## Organization-Managed Azure Resources

### 🏢 **Your Azure Environment**
- **Subscription**: `cb6255866a-vibecode06-az`
- **Resource Group**: `CTS-VibeAppso211`
- **App Service Name**: `cts-vibeappso2111-5`
- **Domain**: `cts-vibeappso2111-5.azurewebsites.net`

### 🚀 **Deployment URL**
Once deployed, your TestGenie platform will be accessible at:
**https://cts-vibeappso2111-5.azurewebsites.net**

### 📋 **Pipeline Configuration Status**
✅ **azure-pipelines.yml** configured with correct values
✅ **application.py** updated for Azure compatibility
✅ **Code repository** ready in Azure DevOps

### 🔧 **Next Steps for Pipeline Setup**

#### **1. Create Azure DevOps Pipeline**
1. Go to: https://dev.azure.com/Vibects5/2148336
2. Navigate to **Pipelines** → **New pipeline**
3. Select **"Azure Repos Git"**
4. Choose repository: **"2148336"**
5. Select **"Existing Azure Pipelines YAML file"**
6. Choose path: **`/azure-pipelines.yml`**

#### **2. Configure Service Connection**
When prompted to create service connection:
1. Choose **"Azure Resource Manager"**
2. Select **"Service principal (automatic)"**
3. **Subscription**: `cb6255866a-vibecode06-az`
4. **Resource Group**: `CTS-VibeAppso211`
5. **Connection Name**: `azure-testgenie-connection`
6. Click **"Save and authorize"**

#### **3. Configure App Service Settings**
Before first deployment, set these in Azure Portal:
- Go to: **Azure Portal** → **App Services** → **cts-vibeappso2111-5**
- Navigate to: **Configuration** → **Application settings**

**Required Environment Variables:**
```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
FLASK_ENV=production
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

**Python Configuration:**
- Go to: **Configuration** → **General settings**
- **Stack**: Python
- **Major version**: 3.11
- **Startup Command**: `python application.py`

#### **4. Run the Pipeline**
1. In Azure DevOps pipeline, click **"Run pipeline"**
2. Monitor the build and deployment process
3. Once complete, test at: https://cts-vibeappso2111-5.azurewebsites.net

### 🔍 **Pipeline Stages**
1. **Build**: Install Python dependencies, prepare application
2. **Deploy**: Deploy to Azure App Service
3. **Verification**: Health check of deployed application

### 📊 **Expected Features After Deployment**
✅ **TestGenie Dashboard** - Project management interface
✅ **AI Test Generation** - Azure OpenAI integration
✅ **Database Storage** - SQLite persistent storage
✅ **REST APIs** - All CRUD operations
✅ **Modern UI** - Bootstrap 5 responsive design

### 🔐 **Security Notes**
- All sensitive configuration stored in App Service settings
- No API keys committed to repository
- HTTPS enabled by default on Azure App Service

### 📞 **Support**
If deployment fails:
1. Check **Azure DevOps** → **Pipelines** → **Failed run logs**
2. Check **Azure Portal** → **App Service** → **Log stream**
3. Verify all environment variables are set correctly

---

**Ready to create the pipeline in Azure DevOps!** 🚀
