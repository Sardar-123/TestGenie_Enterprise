"""
Database Models for TestGenie Enterprise
SQLAlchemy models to replace in-memory storage
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import json

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_cases = db.relationship('TestCase', backref='project', lazy=True, cascade='all, delete-orphan')
    test_suites = db.relationship('TestSuite', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'test_cases_count': len(self.test_cases),
            'test_suites_count': len(self.test_suites)
        }

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text)  # JSON string for steps array
    expected_result = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Draft')
    tags = db.Column(db.Text)  # JSON string for tags array
    
    # Foreign Keys
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_steps(self):
        """Get steps as a list"""
        if self.steps:
            try:
                return json.loads(self.steps)
            except json.JSONDecodeError:
                return [self.steps]  # Fallback for plain text
        return []
    
    def set_steps(self, steps_list):
        """Set steps from a list"""
        if isinstance(steps_list, list):
            self.steps = json.dumps(steps_list)
        else:
            self.steps = str(steps_list)
    
    def get_tags(self):
        """Get tags as a list"""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return [self.tags]  # Fallback for plain text
        return []
    
    def set_tags(self, tags_list):
        """Set tags from a list"""
        if isinstance(tags_list, list):
            self.tags = json.dumps(tags_list)
        else:
            self.tags = str(tags_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'steps': self.get_steps(),
            'expected_result': self.expected_result,
            'priority': self.priority,
            'status': self.status,
            'project_id': self.project_id,
            'tags': self.get_tags(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TestSuite(db.Model):
    __tablename__ = 'test_suites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    test_case_ids = db.Column(db.Text)  # JSON string for test case IDs array
    
    # Foreign Keys
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'), nullable=False)
    
    created_by = db.Column(db.String(50), default='system')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_runs = db.relationship('TestRun', backref='test_suite', lazy=True, cascade='all, delete-orphan')
    
    def get_test_case_ids(self):
        """Get test case IDs as a list"""
        if self.test_case_ids:
            try:
                return json.loads(self.test_case_ids)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_test_case_ids(self, ids_list):
        """Set test case IDs from a list"""
        if isinstance(ids_list, list):
            self.test_case_ids = json.dumps(ids_list)
        else:
            self.test_case_ids = '[]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'test_cases': self.get_test_case_ids(),
            'project_id': self.project_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'test_runs_count': len(self.test_runs)
        }

class TestRun(db.Model):
    __tablename__ = 'test_runs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Not Started')
    executed_by = db.Column(db.String(50))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    results = db.Column(db.Text)  # JSON string for test_case_id -> result mapping
    
    # Foreign Keys
    test_suite_id = db.Column(db.String(36), db.ForeignKey('test_suites.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_results(self):
        """Get results as a dictionary"""
        if self.results:
            try:
                return json.loads(self.results)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_results(self, results_dict):
        """Set results from a dictionary"""
        if isinstance(results_dict, dict):
            self.results = json.dumps(results_dict)
        else:
            self.results = '{}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'test_suite_id': self.test_suite_id,
            'status': self.status,
            'executed_by': self.executed_by,
            'started_at': self.started_at.isoformat() if self.started_at else '',
            'completed_at': self.completed_at.isoformat() if self.completed_at else '',
            'results': self.get_results(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# User model for future authentication
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='tester')  # admin, tester, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
