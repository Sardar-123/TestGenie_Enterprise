# TestGenie Enterprise - Scripts & Files Reference

## 📁 Complete File Structure & Script Purposes

### **🚀 Core Application Files**

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `enterprise_test_platform.py` | **Main Flask application** - All routes, APIs, business logic | 644 | ✅ Active |
| `ai_service.py` | **AI integration module** - Azure OpenAI, multi-provider support | 351 | ✅ Active |
| `requirements.txt` | **Python dependencies** - Flask, OpenAI, etc. | - | ✅ Active |
| `.env` | **Environment variables** - Azure OpenAI credentials | - | ✅ Active |

### **🎬 Startup & Launch Scripts**

| Script | Purpose | Platform | Usage |
|--------|---------|----------|-------|
| `start_server.bat` | **Main server launcher** - Activates venv, starts Flask | Windows | `start_server.bat` |
| `start_testgenie.bat` | Alternative launcher script | Windows | `start_testgenie.bat` |
| `start_testgenie.ps1` | PowerShell launcher script | Windows | `.\start_testgenie.ps1` |

### **🧪 Testing & Debugging Scripts**

| Script | Purpose | What It Tests | Usage |
|--------|---------|---------------|-------|
| `test_platform_functionality.py` | **Complete API testing** - All endpoints, CRUD operations | All REST APIs | `python test_platform_functionality.py` |
| `test_azure_openai.py` | **AI integration testing** - Azure OpenAI connectivity | AI service only | `python test_azure_openai.py` |
| `ai_status_check.py` | **Quick AI provider check** - Fast AI status verification | AI providers | `python ai_status_check.py` |
| `debug_ai_generator.py` | **AI Generator debugging** - Frontend/backend integration | AI Generator page | `python debug_ai_generator.py` |
| `test_projects_issue.py` | **Project loading issues** - Diagnose project dropdown problems | Projects API | `python test_projects_issue.py` |
| `test_all_functionality.py` | Legacy comprehensive testing | All features | `python test_all_functionality.py` |

### **📚 Documentation Files**

| Document | Content | Purpose |
|----------|---------|---------|
| `BACKEND_ARCHITECTURE.md` | **Complete backend analysis** - Architecture, data flow, API routes | Technical documentation |
| `API_REFERENCE.md` | **Complete API documentation** - All 19 endpoints with examples | API integration guide |
| `PLATFORM_CAPABILITIES.md` | **Feature overview** - What TestGenie can do | Business overview |
| `TEST_CASE_TYPES.md` | **Test types supported** - Functional, API, UI, Security, etc. | Testing methodology |
| `USER_GUIDE.md` | **End-user documentation** - How to use the platform | User manual |
| `README.md` | **Project overview** - Getting started, setup instructions | Project introduction |

### **⚙️ Configuration Files**

| File | Purpose | Format |
|------|---------|--------|
| `.env` | **Environment variables** - API keys, endpoints | KEY=value |
| `.env.example` | **Environment template** - Example configuration | KEY=value |
| `requirements.txt` | **Python dependencies** - Package versions | package==version |
| `Dockerfile` | **Docker containerization** - Container setup | Docker commands |
| `docker-compose.yml` | **Multi-container setup** - Service orchestration | YAML |

### **🎨 Frontend Templates**

| Template | Purpose | Features |
|----------|---------|----------|
| `templates/base.html` | **Base layout** - Bootstrap 5, navigation, common styles | Responsive design |
| `templates/dashboard.html` | **Main dashboard** - Statistics, recent activity | Analytics view |
| `templates/projects.html` | **Project management** - CRUD operations, project list | Project management |
| `templates/project_detail.html` | **Project details** - Test cases, suites, runs | Detailed project view |
| `templates/test_cases.html` | **Test case management** - Create, edit, filter test cases | Test case CRUD |
| `templates/test_case_detail.html` | **Test case details** - Steps, results, execution history | Detailed test view |
| `templates/test_runs.html` | **Test execution** - Run tests, view results | Execution management |
| `templates/ai_generator.html` | **AI test generation** - Upload files, generate tests | AI integration UI |
| `templates/settings.html` | **Platform settings** - Configuration, preferences | System settings |

