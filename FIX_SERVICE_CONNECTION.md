# Fix Azure Service Connection Issue
## Step-by-Step Solution

### 🚨 **The Problem**
The pipeline is looking for a service connection named `cb6255866a-vibecode06-az` which doesn't exist in your Azure DevOps project.

### ✅ **Solution: Create Service Connection**

#### **Step 1: Go to Azure DevOps Project Settings**
1. Go to: https://dev.azure.com/Vibects5/2148336
2. Click the **gear icon** (⚙️) in the bottom left
3. Select **"Project settings"**

#### **Step 2: Create Service Connection**
1. In the left menu, click **"Service connections"**
2. Click **"New service connection"**
3. Select **"Azure Resource Manager"**
4. Click **"Next"**

#### **Step 3: Configure Authentication**
1. Choose **"Service principal (automatic)"**
2. Click **"Next"**

#### **Step 4: Fill in Details**
```
Subscription: cb6255866a-vibecode06-az
Resource Group: CTS-VibeAppso211
Service connection name: Azure-Service-Connection
```

#### **Step 5: Grant Access Permission**
1. Check **"Grant access permission to all pipelines"**
2. Click **"Save"**

#### **Step 6: Verify Service Connection**
1. You should see the new service connection listed
2. Status should show as **"Ready"**

---

### 🔄 **Alternative: Use Existing Service Connection**

If you already have a service connection, you can update the pipeline instead:

#### **Option A: Find Existing Service Connection**
1. Go to **Project Settings** → **Service connections**
2. Look for any existing Azure connections
3. Note the exact name

#### **Option B: Update Pipeline Variable**
Update the `azureSubscription` variable in `azure-pipelines.yml` to match your existing service connection name.

---

### 🚀 **After Creating Service Connection**

#### **Step 1: Commit Updated Pipeline**
```bash
git add azure-pipelines.yml
git commit -m "Fix Azure service connection name"
git push origin master
```

#### **Step 2: Run Pipeline Again**
1. Go to **Pipelines** in Azure DevOps
2. Select your pipeline
3. Click **"Run pipeline"**
4. Monitor the execution

---

### 🎯 **Expected Result**
- ✅ Service connection authorization succeeds
- ✅ Build stage completes
- ✅ Deploy stage deploys to Azure App Service
- ✅ App accessible at: https://cts-vibeappso2111-5.azurewebsites.net

---

### 🔧 **Troubleshooting**

#### **If Service Connection Creation Fails:**
1. **Permission Issue**: Ask your Azure administrator for permissions
2. **Subscription Access**: Verify you have contributor access to the subscription
3. **Resource Group**: Ensure the resource group exists

#### **If Pipeline Still Fails:**
1. **Check service connection name** matches exactly in pipeline
2. **Verify permissions** on the service connection
3. **Check Azure subscription** is active and accessible

#### **Common Service Connection Names:**
- `Azure-Service-Connection`
- `azure-subscription`
- `Azure Resource Manager`
- Your custom name

---

## 📋 **Quick Checklist**
- [ ] Service connection created in Azure DevOps
- [ ] Service connection named `Azure-Service-Connection`
- [ ] Pipeline updated with correct service connection name
- [ ] Pipeline granted access to service connection
- [ ] Code committed and pushed
- [ ] Pipeline re-run successfully

**Ready to create the service connection?** 🚀
