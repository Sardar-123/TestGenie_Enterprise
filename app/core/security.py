"""
Enterprise Security Module
Includes authentication, authorization, encryption, and audit logging
"""
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import logging
from .config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
ALGORITHM = "HS256"

class SecurityManager:
    """Enterprise security manager"""
    
    def __init__(self):
        self.secret_key = settings.security.secret_key
        self.fernet = Fernet(self._get_or_create_encryption_key())
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for file encryption"""
        # In production, store this in secure key management service
        key = settings.security.secret_key.encode()
        return Fernet.generate_key()
    
    # Password management
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    # JWT token management
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.security.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.security.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTError as e:
            logger.warning(f"JWT error: {e}")
            return None
    
    # File encryption
    def encrypt_file_content(self, content: bytes) -> bytes:
        """Encrypt file content"""
        return self.fernet.encrypt(content)
    
    def decrypt_file_content(self, encrypted_content: bytes) -> bytes:
        """Decrypt file content"""
        return self.fernet.decrypt(encrypted_content)
    
    # File validation
    def validate_file_type(self, filename: str) -> bool:
        """Validate file type against allowed extensions"""
        if not filename:
            return False
        
        extension = filename.rsplit('.', 1)[-1].lower()
        return extension in settings.security.allowed_extensions
    
    def validate_file_size(self, file_size: int) -> bool:
        """Validate file size"""
        max_size_bytes = settings.security.max_file_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    
    def calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA256 hash of file content"""
        return hashlib.sha256(content).hexdigest()
    
    def is_safe_filename(self, filename: str) -> bool:
        """Check if filename is safe (no path traversal, etc.)"""
        dangerous_chars = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
        return not any(char in filename for char in dangerous_chars)

class RoleManager:
    """Role-based access control manager"""
    
    ROLES = {
        "admin": {
            "permissions": ["*"],  # All permissions
            "description": "System administrator"
        },
        "test_manager": {
            "permissions": [
                "project.create", "project.read", "project.update", "project.delete",
                "testcase.create", "testcase.read", "testcase.update", "testcase.delete",
                "file.upload", "file.read", "file.delete",
                "user.read", "user.update"
            ],
            "description": "Test manager with project oversight"
        },
        "tester": {
            "permissions": [
                "project.read", "testcase.create", "testcase.read", "testcase.update",
                "file.upload", "file.read"
            ],
            "description": "Test engineer"
        },
        "viewer": {
            "permissions": [
                "project.read", "testcase.read", "file.read"
            ],
            "description": "Read-only access"
        }
    }
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if role has specific permission"""
        if user_role not in self.ROLES:
            return False
        
        role_permissions = self.ROLES[user_role]["permissions"]
        
        # Admin has all permissions
        if "*" in role_permissions:
            return True
        
        return permission in role_permissions
    
    def get_role_permissions(self, role: str) -> List[str]:
        """Get all permissions for a role"""
        return self.ROLES.get(role, {}).get("permissions", [])

class AuditLogger:
    """Enterprise audit logging"""
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    def log_action(self, user_id: str, action: str, resource_type: str, 
                   resource_id: str, details: Dict[str, Any] = None,
                   ip_address: str = None, user_agent: str = None):
        """Log user action for audit purposes"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address,
            "user_agent": user_agent
        }
        
        self.logger.info(f"AUDIT: {audit_entry}")
    
    def log_security_event(self, event_type: str, user_id: str = None, 
                          details: Dict[str, Any] = None, 
                          ip_address: str = None):
        """Log security-related events"""
        security_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details or {},
            "ip_address": ip_address,
            "severity": "HIGH" if event_type in ["login_failed", "unauthorized_access"] else "INFO"
        }
        
        self.logger.warning(f"SECURITY: {security_entry}")

# Global instances
security_manager = SecurityManager()
role_manager = RoleManager()
audit_logger = AuditLogger()
