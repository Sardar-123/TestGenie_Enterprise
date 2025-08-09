"""
TestGenie Enterprise - Full Test Management Platform
Enhanced version with test management capabilities 
Now with Real AI Integration (Azure OpenAI) and SQLite Database
"""
from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
import os
import json
import time
from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database models and AI service
from models import db, Project, TestCase, TestSuite, TestRun, User
from ai_service import ai_service

app = Flask(__name__)
app.secret_key = 'testgenie-enterprise-secret'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///testgenie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@dataclass
class TestCase:
    id: str
    title: str
    description: str
    steps: List[str]
    expected_result: str
    priority: str = "Medium"
    status: str = "Draft"
    project_id: str = ""
    created_by: str = "system"
    created_at: str = ""
    tags: List[str] = None

@dataclass
class TestSuite:
    id: str
    name: str
    description: str
    test_cases: List[str]
    project_id: str
    created_by: str = "system"
    created_at: str = ""

@dataclass
class TestRun:
    id: str
    name: str
    test_suite_id: str
    status: str = "Not Started"
    executed_by: str = ""
    started_at: str = ""
    completed_at: str = ""
    results: Dict[str, str] = None  # test_case_id -> result

@dataclass
class Project:
    id: str
    name: str
    description: str
    created_by: str = "system"
    created_at: str = ""

# Routes
@app.route('/')
def dashboard():
    """Main dashboard like TestRail/Zephyr"""
    stats = {
        'total_projects': len(projects),
        'total_test_cases': len(test_cases),
        'total_test_suites': len(test_suites),
        'active_test_runs': len([tr for tr in test_runs.values() if tr.status == "In Progress"])
    }
    return render_template('dashboard.html', stats=stats, projects=list(projects.values())[:5])

@app.route('/projects')
def projects_list():
    """Project management"""
    return render_template('projects.html', projects=list(projects.values()))

@app.route('/projects/<project_id>')
def project_detail(project_id):
    """Project detail with test cases and suites"""
    project = projects.get(project_id)
    if not project:
        return "Project not found", 404
    
    project_test_cases = [tc for tc in test_cases.values() if tc.project_id == project_id]
    project_test_suites = [ts for ts in test_suites.values() if ts.project_id == project_id]
    
    return render_template('project_detail.html', 
                         project=project, 
                         test_cases=project_test_cases,
                         test_suites=project_test_suites)

@app.route('/test-cases')
def test_cases_list():
    """Test case repository"""
    return render_template('test_cases.html', test_cases=list(test_cases.values()))

@app.route('/test-case/<test_case_id>')
def test_case_detail(test_case_id):
    """Individual test case view"""
    test_case = test_cases.get(test_case_id)
    if not test_case:
        return "Test case not found", 404
    return render_template('test_case_detail.html', test_case=test_case)

@app.route('/test-runs')
def test_runs_list():
    """Test execution management"""
    return render_template('test_runs.html', test_runs=list(test_runs.values()))

@app.route('/ai-generator')
def ai_generator():
    """AI test generation interface"""
    return render_template('ai_generator.html')

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    # Calculate some basic stats for reports
    stats = {
        'total_projects': len(projects),
        'total_test_cases': len(test_cases),
        'total_test_suites': len(test_suites),
        'total_test_runs': len(test_runs),
        'passed_tests': 0,
        'failed_tests': 0,
        'test_coverage': 0,
        'active_projects': len([p for p in projects.values()]),
        'recent_activities': []
    }
    
    # Calculate pass/fail stats from test runs
    for test_run in test_runs.values():
        if test_run.results:
            for result in test_run.results.values():
                if result == 'pass':
                    stats['passed_tests'] += 1
                elif result == 'fail':
                    stats['failed_tests'] += 1
    
    return render_template('reports.html', stats=stats)

