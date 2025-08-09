# TestGenie Enterprise

Enterprise-grade test case generation platform powered by AI.

## 🚀 **CURRENT SETUP - READY TO RUN!**

### **Quick Start (Your Current Setup)**

**Option 1: One-Click Startup (Recommended)**
```cmd
start_testgenie.bat
```
or
```powershell
.\start_testgenie.ps1
```

**Option 2: Manual Startup**
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run the application
python simple_app.py

# 3. Open browser: http://localhost:5000
```

### **Your Application URLs**
- 🏠 **Main App**: http://localhost:5000
- 💚 **Health Check**: http://localhost:5000/api/health
- 📊 **System Status**: http://localhost:5000/api/status
- 📤 **Upload API**: http://localhost:5000/api/upload
- 🤖 **Generate Tests**: http://localhost:5000/api/generate-test-cases

---

## 🚀 Quick Start

### Development Setup
```powershell
# 1. Clone and setup environment
git clone <repository>
cd testgenie-enterprise
cp .env.example .env

# 2. Edit .env with your configuration
# Add your Azure OpenAI credentials, database settings, etc.

# 3. Start with Docker Compose
docker-compose up -d

# 4. Access the application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# MinIO Console: http://localhost:9090
# Grafana: http://localhost:3000
```

### Manual Setup
```powershell
# 1. Install dependencies
pip install -r requirements/development.txt

# 2. Start services
docker-compose up -d postgres redis minio

# 3. Run application
python enterprise_main.py
```

## 📁 Project Structure

```
testgenie-enterprise/
├── app/                      # Application modules
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   ├── models/               # Data models
│   └── services/             # Business logic
├── docs/                     # Documentation
├── requirements/             # Python dependencies
├── uploads/                  # File uploads (development)
├── docker-compose.yml        # Development environment
├── Dockerfile               # Container definition
├── enterprise_main.py       # Application entry point
└── .env.example             # Environment template
```

## ✨ Features

### 🔐 Enterprise Security
- OAuth2/JWT authentication
- Role-based access control
- File encryption at rest
- Comprehensive audit logging
- API rate limiting

### 🤖 Advanced AI
- Multiple AI provider support (Azure OpenAI, OpenAI, Anthropic)
- Quality scoring for test cases
- Industry-specific prompts
- Automatic provider fallback

### 📊 Scalability
- Microservices architecture
- Database connection pooling
- Redis caching
- Kubernetes-ready
- Load balancing support

### 🔗 Enterprise Integration
- Test management tools (Jira, TestRail, Azure DevOps)
- CI/CD pipeline integration
- SSO/SAML authentication
- RESTful APIs

### 📈 Monitoring
- Prometheus metrics
- Grafana dashboards
- Health checks
- Performance monitoring
- Structured logging

## 🛠️ Configuration

Key environment variables in `.env`:

```bash
# Database
DB_HOST=localhost
DB_NAME=testgenie
DB_USER=postgres
DB_PASSWORD=your_password

# AI Providers
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment

# Security
SECRET_KEY=your_secret_key
MAX_FILE_SIZE_MB=50
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔍 Health Monitoring

- **Basic Health**: GET `/health`
- **Detailed Health**: GET `/health/detailed`
- **Metrics**: GET `/metrics`

## 📖 Documentation

See the `docs/` directory for detailed documentation:

- [Architecture Recommendations](docs/architecture_recommendations.md)
- [Security Guidelines](docs/security_recommendations.md)
- [Implementation Roadmap](docs/implementation_roadmap.md)
- [Migration Guide](MIGRATION_GUIDE.md)

## 🚢 Deployment

### Docker
```powershell
docker build -t testgenie-enterprise .
docker run -p 8000:8000 testgenie-enterprise
```

### Production
```powershell
# Use production compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```powershell
# Install test dependencies
pip install -r requirements/development.txt

# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

## 📞 Support

For enterprise support and customization:
- Documentation: See `docs/` folder
- Issues: Create GitHub issues
- Enterprise features: Contact sales team

## 📄 License

Enterprise License - Contact for licensing terms.
