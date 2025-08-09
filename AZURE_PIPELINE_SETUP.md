# Azure DevOps Pipeline Setup Guide
## Step-by-Step Instructions for TestGenie Deployment

### 🚀 **Phase 1: Create Azure App Service Resource**

Before setting up the pipeline, you need to create the Azure App Service resource:

#### **1.1 Log into Azure Portal**
- Go to: https://portal.azure.com
- Sign in with your Azure account

#### **1.2 Create Resource Group** (if not exists)
```bash
Resource Group Name: testgenie-rg
Location: East US (or your preferred region)
```

#### **1.3 Create App Service Plan**
1. Search for "App Service Plans" → Create
2. **Settings:**
   - Name: `testgenie-plan`
   - Operating System: `Linux`
   - Pricing Tier: `Basic B1` (or Free F1 for testing)
   - Region: Same as resource group

#### **1.4 Create Web App**
1. Search for "App Services" → Create → Web App
2. **Basic Settings:**
   - Name: `testgenie-enterprise-[unique-suffix]`
   - Resource Group: `testgenie-rg`
   - Runtime stack: `Python 3.11`
   - Operating System: `Linux`
   - App Service Plan: `testgenie-plan`

3. **Important:** Note down your App Service name (you'll need it for pipeline)

---

### 🔧 **Phase 2: Configure Pipeline Variables**

#### **2.1 Update Pipeline Configuration**
You need to update the following in `azure-pipelines.yml`:

```yaml
variables:
  azureSubscription: 'YOUR_AZURE_SUBSCRIPTION_NAME'
  appServiceName: 'your-actual-app-service-name'  
  resourceGroup: 'testgenie-rg'
```

#### **2.2 Find Your Azure Subscription**
- In Azure Portal → Subscriptions
- Copy the subscription name (not the ID)

---

### 🚀 **Phase 3: Create Azure DevOps Pipeline**

#### **3.1 Go to Azure DevOps**
- URL: https://dev.azure.com/Vibects5/2148336
- Navigate to **Pipelines** section

#### **3.2 Create New Pipeline**
1. Click **"New pipeline"**
2. Select **"Azure Repos Git"**
3. Choose your repository: `2148336`
4. Select **"Existing Azure Pipelines YAML file"**
5. Choose `/azure-pipelines.yml`

#### **3.3 Configure Service Connection**
1. When prompted, create **Azure Resource Manager** service connection
2. Choose **Service principal (automatic)**
3. Select your subscription and resource group
4. Name it: `azure-testgenie-connection`
5. Save and authorize

#### **3.4 Update Pipeline Variables**
Before running, you'll need to update these values in the pipeline:
- `azureSubscription`: Name of your service connection
- `appServiceName`: Your actual App Service name
- `resourceGroup`: `testgenie-rg`

---

### 🔐 **Phase 4: Configure Environment Variables**

#### **4.1 Set App Service Configuration**
In Azure Portal → Your App Service → Configuration → Application settings:

```bash
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
OPENAI_API_KEY=your_openai_key (if using OpenAI)
FLASK_ENV=production
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

#### **4.2 Set Python Version**
In Azure Portal → Your App Service → Configuration → General settings:
- Python version: `3.11`

---

### ✅ **Phase 5: Run the Pipeline**

#### **5.1 Commit Pipeline Configuration**
```bash
git add azure-pipelines.yml
git commit -m "Configure Azure DevOps pipeline"
git push origin master
```

#### **5.2 Run Pipeline**
1. Go to Azure DevOps → Pipelines
2. Select your pipeline
3. Click **"Run pipeline"**
4. Monitor the build and deployment

#### **5.3 Expected Pipeline Stages**
1. **Build Stage**: Install dependencies, run tests
2. **Deploy Stage**: Deploy to Azure App Service
3. **Verification**: App should be accessible at your Azure URL

---

### 🌐 **Phase 6: Access Your Deployed Application**

Once deployed successfully:
- **URL**: `https://your-app-service-name.azurewebsites.net`
- **Admin Interface**: Available at the root URL
- **API Endpoints**: `/api/projects`, `/api/test-cases`, etc.

---

### 🔧 **Troubleshooting**

#### **Common Issues:**
1. **Build fails**: Check Python dependencies in `requirements.txt`
2. **Deployment fails**: Verify service connection permissions
3. **App won't start**: Check Application logs in Azure Portal
4. **Database issues**: Ensure SQLite file permissions

#### **Where to Check Logs:**
- Azure Portal → App Service → Log stream
- Azure DevOps → Pipeline → Failed task details

---

### 📝 **Next Steps After Successful Deployment**

1. **Test all features** in production environment
2. **Set up monitoring** (Application Insights)
3. **Configure custom domain** (if needed)
4. **Set up staging slots** for safe deployments
5. **Enable continuous deployment** on code changes

---

## 🎯 **Ready to Start?**

Follow Phase 1 first (create Azure resources), then proceed with the pipeline setup!
