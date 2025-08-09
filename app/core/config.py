"""
Enterprise Configuration Management
Supports multiple environments with proper validation
"""
import os
from typing import Optional, List, Dict, Any
from pydantic import BaseSettings, Field, validator
from functools import lru_cache

class DatabaseSettings(BaseSettings):
    """Database configuration with connection pooling"""
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    database: str = Field(default="testgenie", env="DB_NAME")
    username: str = Field(default="postgres", env="DB_USER")
    password: str = Field(default="", env="DB_PASSWORD")
    pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")
    echo: bool = Field(default=False, env="DB_ECHO")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

class RedisSettings(BaseSettings):
    """Redis cache configuration"""
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    db: int = Field(default=0, env="REDIS_DB")
    ttl_seconds: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    max_connections: int = Field(default=10, env="REDIS_MAX_CONNECTIONS")

    @property
    def redis_url(self) -> str:
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"

class SecuritySettings(BaseSettings):
    """Security configuration"""
    secret_key: str = Field(env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    password_bcrypt_rounds: int = Field(default=12, env="PASSWORD_BCRYPT_ROUNDS")
    allowed_hosts: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    # File security
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    allowed_extensions: List[str] = Field(
        default=[
            "txt", "csv", "xlsx", "xls", "docx", "json", "pdf", 
            "xml", "md", "html", "zip", "png", "jpg", "jpeg", 
            "gif", "pptx", "vsdx", "msg", "eml", "py", "js", "java"
        ],
        env="ALLOWED_EXTENSIONS"
    )
    virus_scan_enabled: bool = Field(default=True, env="VIRUS_SCAN_ENABLED")
    encryption_at_rest: bool = Field(default=True, env="ENCRYPTION_AT_REST")

class AISettings(BaseSettings):
    """AI service configuration with multiple providers"""
    primary_provider: str = Field(default="azure", env="AI_PRIMARY_PROVIDER")
    
    # Azure OpenAI
    azure_endpoint: Optional[str] = Field(default=None, env="AZURE_OPENAI_ENDPOINT")
    azure_api_key: Optional[str] = Field(default=None, env="AZURE_OPENAI_API_KEY")
    azure_deployment: Optional[str] = Field(default=None, env="AZURE_OPENAI_DEPLOYMENT")
    azure_api_version: str = Field(default="2023-12-01-preview", env="AZURE_OPENAI_API_VERSION")
    
    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Anthropic Claude
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # General AI settings
    max_tokens: int = Field(default=4000, env="AI_MAX_TOKENS")
    temperature: float = Field(default=0.7, env="AI_TEMPERATURE")
    timeout_seconds: int = Field(default=60, env="AI_TIMEOUT_SECONDS")
    rate_limit_per_minute: int = Field(default=100, env="AI_RATE_LIMIT_PER_MINUTE")
    fallback_enabled: bool = Field(default=True, env="AI_FALLBACK_ENABLED")

class StorageSettings(BaseSettings):
    """File storage configuration (MinIO/S3)"""
    endpoint: str = Field(default="localhost:9000", env="STORAGE_ENDPOINT")
    access_key: str = Field(env="STORAGE_ACCESS_KEY")
    secret_key: str = Field(env="STORAGE_SECRET_KEY")
    bucket_name: str = Field(default="testgenie-files", env="STORAGE_BUCKET_NAME")
    secure: bool = Field(default=False, env="STORAGE_SECURE")
    region: str = Field(default="us-east-1", env="STORAGE_REGION")

class MonitoringSettings(BaseSettings):
    """Monitoring and observability configuration"""
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    enable_tracing: bool = Field(default=True, env="ENABLE_TRACING")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    jaeger_endpoint: Optional[str] = Field(default=None, env="JAEGER_ENDPOINT")

class Settings(BaseSettings):
    """Main application settings"""
    # Application
    app_name: str = Field(default="TestGenie Enterprise", env="APP_NAME")
    version: str = Field(default="2.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # Components
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    ai: AISettings = AISettings()
    storage: StorageSettings = StorageSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    @validator("environment")
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()
