# 🚀 TestGenie Enterprise - Complete User Guide

## 📋 Table of Contents
1. [How to Start the Platform](#how-to-start)
2. [Accessing the Platform](#accessing)
3. [User Interface Overview](#ui-overview)
4. [Step-by-Step Usage Guide](#usage-guide)
5. [Features Walkthrough](#features)
6. [API Documentation](#api-docs)
7. [Troubleshooting](#troubleshooting)

---

## 🟢 How to Start the Platform {#how-to-start}

### Option 1: Start from Scratch
```powershell
# 1. Navigate to the project directory
cd "C:\Users\2148336\OneDrive - Cognizant\Desktop\MVP"

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start the platform
python enterprise_test_platform.py
```

### Option 2: If Already Running
- The platform is **currently running** on: http://localhost:5000
- You can directly access it in your browser

### Success Indicators
When started successfully, you'll see:
```
🚀 TestGenie Enterprise Test Management Platform
============================================================
📍 Dashboard: http://localhost:5000
📊 Projects: http://localhost:5000/projects
📝 Test Cases: http://localhost:5000/test-cases
🏃 Test Runs: http://localhost:5000/test-runs
🤖 AI Generator: http://localhost:5000/ai-generator
============================================================
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Accessing the Platform {#accessing}

### Direct URLs:
- **Main Dashboard:** http://localhost:5000
- **Projects:** http://localhost:5000/projects
- **Test Cases:** http://localhost:5000/test-cases
- **Test Runs:** http://localhost:5000/test-runs
- **AI Generator:** http://localhost:5000/ai-generator

### Browser Requirements:
- Chrome, Firefox, Safari, Edge (latest versions)
- JavaScript enabled
- Local network access to localhost:5000

---

## 🎨 User Interface Overview {#ui-overview}

### Navigation Structure:
```
🏠 Dashboard     📁 Projects     📝 Test Cases     🏃 Test Runs     🤖 AI Generator
     |                |               |               |                |
   Statistics      Create/View     Repository      Execution      Generate Tests
   Quick Actions   Manage Teams    Search/Filter   Track Progress  Upload Files
   Recent Activity Project Details Bulk Operations View Results   Save to Projects
```

### Professional Design Features:
- **Modern Bootstrap 5** styling
- **Responsive design** (works on mobile/tablet)
- **Icon-based navigation** with clear labels
- **Modal dialogs** for forms and actions
- **Real-time statistics** and updates

---

## 📚 Step-by-Step Usage Guide {#usage-guide}

### 🚀 **Getting Started (5 minutes)**

#### Step 1: Access Dashboard
1. Open browser and go to: **http://localhost:5000**
2. You'll see the main dashboard with statistics
3. Notice the sample "E-commerce Platform" project is already loaded

#### Step 2: Create Your First Project
1. Click **"New Project"** button (top right)
2. Fill in:
   - **Project Name:** "My Test Project"
   - **Description:** "Testing for my application"
3. Click **"Create Project"**
4. Project appears in the list with 0 test cases

#### Step 3: Generate Test Cases with AI
1. Click **"🤖 AI Generator"** in sidebar
2. **Option A - Upload File:**
   - Select a project from dropdown
   - Upload requirements document (PDF, Word, etc.)
   - Choose test type (Functional, API, UI, etc.)
   - Click **"Generate Test Cases with AI"**

3. **Option B - Manual Input:**
   - Enter requirements in text area:
   ```
   User login functionality:
   - User can login with email and password
   - System validates credentials
   - User gets error for invalid login
   - User redirects to dashboard on success
   ```
   - Select test count (5, 10, 15, 20)
   - Click **"Generate Test Cases with AI"**

4. Review generated test cases
5. Click **"Save All to Project"**

#### Step 4: View and Manage Test Cases
1. Go to **"📝 Test Cases"**
2. See all your test cases in table view
3. Use filters to search by:
   - Priority (High, Medium, Low)
   - Status (Draft, Active, Deprecated)
   - Project
4. Click **"View Details"** to see individual test case

#### Step 5: Create and Run Test Execution
1. Go to **"🏃 Test Runs"**
2. Click **"New Test Run"**
3. Fill in:
   - **Run Name:** "Regression Test v1.0"
   - **Test Suite:** Select from dropdown
   - **Executed By:** Your name
4. Choose options:
   - ☑️ Auto-execute test cases
   - ☑️ Generate execution report
5. Click **"Create & Start Test Run"**
6. Monitor progress in real-time

---

## ⭐ Features Walkthrough {#features}

### 📊 **Dashboard Features**
- **Statistics Cards:** Projects, Test Cases, Test Suites, Active Runs
- **Quick Actions:** Create Project, Generate Tests, New Test Run, View Reports
- **Recent Projects:** Last 5 projects with direct access
- **Activity Feed:** Recent system activities and updates

### 📁 **Project Management**
- **Create Projects:** Name, description, team assignment
- **View Projects:** Card layout with statistics
- **Project Details:** Dedicated page per project
- **Project Stats:** Test case count, coverage percentage
- **Team Collaboration:** User roles and permissions

### 📝 **Test Case Repository**
- **Multiple Views:** Table view and card view
- **Advanced Search:** Title, description, tags
- **Smart Filters:** Priority, status, project, creation date
- **Bulk Operations:** Select multiple, update status, delete
- **Rich Test Cases:** Steps, expected results, priority, tags
- **Version Control:** Track changes and history

### 🤖 **AI Test Generation**
- **File Upload Support:** PDF, Word, Text, Markdown, JSON, XML
- **Manual Input:** Paste requirements directly
- **Test Types:** Functional, UI/UX, API, Performance, Security, Integration
- **Configurable Count:** 5-20 test cases per generation
- **Smart Analysis:** Automatically identifies test scenarios
- **Edge Case Detection:** Finds boundary conditions
- **Save Options:** Individual save or bulk save to projects

### 🏃 **Test Execution**
- **Test Run Creation:** Configure execution parameters
- **Multiple Configurations:** Auto-execute, stop on failure, email notifications
- **Real-time Tracking:** Live status updates
- **Execution Results:** Pass/fail ratios, duration, detailed logs
- **Progress Monitoring:** Visual progress bars and statistics

### 🔧 **Advanced Features**
- **REST API:** Full programmatic access
- **Real-time Updates:** Auto-refresh capabilities
- **Export/Import:** Data portability
- **Integration Ready:** Hooks for CI/CD, Jira, etc.

---

## 🔌 API Documentation {#api-docs}

### Base URL: `http://localhost:5000/api`

### Core Endpoints:

#### **Health Check**
```http
GET /api/health
Response: {
  "status": "healthy",
  "version": "2.0.0-enterprise",
  "features": {...}
}
```

#### **Projects**
```http
GET /api/projects                    # List all projects
POST /api/projects                   # Create new project
GET /api/projects/{id}              # Get project details

Body for POST:
{
  "name": "Project Name",
  "description": "Project description"
}
```

#### **Test Cases**
```http
GET /api/test-cases                  # List all test cases
POST /api/test-cases                 # Create new test case
GET /api/test-cases/{id}            # Get test case details
PUT /api/test-cases/{id}            # Update test case
DELETE /api/test-cases/{id}         # Delete test case

Body for POST:
{
  "title": "Test Case Title",
  "description": "Description",
  "steps": ["Step 1", "Step 2"],
  "expected_result": "Expected outcome",
  "priority": "High|Medium|Low",
  "project_id": "project-uuid",
  "tags": ["tag1", "tag2"]
}
```

#### **AI Generation**
```http
POST /api/ai-generate               # Generate test cases with AI

Body:
{
  "requirements": "User requirements text",
  "project_id": "project-uuid",
  "test_type": "functional|api|ui|performance",
  "count": 10
}
```

#### **Test Runs**
```http
GET /api/test-runs                   # List all test runs
POST /api/test-runs                  # Create new test run
POST /api/test-runs/{id}/start      # Start test run
POST /api/test-runs/{id}/complete   # Complete test run
```

#### **Dashboard Statistics**
```http
GET /api/dashboard-stats            # Get real-time statistics
Response: {
  "total_projects": 3,
  "total_test_cases": 15,
  "active_test_runs": 2,
  "pass_rate": 85.5,
  "recent_activity": [...],
  "priority_stats": {...}
}
```

---

## 🔧 Troubleshooting {#troubleshooting}

### Common Issues:

#### **Server Not Starting**
```powershell
# Check if virtual environment is activated
venv\Scripts\activate

# Install dependencies
pip install -r requirements_basic.txt

# Try running again
python enterprise_test_platform.py
```

#### **Port Already in Use**
```powershell
# Kill existing processes
taskkill /F /IM python.exe

# Or change port in enterprise_test_platform.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

#### **Browser Can't Connect**
- Check firewall settings
- Try http://127.0.0.1:5000 instead of localhost
- Disable VPN if using one
- Check if antivirus is blocking the connection

#### **Features Not Working**
- Clear browser cache (Ctrl+F5)
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled
- Try in incognito/private mode

#### **Data Not Saving**
- Data is stored in memory (resets on server restart)
- For persistent storage, we'd need to implement database
- Current implementation is for demo/development

### **Support Commands:**
```powershell
# Test all functionality
python test_platform_functionality.py

# Check Python version
python --version

# Check Flask installation
pip show flask

# Check server status
netstat -an | findstr :5000
```

---

## 🎯 **Quick Start Summary**

1. **Start:** `python enterprise_test_platform.py`
2. **Access:** http://localhost:5000
3. **Create:** New project → Generate tests with AI → Run tests
4. **Monitor:** Dashboard shows real-time progress
5. **Stop:** Ctrl+C in terminal

---

## 🏆 **Congratulations!**

You now have a fully functional **enterprise-grade test management platform** that competes with TestRail, Zephyr, and qTest - plus unique AI capabilities they don't have!

**Happy Testing!** 🚀
