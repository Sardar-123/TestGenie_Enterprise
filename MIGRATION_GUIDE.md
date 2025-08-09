# TestGenie MVP to Enterprise Migration Guide

## Overview
This guide walks you through migrating your TestGenie MVP to the enterprise architecture.

## Pre-Migration Checklist

### 1. Environment Setup
```powershell
# Create virtual environment
python -m venv venv-enterprise
venv-enterprise\Scripts\activate

# Install enterprise dependencies
pip install -r requirements/development.txt
```

### 2. Database Setup
```powershell
# Install PostgreSQL (if not already installed)
# Download from: https://www.postgresql.org/download/windows/

# Create database
createdb testgenie

# Set up environment variables
copy .env.example .env
# Edit .env with your configuration
```

### 3. Infrastructure Services
```powershell
# Start services with Docker Compose
docker-compose up -d postgres redis minio

# Verify services are running
docker-compose ps
```

## Migration Steps

### Step 1: Data Migration
```powershell
# Backup existing MVP data (if any)
python backup_mvp_data.py

# Initialize new database schema
alembic upgrade head

# Migrate existing data (if any)
python migrate_data.py
```

### Step 2: Configuration Migration
1. Copy your Azure OpenAI credentials from old app to `.env`
2. Update file upload paths to use MinIO
3. Configure Redis for caching
4. Set up monitoring endpoints

### Step 3: Application Deployment

#### Development Deployment
```powershell
# Run locally for testing
python enterprise_main.py

# Or with uvicorn
uvicorn enterprise_main:app --reload
```

#### Docker Deployment
```powershell
# Build and run with Docker
docker-compose up --build

# Access application at http://localhost:8000
# Access MinIO console at http://localhost:9090
# Access Grafana at http://localhost:3000
```

#### Production Deployment
```powershell
# Build production image
docker build --target production -t testgenie-enterprise:latest .

# Deploy with docker-compose (production profile)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Features Comparison

### MVP Features ✅
- File upload and preview
- Basic AI test case generation
- Simple web interface
- Single file processing

### Enterprise Features 🚀

#### Security & Compliance
- ✅ Multi-factor authentication
- ✅ Role-based access control
- ✅ File encryption at rest
- ✅ Comprehensive audit logging
- ✅ API rate limiting

#### Scalability & Performance
- ✅ Microservices architecture
- ✅ Database connection pooling
- ✅ Redis caching
- ✅ Horizontal scaling with Kubernetes
- ✅ Load balancing

#### Advanced AI Features
- ✅ Multiple AI provider support
- ✅ Quality scoring for test cases
- ✅ Industry-specific prompts
- ✅ Test case optimization
- ✅ Custom prompt templates

#### Enterprise Integration
- ✅ Test management tool connectors
- ✅ CI/CD pipeline integration
- ✅ SSO/SAML authentication
- ✅ API marketplace ready

#### Monitoring & Observability
- ✅ Prometheus metrics
- ✅ Grafana dashboards
- ✅ Structured logging
- ✅ Health checks
- ✅ Performance monitoring

#### Multi-tenancy
- ✅ Organization management
- ✅ User workspace isolation
- ✅ Resource quotas
- ✅ Subscription management

## Testing the Migration

### 1. Functionality Tests
```powershell
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run end-to-end tests
pytest tests/e2e/
```

### 2. Performance Tests
```powershell
# Load testing with locust
locust -f tests/performance/locustfile.py

# Database performance
python tests/performance/db_performance.py
```

### 3. Security Tests
```powershell
# Security scan
bandit -r app/

# Dependency vulnerability check
safety check
```

## Post-Migration Verification

### 1. Core Functionality
- [ ] User registration and authentication
- [ ] File upload and processing
- [ ] AI test case generation
- [ ] Test case management
- [ ] Project organization

### 2. Performance
- [ ] Page load times < 2 seconds
- [ ] API response times < 500ms
- [ ] File upload handling for 50MB files
- [ ] Concurrent user support (100+ users)

### 3. Security
- [ ] Authentication required for all endpoints
- [ ] File type validation working
- [ ] Rate limiting active
- [ ] Audit logs being generated

### 4. Monitoring
- [ ] Health check endpoints responding
- [ ] Metrics being collected
- [ ] Logs being generated
- [ ] Alerts configured

## Rollback Plan

If issues occur during migration:

1. **Stop enterprise services**:
   ```powershell
   docker-compose down
   ```

2. **Restore MVP**:
   ```powershell
   # Restore backup
   python restore_mvp.py
   
   # Start MVP version
   python app.py
   ```

3. **Data recovery**:
   ```powershell
   # Restore database from backup
   pg_restore -d testgenie backup.sql
   ```

## Support and Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify credentials in .env
   - Check firewall settings

2. **AI Provider Errors**
   - Verify API keys in .env
   - Check rate limits
   - Test with different providers

3. **File Upload Issues**
   - Check MinIO is running
   - Verify storage credentials
   - Check file size limits

### Getting Help

- Check logs: `docker-compose logs testgenie-app`
- Review health checks: `curl http://localhost:8000/health/detailed`
- Monitor metrics: Access Grafana at `http://localhost:3000`

## Next Steps

After successful migration:

1. **User Training**: Train team on new features
2. **Integration Setup**: Connect with existing tools
3. **Monitoring Setup**: Configure alerts and dashboards
4. **Backup Strategy**: Implement regular backups
5. **Scaling Plan**: Plan for growth and additional features

## Production Deployment Checklist

- [ ] SSL/TLS certificates configured
- [ ] Environment variables secured
- [ ] Database backups scheduled
- [ ] Monitoring alerts configured
- [ ] Load balancer configured
- [ ] CDN setup for static assets
- [ ] Log aggregation configured
- [ ] Security scanning automated
- [ ] Disaster recovery plan documented
- [ ] Performance baselines established
