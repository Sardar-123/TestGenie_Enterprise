# Multi-stage Docker build for enterprise deployment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd --create-home --shell /bin/bash appuser

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements/ ./requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/production.txt

# Development stage
FROM base as development
RUN pip install --no-cache-dir -r requirements/development.txt
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
CMD ["uvicorn", "enterprise_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "enterprise_main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
