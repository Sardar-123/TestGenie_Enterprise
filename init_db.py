"""
Database Initialization Script for TestGenie Enterprise
This script creates the database tables and populates with sample data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize database with tables and sample data"""
    
    # Import Flask and models
    from flask import Flask
    from models import db, Project, TestCase, TestSuite, TestRun, User
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testgenie.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        print("🗄️ Creating database tables...")
        
        # Drop all tables (for clean start)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # Add sample data
        print("📝 Adding sample data...")
        
        # Create sample users
        admin_user = User(
            username='admin',
            name='Admin User',
            email='admin@testgenie.com',
            role='admin'
        )
        
        tester_user = User(
            username='tester',
            name='Test Engineer',
            email='tester@testgenie.com',
            role='tester'
        )
        
        db.session.add(admin_user)
        db.session.add(tester_user)
        
        # Create sample projects
        web_project = Project(
            name='E-commerce Website Testing',
            description='Comprehensive testing for online shopping platform',
            created_by='admin'
        )
        
        mobile_project = Project(
            name='Mobile App Testing',
            description='iOS and Android mobile application testing',
            created_by='admin'
        )
        
        api_project = Project(
            name='REST API Testing',
            description='Backend API testing and validation',
            created_by='admin'
        )
        
        db.session.add(web_project)
        db.session.add(mobile_project)
        db.session.add(api_project)
        
        # Commit to get IDs
        db.session.commit()
        
        # Create sample test cases for web project
        login_test = TestCase(
            title='User Login Functionality',
            description='Test user authentication with valid and invalid credentials',
            project_id=web_project.id,
            priority='High',
            status='Approved'
        )
        login_test.set_steps([
            'Navigate to login page',
            'Enter valid email and password',
            'Click login button',
            'Verify successful login and redirect to dashboard'
        ])
        login_test.set_tags(['authentication', 'functional', 'high-priority'])
        login_test.expected_result = 'User should be logged in successfully and redirected to dashboard'
        
        checkout_test = TestCase(
            title='Shopping Cart Checkout Process',
            description='Test the complete checkout flow from cart to payment',
            project_id=web_project.id,
            priority='High',
            status='Draft'
        )
        checkout_test.set_steps([
            'Add items to shopping cart',
            'Navigate to checkout page',
            'Enter shipping information',
            'Select payment method',
            'Complete payment process',
            'Verify order confirmation'
        ])
        checkout_test.set_tags(['checkout', 'e-commerce', 'payment'])
        checkout_test.expected_result = 'Order should be processed successfully with confirmation email sent'
        
        search_test = TestCase(
            title='Product Search Functionality',
            description='Test product search with various filters and sorting options',
            project_id=web_project.id,
            priority='Medium',
            status='Under Review'
        )
        search_test.set_steps([
            'Enter search term in search box',
            'Apply category filters',
            'Sort by price/rating',
            'Verify search results accuracy'
        ])
        search_test.set_tags(['search', 'filtering', 'ui'])
        search_test.expected_result = 'Relevant products should be displayed with correct filtering and sorting'
        
        # API test cases
        api_auth_test = TestCase(
            title='API Authentication Endpoint',
            description='Test REST API authentication endpoints',
            project_id=api_project.id,
            priority='High',
            status='Approved'
        )
        api_auth_test.set_steps([
            'Send POST request to /api/auth/login',
            'Include valid credentials in request body',
            'Verify 200 status code',
            'Verify JWT token in response',
            'Test token validation on protected endpoints'
        ])
        api_auth_test.set_tags(['api', 'authentication', 'jwt'])
        api_auth_test.expected_result = 'API should return valid JWT token for authenticated users'
        
        api_users_test = TestCase(
            title='User Management API CRUD',
            description='Test user creation, reading, updating, and deletion via API',
            project_id=api_project.id,
            priority='Medium',
            status='Draft'
        )
        api_users_test.set_steps([
            'POST /api/users - Create new user',
            'GET /api/users/{id} - Retrieve user details',
            'PUT /api/users/{id} - Update user information',
            'DELETE /api/users/{id} - Delete user',
            'Verify proper error handling for invalid requests'
        ])
        api_users_test.set_tags(['api', 'crud', 'users'])
        api_users_test.expected_result = 'All CRUD operations should work correctly with proper status codes'
        
        # Mobile test cases
        mobile_login_test = TestCase(
            title='Mobile App Login Flow',
            description='Test login functionality on mobile devices',
            project_id=mobile_project.id,
            priority='High',
            status='Approved'
        )
        mobile_login_test.set_steps([
            'Launch mobile application',
            'Tap on login button',
            'Enter credentials using mobile keyboard',
            'Test biometric authentication if available',
            'Verify successful login'
        ])
        mobile_login_test.set_tags(['mobile', 'authentication', 'biometric'])
        mobile_login_test.expected_result = 'User should be able to login using password or biometric authentication'
        
        # Add all test cases
        test_cases = [login_test, checkout_test, search_test, api_auth_test, api_users_test, mobile_login_test]
        for tc in test_cases:
            db.session.add(tc)
        
        # Create sample test suite
        regression_suite = TestSuite(
            name='Regression Test Suite',
            description='Core functionality regression tests',
            project_id=web_project.id,
            created_by='admin'
        )
        regression_suite.set_test_case_ids([login_test.id, checkout_test.id, search_test.id])
        
        api_suite = TestSuite(
            name='API Test Suite',
            description='Complete API testing suite',
            project_id=api_project.id,
            created_by='tester'
        )
        api_suite.set_test_case_ids([api_auth_test.id, api_users_test.id])
        
        db.session.add(regression_suite)
        db.session.add(api_suite)
        
        # Commit test suites to get IDs
        db.session.commit()
        
        # Create sample test run
        sample_run = TestRun(
            name='Sprint 15 Regression Testing',
            test_suite_id=regression_suite.id,
            status='In Progress',
            executed_by='tester',
            started_at=datetime.utcnow()
        )
        sample_run.set_results({
            login_test.id: 'Passed',
            search_test.id: 'Passed'
            # checkout_test still running
        })
        
        db.session.add(sample_run)
        
        # Final commit
        db.session.commit()
        
        print("✅ Sample data added successfully!")
        print("\n📊 Database Summary:")
        print(f"   - Projects: {Project.query.count()}")
        print(f"   - Test Cases: {TestCase.query.count()}")
        print(f"   - Test Suites: {TestSuite.query.count()}")
        print(f"   - Test Runs: {TestRun.query.count()}")
        print(f"   - Users: {User.query.count()}")
        print(f"\n🗄️ Database file: testgenie.db")
        print("🚀 TestGenie database is ready!")

if __name__ == '__main__':
    init_database()
