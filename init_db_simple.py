"""
Simple Database Initialization Script for TestGenie Enterprise
Creates database with only the fields that exist in the models
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
    
    # Configure database with absolute path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'testgenie.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"🗄️ Database path: {db_path}")
    
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
            name='E-commerce Website',
            description='Online shopping platform with user authentication, product catalog, and checkout',
            created_by='admin'
        )
        
        api_project = Project(
            name='Payment API',
            description='RESTful API for processing payments and managing transactions',
            created_by='admin'
        )
        
        mobile_project = Project(
            name='Mobile App',
            description='iOS and Android app for customer engagement',
            created_by='tester'
        )
        
        db.session.add(web_project)
        db.session.add(api_project)
        db.session.add(mobile_project)
        db.session.commit()  # Commit to get IDs
        
        # Create sample test cases
        login_test = TestCase(
            title='User Login Functionality',
            description='Test user authentication with valid credentials',
            project_id=web_project.id,
            created_by='tester',
            priority='High',
            status='Active',
            expected_result='User should be redirected to dashboard'
        )
        login_test.set_steps([
            'Navigate to login page',
            'Enter valid username and password',
            'Click login button'
        ])
        
        search_test = TestCase(
            title='Product Search',
            description='Test product search functionality',
            project_id=web_project.id,
            created_by='tester',
            priority='Medium',
            status='Active',
            expected_result='Relevant products should be displayed'
        )
        search_test.set_steps([
            'Navigate to homepage',
            'Enter product name in search box',
            'Click search button'
        ])
        
        checkout_test = TestCase(
            title='Checkout Process',
            description='Test end-to-end checkout functionality',
            project_id=web_project.id,
            created_by='admin',
            priority='High',
            status='Active',
            expected_result='Order should be placed successfully'
        )
        checkout_test.set_steps([
            'Add items to cart',
            'Proceed to checkout',
            'Enter shipping information',
            'Select payment method',
            'Complete order'
        ])
        
        api_auth_test = TestCase(
            title='API Authentication',
            description='Test API token authentication',
            project_id=api_project.id,
            created_by='admin',
            priority='High',
            status='Active',
            expected_result='API should return 200 status with valid data'
        )
        api_auth_test.set_steps([
            'Send request with valid API token',
            'Verify response status',
            'Check response data'
        ])
        
        mobile_login_test = TestCase(
            title='Mobile App Login',
            description='Test mobile app authentication',
            project_id=mobile_project.id,
            created_by='tester',
            priority='High',
            status='Draft',
            expected_result='User should be authenticated'
        )
        mobile_login_test.set_steps([
            'Open mobile app',
            'Enter credentials',
            'Tap login button'
        ])
        
        db.session.add(login_test)
        db.session.add(search_test)
        db.session.add(checkout_test)
        db.session.add(api_auth_test)
        db.session.add(mobile_login_test)
        db.session.commit()  # Commit to get IDs
        
        # Create sample test suites
        smoke_suite = TestSuite(
            name='Smoke Test Suite',
            description='Basic functionality tests for quick validation',
            project_id=web_project.id,
            created_by='admin'
        )
        smoke_suite.set_test_case_ids([login_test.id, search_test.id])
        
        regression_suite = TestSuite(
            name='Regression Test Suite',
            description='Comprehensive tests for regression testing',
            project_id=web_project.id,
            created_by='tester'
        )
        regression_suite.set_test_case_ids([login_test.id, search_test.id, checkout_test.id])
        
        db.session.add(smoke_suite)
        db.session.add(regression_suite)
        db.session.commit()  # Commit to get IDs
        
        # Create sample test run
        sample_run = TestRun(
            name='Sprint 15 Regression Testing',
            test_suite_id=regression_suite.id,
            status='In Progress',
            executed_by='tester',
            started_at=datetime.now()  # Fixed deprecation warning
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
        print(f"\n🗄️ Database file: {db_path}")
        print(f"📏 Database size: {os.path.getsize(db_path)} bytes")
        print("🚀 TestGenie database is ready!")

if __name__ == '__main__':
    init_database()
