# Enterprise TestGenie Architecture

## Project Structure
```
testgenie-enterprise/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   ├── files/
│   │   ├── projects/
│   │   ├── test_cases/
│   │   └── users/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── cache.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── file.py
│   │   └── test_case.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── file_service.py
│   │   ├── auth_service.py
│   │   └── test_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── constants.py
│   └── web/
│       ├── __init__.py
│       ├── static/
│       └── templates/
├── migrations/
├── tests/
├── docker/
├── kubernetes/
├── docs/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── alembic.ini
└── main.py
```

## Technology Stack
- **Backend**: FastAPI (replacing Flask for better performance and async support)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Message Queue**: Celery with Redis broker
- **Authentication**: OAuth2 with JWT tokens
- **File Storage**: MinIO (S3-compatible)
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with ELK stack
- **Container**: Docker + Kubernetes
- **Frontend**: React.js (separate SPA)