### **🗂️ Directory Structure**

```
MVP/
├── 📁 venv/                    # Virtual environment (Python packages)
├── 📁 templates/               # Jinja2 HTML templates (9 files)
├── 📁 uploads/                 # File upload storage
├── 📁 data/                    # Data storage directory
├── 📁 docs/                    # Additional documentation
├── 📁 requirements/            # Dependency management
├── 📁 __pycache__/            # Python bytecode cache
├── 📁 .vscode/                # VS Code settings
└── 📁 app/                    # Legacy app structure
```

## 🔄 Script Execution Flow

### **1. Development Workflow**
```bash
# 1. Start the platform
start_server.bat

# 2. Test API functionality
python test_platform_functionality.py

# 3. Test AI integration
python test_azure_openai.py

# 4. Debug specific issues
python debug_ai_generator.py
```

### **2. Testing Workflow**
```bash
# Quick health check
python ai_status_check.py

# Comprehensive API testing
python test_platform_functionality.py

# Project-specific issues
python test_projects_issue.py

# AI generator debugging
python debug_ai_generator.py
```

## 🛠️ Script Breakdown by Category

### **🎯 Primary Scripts (Must Have)**
1. **`enterprise_test_platform.py`** - Core application (644 lines)
2. **`ai_service.py`** - AI integration (351 lines)
3. **`start_server.bat`** - Server launcher
4. **`test_platform_functionality.py`** - API testing

### **🔧 Utility Scripts (Helper Tools)**
1. **`ai_status_check.py`** - Quick AI diagnostics
2. **`debug_ai_generator.py`** - Frontend debugging
3. **`test_projects_issue.py`** - Project-specific debugging

### **📖 Legacy/Backup Scripts**
1. **`test_all_functionality.py`** - Older comprehensive test
2. **`test_functionality.py`** - Basic functionality test
3. **`simple_app.py`** - Minimal Flask app
4. **`app.py`** - Original MVP application

## 🎪 Database & Storage

### **Current Storage (In-Memory)**
```python
# Located in enterprise_test_platform.py
projects = {}       # Dictionary acting as Projects table
test_cases = {}     # Dictionary acting as TestCases table
test_suites = {}    # Dictionary acting as TestSuites table
test_runs = {}      # Dictionary acting as TestRuns table
users = {...}       # Pre-defined user accounts
```

### **Data Persistence**
- **Current**: In-memory dictionaries (data lost on restart)
- **Files**: Uploaded files stored in `uploads/` directory
- **Configuration**: Environment variables in `.env` file
- **Future**: SQLAlchemy + PostgreSQL/MySQL migration planned

### **Data Flow**
```
User Input → Flask Routes → Business Logic → In-Memory Storage → JSON Response
```

## 🚀 Quick Start Commands

### **Essential Commands**
```bash
# Start the platform
start_server.bat

# Open in browser
http://localhost:5000

# Test all APIs
python test_platform_functionality.py

# Check AI status
python ai_status_check.py
```

### **Troubleshooting Commands**
```bash
# Debug AI generator issues
python debug_ai_generator.py

# Test specific project loading
python test_projects_issue.py

# Full Azure OpenAI test
python test_azure_openai.py
```

## 📊 File Statistics

| Category | Files | Total Lines | Purpose |
|----------|-------|-------------|---------|
| **Core Application** | 2 | ~1000 | Main business logic |
| **Testing Scripts** | 6 | ~800 | Quality assurance |
| **Documentation** | 8 | ~2000 | Technical documentation |
| **Templates** | 9 | ~3000 | User interface |
| **Configuration** | 5 | ~100 | Environment setup |
| **Total** | **30+** | **~6900** | **Complete platform** |

This comprehensive overview shows that TestGenie Enterprise is a well-structured, thoroughly tested platform with extensive documentation and multiple testing utilities to ensure reliability and maintainability!
