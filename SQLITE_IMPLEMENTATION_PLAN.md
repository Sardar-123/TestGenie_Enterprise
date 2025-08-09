# TestGenie SQLite Migration Plan

## 🎯 SQLite Implementation Strategy

### **Phase 1: Database Setup (30 minutes)**
1. Install SQLAlchemy and SQLite support
2. Create database models
3. Database initialization script
4. Migration from in-memory to SQLite

### **Phase 2: GitHub/Azure DevOps Ready (15 minutes)**
1. Configure .gitignore for database files
2. Environment-specific database paths
3. CI/CD database setup

## 📋 Step-by-Step Implementation

### **1. Install Dependencies**
```bash
pip install sqlalchemy alembic
```

### **2. Database Configuration**
```python
# config.py
import os

class Config:
    # Development - local SQLite file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///testgenie.db'
    
    # Production - can use PostgreSQL/MySQL later
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@host/db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### **3. Database Models** (SQLAlchemy)
```python
# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_cases = db.relationship('TestCase', backref='project', lazy=True)
    test_suites = db.relationship('TestSuite', backref='project', lazy=True)

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.JSON)  # Store as JSON array
    expected_result = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Draft')
    tags = db.Column(db.JSON)  # Store as JSON array
    
    # Foreign Keys
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TestSuite(db.Model):
    __tablename__ = 'test_suites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    test_case_ids = db.Column(db.JSON)  # Array of test case IDs
    
    # Foreign Keys
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestRun(db.Model):
    __tablename__ = 'test_runs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Not Started')
    executed_by = db.Column(db.String(50))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    results = db.Column(db.JSON)  # test_case_id -> result mapping
    
    # Foreign Keys
    test_suite_id = db.Column(db.String(36), db.ForeignKey('test_suites.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### **4. GitHub/Azure DevOps Configuration**

#### **.gitignore Setup**
```gitignore
# Database files (choose one approach)

# Option A: Ignore database files (recommended for development)
*.db
*.sqlite
*.sqlite3
instance/

# Option B: Include sample database (for demo purposes)
# testgenie.db
# !sample_data.db
```

#### **Environment Configuration**
```bash
# .env (local development)
DATABASE_URL=sqlite:///testgenie_dev.db
FLASK_ENV=development

# .env.production (Azure/production)
DATABASE_URL=sqlite:///testgenie_prod.db
# Or PostgreSQL: postgresql://user:pass@host/testgenie
FLASK_ENV=production
```

## 🚀 Migration Benefits

### **For GitHub:**
- ✅ **Repository Size**: SQLite files are small (few MB)
- ✅ **Branching**: Each branch can have its own database
- ✅ **Collaboration**: Database schema versioned with code
- ✅ **CI/CD**: Automated testing with fresh databases

### **For Azure DevOps:**
- ✅ **Build Pipelines**: SQLite works in build agents
- ✅ **Release Pipelines**: Easy deployment to Azure App Service
- ✅ **Testing**: Isolated test databases per pipeline run
- ✅ **Scaling**: Can migrate to Azure SQL later without code changes

### **Development Workflow:**
```bash
# Local development
git clone <your-repo>
python -m venv venv
pip install -r requirements.txt
python init_db.py  # Create fresh database
python enterprise_test_platform.py

# Database changes
python migrate.py  # Update database schema
git add models.py
git commit -m "Add user authentication table"
```

## 🎯 Recommendation: **IMPLEMENT SQLITE NOW**

### **Why SQLite is Perfect for Your Journey:**

1. **Immediate Benefits**: 
   - Persistent data (no more data loss on restart)
   - Better performance than in-memory
   - Professional database features (transactions, relationships)

2. **GitHub/Azure Ready**:
   - Zero deployment complexity
   - No external dependencies
   - Works in any environment

3. **Future-Proof**:
   - SQLAlchemy abstracts database layer
   - Easy migration to PostgreSQL/MySQL later
   - Same code works with any SQL database

4. **Professional Grade**:
   - ACID compliance
   - Concurrent access support
   - Backup and recovery

### **Timeline Impact:**
- **SQLite Implementation**: 2-3 hours
- **GitHub Migration**: 30 minutes (unaffected)
- **Azure Deployment**: Still simple (possibly easier)

**Conclusion**: Implementing SQLite now will **enhance** your GitHub/Azure migration, not hinder it. You'll have a more professional, persistent, and scalable solution that deploys seamlessly to any platform.

Would you like me to help you implement the SQLite migration right now?