# API Endpoints
@app.route('/api/health')
def health_check():
    """API Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0-enterprise',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'message': 'TestGenie Enterprise Test Management Platform',
        'features': {
            'test_management': True,
            'ai_generation': True,
            'project_management': True,
            'test_execution': True,
            'reporting': True
        }
    })

@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    """Project management API"""
    if request.method == 'GET':
        project_list = []
        for project in projects.values():
            project_dict = asdict(project)
            # Add additional stats
            project_test_cases = [tc for tc in test_cases.values() if tc.project_id == project.id]
            project_test_suites = [ts for ts in test_suites.values() if ts.project_id == project.id]
            project_dict['stats'] = {
                'test_cases': len(project_test_cases),
                'test_suites': len(project_test_suites),
                'coverage': 0  # Calculate coverage if needed
            }
            project_list.append(project_dict)
        return jsonify(project_list)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('name', '').strip():
                return jsonify({'error': 'Project name is required'}), 400
                
            project_name = data.get('name', '').strip()
            
            # Check for duplicate names
            for existing_project in projects.values():
                if existing_project.name.lower() == project_name.lower():
                    return jsonify({'error': 'Project name already exists'}), 400
            
            project_id = str(uuid.uuid4())
            project = Project(
                id=project_id,
                name=project_name,
                description=data.get('description', '').strip(),
                created_by=data.get('created_by', 'Admin User'),
                created_at=datetime.now(timezone.utc).isoformat()
            )
            projects[project_id] = project
            
            # Return project with stats
            project_dict = asdict(project)
            project_dict['stats'] = {
                'test_cases': 0,
                'test_suites': 0,
                'coverage': 0
            }
            
            return jsonify(project_dict), 201
            
        except Exception as e:
            return jsonify({'error': f'Error creating project: {str(e)}'}), 500

@app.route('/api/test-cases', methods=['GET', 'POST'])
def api_test_cases():
    """Test case management API"""
    if request.method == 'GET':
        project_id = request.args.get('project_id')
        if project_id:
            filtered_cases = [tc for tc in test_cases.values() if tc.project_id == project_id]
            return jsonify([asdict(tc) for tc in filtered_cases])
        return jsonify([asdict(tc) for tc in test_cases.values()])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('title', '').strip():
                return jsonify({'error': 'Test case title is required'}), 400
            
            # Handle both AI-generated and manual test cases
            test_case_id = data.get('id') or str(uuid.uuid4())
            steps = data.get('steps', [])
            
            # If steps is a string, convert to list
            if isinstance(steps, str):
                steps = [step.strip() for step in steps.split('\n') if step.strip()]
            
            test_case = TestCase(
                id=test_case_id,
                title=data.get('title', '').strip(),
                description=data.get('description', '').strip(),
                steps=steps,
                expected_result=data.get('expected_result', '').strip(),
                priority=data.get('priority', 'Medium'),
                status=data.get('status', 'Draft'),
                project_id=data.get('project_id', ''),
                created_by=data.get('created_by', 'Admin User'),
                created_at=data.get('created_at') or datetime.utcnow().isoformat(),
                tags=data.get('tags', [])
            )
            test_cases[test_case_id] = test_case
            return jsonify(asdict(test_case)), 201
            
        except Exception as e:
            return jsonify({'error': f'Error creating test case: {str(e)}'}), 500

@app.route('/api/test-cases/<test_case_id>', methods=['GET', 'PUT', 'DELETE'])
def api_test_case_detail(test_case_id):
    """Individual test case operations"""
    if test_case_id not in test_cases:
        return jsonify({'error': 'Test case not found'}), 404
    
    if request.method == 'GET':
        return jsonify(asdict(test_cases[test_case_id]))
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            test_case = test_cases[test_case_id]
            
            # Update fields
            if 'title' in data:
                test_case.title = data['title'].strip()
            if 'description' in data:
                test_case.description = data['description'].strip()
            if 'steps' in data:
                test_case.steps = data['steps']
            if 'expected_result' in data:
                test_case.expected_result = data['expected_result'].strip()
            if 'priority' in data:
                test_case.priority = data['priority']
            if 'status' in data:
                test_case.status = data['status']
            if 'tags' in data:
                test_case.tags = data['tags']
                
            return jsonify(asdict(test_case))
            
        except Exception as e:
            return jsonify({'error': f'Error updating test case: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        try:
            del test_cases[test_case_id]
            return jsonify({'message': 'Test case deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Error deleting test case: {str(e)}'}), 500

@app.route('/api/ai-generate', methods=['POST'])
def api_ai_generate():
    """AI test case generation with real Azure OpenAI integration"""
    try:
        data = request.get_json()
        
        # Extract parameters
        requirements = data.get('requirements', '')
        project_id = data.get('project_id', '')
        test_type = data.get('test_type', 'functional')
        count = int(data.get('count', data.get('num_cases', 3)))
        
        # Validate input
        if not requirements.strip():
            return jsonify({'error': 'Requirements cannot be empty'}), 400
        
        if count > 20:  # Limit to prevent excessive API costs
            count = 20
        
        # Generate test cases using AI service
        generated_cases = ai_service.generate_test_cases(
            requirements=requirements,
            project_id=project_id,
            test_type=test_type,
            count=count
        )
        
        # Store generated test cases in memory
        for case in generated_cases:
            test_cases[case['id']] = TestCase(**case)
        
        # Get AI provider status for response
        provider_status = ai_service.get_provider_status()
        
        return jsonify({
            'generated_cases': generated_cases,
            'count': len(generated_cases),
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'status': 'success',
            'ai_provider': provider_status['primary_provider'],
            'provider_details': provider_status.get('provider_details', {})
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate test cases: {str(e)}',
            'generated_cases': [],
            'count': 0,
            'status': 'error'
        }), 500

@app.route('/api/test-runs', methods=['GET', 'POST'])
def api_test_runs():
    """Test run management API"""
    if request.method == 'GET':
        run_list = []
        for test_run in test_runs.values():
            run_dict = asdict(test_run)
            # Add additional calculated fields
            if test_run.results:
                passed = len([r for r in test_run.results.values() if r == 'Passed'])
                failed = len([r for r in test_run.results.values() if r == 'Failed'])
                run_dict['stats'] = {
                    'total_tests': len(test_run.results),
                    'passed': passed,
                    'failed': failed,
                    'pass_rate': round((passed / len(test_run.results)) * 100, 1) if test_run.results else 0
                }
            else:
                run_dict['stats'] = {'total_tests': 0, 'passed': 0, 'failed': 0, 'pass_rate': 0}
            run_list.append(run_dict)
        return jsonify(run_list)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('name', '').strip():
                return jsonify({'error': 'Test run name is required'}), 400
            
            test_run_id = str(uuid.uuid4())
            test_run = TestRun(
                id=test_run_id,
                name=data.get('name', '').strip(),
                test_suite_id=data.get('test_suite_id', ''),
                status='Not Started',
                executed_by=data.get('executed_by', 'Admin User'),
                started_at='',
                completed_at='',
                results={}
            )
            test_runs[test_run_id] = test_run
            
            # If auto_start is requested, start the run
            if data.get('auto_start', False):
                test_run.status = 'In Progress'
                test_run.started_at = datetime.utcnow().isoformat()
            
            run_dict = asdict(test_run)
            run_dict['stats'] = {'total_tests': 0, 'passed': 0, 'failed': 0, 'pass_rate': 0}
            
            return jsonify(run_dict), 201
            
        except Exception as e:
            return jsonify({'error': f'Error creating test run: {str(e)}'}), 500

@app.route('/api/test-runs/<test_run_id>/start', methods=['POST'])
def api_start_test_run(test_run_id):
    """Start a test run"""
    if test_run_id not in test_runs:
        return jsonify({'error': 'Test run not found'}), 404
    
    try:
        test_run = test_runs[test_run_id]
        test_run.status = 'In Progress'
        test_run.started_at = datetime.utcnow().isoformat()
        
        # Simulate test execution with some mock results
        mock_results = {
            'tc_001': 'Passed',
            'tc_002': 'Passed', 
            'tc_003': 'Failed',
            'tc_004': 'Passed'
        }
        test_run.results = mock_results
        
        return jsonify({
            'message': 'Test run started successfully',
            'test_run': asdict(test_run)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error starting test run: {str(e)}'}), 500

@app.route('/api/test-runs/<test_run_id>/complete', methods=['POST'])
def api_complete_test_run(test_run_id):
    """Complete a test run"""
    if test_run_id not in test_runs:
        return jsonify({'error': 'Test run not found'}), 404
    
    try:
        test_run = test_runs[test_run_id]
        test_run.status = 'Completed'
        test_run.completed_at = datetime.utcnow().isoformat()
        
        return jsonify({
            'message': 'Test run completed successfully',
            'test_run': asdict(test_run)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error completing test run: {str(e)}'}), 500

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """Dashboard statistics API - Enhanced"""
    try:
        # Calculate comprehensive statistics
        total_executions = sum(len(tr.results or {}) for tr in test_runs.values())
        passed_tests = sum(len([r for r in tr.results.values() if r == 'Passed']) for tr in test_runs.values() if tr.results)
        failed_tests = sum(len([r for r in tr.results.values() if r == 'Failed']) for tr in test_runs.values() if tr.results)
        
        # Test case statistics by priority
        priority_stats = {'High': 0, 'Medium': 0, 'Low': 0}
        for tc in test_cases.values():
            priority_stats[tc.priority] = priority_stats.get(tc.priority, 0) + 1
        
        # Test case statistics by status
        status_stats = {'Draft': 0, 'Active': 0, 'Deprecated': 0}
        for tc in test_cases.values():
            status_stats[tc.status] = status_stats.get(tc.status, 0) + 1
        
        # Recent activity simulation
        recent_activity = [
            {
                'type': 'test_generated',
                'message': f'{len([tc for tc in test_cases.values() if "ai-generated" in (tc.tags or [])])} AI-generated test cases',
                'timestamp': '2 hours ago',
                'icon': 'robot'
            },
            {
                'type': 'test_run',
                'message': f'{len([tr for tr in test_runs.values() if tr.status == "In Progress"])} active test runs',
                'timestamp': '4 hours ago', 
                'icon': 'play-circle'
            },
            {
                'type': 'project',
                'message': f'{len(projects)} total projects',
                'timestamp': '1 day ago',
                'icon': 'folder'
            }
        ]
        
        return jsonify({
            'total_projects': len(projects),
            'total_test_cases': len(test_cases),
            'total_test_suites': len(test_suites),
            'active_test_runs': len([tr for tr in test_runs.values() if tr.status == "In Progress"]),
            'total_executions': total_executions,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'pass_rate': round((passed_tests / total_executions * 100), 1) if total_executions > 0 else 0,
            'priority_stats': priority_stats,
            'status_stats': status_stats,
            'recent_activity': recent_activity,
            'health': 'healthy',
            'last_updated': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Error fetching dashboard stats: {str(e)}'}), 500

@app.route('/api/ai-status', methods=['GET'])
def api_ai_status():
    """Get AI provider status and configuration"""
    try:
        status = ai_service.get_provider_status()
        return jsonify({
            'status': 'success',
            'ai_providers': status
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Initialize some sample data for demonstration
def initialize_sample_data():
    """Initialize the platform with some sample data"""
    
    # Create a sample project
    sample_project_id = str(uuid.uuid4())
    sample_project = Project(
        id=sample_project_id,
        name="E-commerce Platform",
        description="Test management for our online shopping platform",
        created_by="Admin User",
        created_at=datetime.now(timezone.utc).isoformat()
    )
    projects[sample_project_id] = sample_project
    
    # Create sample test cases
    sample_test_cases = [
        {
            'title': 'User Login with Valid Credentials',
            'description': 'Verify that users can log in with correct email and password',
            'steps': ['Navigate to login page', 'Enter valid email', 'Enter valid password', 'Click login button'],
            'expected_result': 'User should be successfully logged in and redirected to dashboard',
            'priority': 'High',
            'status': 'Active'
        },
        {
            'title': 'Product Search Functionality',
            'description': 'Test the product search feature with various keywords',
            'steps': ['Navigate to homepage', 'Enter product name in search', 'Click search button', 'Verify results'],
            'expected_result': 'Relevant products should be displayed in search results',
            'priority': 'Medium',
            'status': 'Active'
        },
        {
            'title': 'Shopping Cart Operations',
            'description': 'Verify add to cart, update quantity, and remove item functionality',
            'steps': ['Add product to cart', 'Update quantity', 'Remove item', 'Verify cart is empty'],
            'expected_result': 'Cart operations should work correctly without errors',
            'priority': 'High',
            'status': 'Draft'
        }
    ]
    
    for i, tc_data in enumerate(sample_test_cases):
        test_case_id = str(uuid.uuid4())
        test_case = TestCase(
            id=test_case_id,
            title=tc_data['title'],
            description=tc_data['description'],
            steps=tc_data['steps'],
            expected_result=tc_data['expected_result'],
            priority=tc_data['priority'],
            status=tc_data['status'],
            project_id=sample_project_id,
            created_by="Admin User",
            created_at=datetime.now(timezone.utc).isoformat(),
            tags=['manual', 'functional']
        )
        test_cases[test_case_id] = test_case

# Initialize sample data when the app starts
initialize_sample_data()

if __name__ == '__main__':
    initialize_sample_data()
    
    print("🚀 TestGenie Enterprise Test Management Platform")
    print("=" * 60)
    print("📍 Dashboard: http://localhost:5000")
    print("📊 Projects: http://localhost:5000/projects")
    print("📝 Test Cases: http://localhost:5000/test-cases")
    print("🏃 Test Runs: http://localhost:5000/test-runs")
    print("🤖 AI Generator: http://localhost:5000/ai-generator")
    print("🔍 API Health: http://localhost:5000/api/health")
    print("=" * 60)
    print("✨ Features: Project Management | Test Cases | Test Execution | AI Generation")
    # print("🎯 Competing with: TestRail | Zephyr | qTest")
    print("🏆 Unique Advantage: AI-Powered Test Generation")
    print("=" * 60)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
