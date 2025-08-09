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

# Routes
@app.route('/')
def dashboard():
    """Main dashboard like TestRail/Zephyr"""
    stats = {
        'total_projects': Project.query.count(),
        'total_test_cases': TestCase.query.count(),
        'total_test_suites': TestSuite.query.count(),
        'active_test_runs': TestRun.query.filter_by(status="In Progress").count()
    }
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    projects_data = [p.to_dict() for p in recent_projects]
    return render_template('dashboard.html', stats=stats, projects=projects_data)

@app.route('/projects')
def projects_list():
    """Project management"""
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    projects_data = [p.to_dict() for p in all_projects]
    return render_template('projects.html', projects=projects_data)

@app.route('/projects/<project_id>')
def project_detail(project_id):
    """Project detail view"""
    project = Project.query.get_or_404(project_id)
    project_test_cases = TestCase.query.filter_by(project_id=project_id).all()
    project_test_suites = TestSuite.query.filter_by(project_id=project_id).all()
    
    return render_template('project_detail.html', 
                         project=project.to_dict(),
                         test_cases=[tc.to_dict() for tc in project_test_cases],
                         test_suites=[ts.to_dict() for ts in project_test_suites])

@app.route('/test-cases')
def test_cases_list():
    """Test case management"""
    all_test_cases = TestCase.query.order_by(TestCase.created_at.desc()).all()
    test_cases_data = [tc.to_dict() for tc in all_test_cases]
    return render_template('test_cases.html', test_cases=test_cases_data)

@app.route('/test-case/<test_case_id>')
def test_case_detail(test_case_id):
    """Test case detail view"""
    test_case = TestCase.query.get_or_404(test_case_id)
    return render_template('test_case_detail.html', test_case=test_case.to_dict())

@app.route('/test-runs')
def test_runs_list():
    """Test execution management"""
    all_test_runs = TestRun.query.order_by(TestRun.created_at.desc()).all()
    test_runs_data = [tr.to_dict() for tr in all_test_runs]
    return render_template('test_runs.html', test_runs=test_runs_data)

@app.route('/ai-generator')
def ai_generator():
    """AI test case generator"""
    return render_template('ai_generator.html')

@app.route('/settings')
def settings():
    """Platform settings"""
    return render_template('settings.html')

@app.route('/reports')
def reports():
    """Analytics and reports"""
    # Calculate comprehensive statistics
    total_projects = Project.query.count()
    total_test_cases = TestCase.query.count()
    total_test_suites = TestSuite.query.count()
    total_test_runs = TestRun.query.count()
    
    # Test case statistics by status
    test_case_stats = {}
    for status in ['Draft', 'Under Review', 'Approved', 'Obsolete']:
        test_case_stats[status] = TestCase.query.filter_by(status=status).count()
    
    # Test case statistics by priority
    priority_stats = {}
    for priority in ['Low', 'Medium', 'High']:
        priority_stats[priority] = TestCase.query.filter_by(priority=priority).count()
    
    stats = {
        'total_projects': total_projects,
        'total_test_cases': total_test_cases,
        'total_test_suites': total_test_suites,
        'total_test_runs': total_test_runs,
        'test_case_stats': test_case_stats,
        'priority_stats': priority_stats
    }
    
    return render_template('reports.html', stats=stats)

# API Routes
@app.route('/api/health')
def health_check():
    """API Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '2.0.0-sqlite',
        'database': 'sqlite'
    })

# Projects API
@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    """Projects CRUD API"""
    if request.method == 'GET':
        all_projects = Project.query.order_by(Project.created_at.desc()).all()
        return jsonify([p.to_dict() for p in all_projects])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('name', '').strip():
                return jsonify({'error': 'Project name is required'}), 400
            
            # Check for duplicate names
            existing = Project.query.filter_by(name=data.get('name').strip()).first()
            if existing:
                return jsonify({'error': 'Project name already exists'}), 400
            
            # Create new project
            project = Project(
                name=data.get('name').strip(),
                description=data.get('description', ''),
                created_by=data.get('created_by', 'admin')
            )
            
            db.session.add(project)
            db.session.commit()
            
            return jsonify(project.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating project: {str(e)}'}), 500

# Test Cases API
@app.route('/api/test-cases', methods=['GET', 'POST'])
def api_test_cases():
    """Test cases CRUD API with filtering"""
    if request.method == 'GET':
        # Get query parameters for filtering
        project_id = request.args.get('project_id')
        status = request.args.get('status')
        priority = request.args.get('priority')
        search = request.args.get('search', '').strip()
        
        # Build query
        query = TestCase.query
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if search:
            query = query.filter(TestCase.title.contains(search))
        
        # Execute query
        test_cases = query.order_by(TestCase.created_at.desc()).all()
        return jsonify([tc.to_dict() for tc in test_cases])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('title', '').strip():
                return jsonify({'error': 'Test case title is required'}), 400
            
            if not data.get('project_id'):
                return jsonify({'error': 'Project ID is required'}), 400
            
            # Verify project exists
            project = Project.query.get(data.get('project_id'))
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            
            # Create new test case
            test_case = TestCase(
                title=data.get('title').strip(),
                description=data.get('description', ''),
                expected_result=data.get('expected_result', ''),
                priority=data.get('priority', 'Medium'),
                status=data.get('status', 'Draft'),
                project_id=data.get('project_id'),
                created_by=data.get('created_by', 'system')
            )
            
            # Handle steps and tags
            if data.get('steps'):
                test_case.set_steps(data.get('steps'))
            if data.get('tags'):
                test_case.set_tags(data.get('tags'))
            
            db.session.add(test_case)
            db.session.commit()
            
            return jsonify(test_case.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating test case: {str(e)}'}), 500

@app.route('/api/test-cases/<test_case_id>', methods=['GET', 'PUT', 'DELETE'])
def api_test_case_detail(test_case_id):
    """Individual test case operations"""
    test_case = TestCase.query.get_or_404(test_case_id)
    
    if request.method == 'GET':
        return jsonify(test_case.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            
            # Update fields
            if 'title' in data:
                test_case.title = data['title'].strip()
            if 'description' in data:
                test_case.description = data['description']
            if 'expected_result' in data:
                test_case.expected_result = data['expected_result']
            if 'priority' in data:
                test_case.priority = data['priority']
            if 'status' in data:
                test_case.status = data['status']
            if 'steps' in data:
                test_case.set_steps(data['steps'])
            if 'tags' in data:
                test_case.set_tags(data['tags'])
            
            # Update timestamp
            test_case.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify(test_case.to_dict())
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating test case: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(test_case)
            db.session.commit()
            return jsonify({'message': 'Test case deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error deleting test case: {str(e)}'}), 500

# AI Generation API
@app.route('/api/ai-generate', methods=['POST'])
def api_ai_generate():
    """AI test case generation with SQLite storage"""
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
        
        # Verify project exists if provided
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
        
        # Generate test cases using AI service
        generated_cases = ai_service.generate_test_cases(
            requirements=requirements,
            project_id=project_id,
            test_type=test_type,
            count=count
        )
        
        # Store generated test cases in SQLite database
        stored_cases = []
        for case_data in generated_cases:
            test_case = TestCase(
                title=case_data.get('title', 'AI Generated Test Case'),
                description=case_data.get('description', ''),
                expected_result=case_data.get('expected_result', ''),
                priority=case_data.get('priority', 'Medium'),
                status='Draft',
                project_id=project_id,
                created_by='ai-system'
            )
            
            # Handle steps and tags
            if case_data.get('steps'):
                test_case.set_steps(case_data.get('steps'))
            if case_data.get('tags'):
                test_case.set_tags(case_data.get('tags', []) + ['ai-generated'])
            else:
                test_case.set_tags(['ai-generated'])
            
            db.session.add(test_case)
            stored_cases.append(test_case)
        
        # Commit all test cases
        db.session.commit()
        
        # Convert to dictionaries for response
        response_cases = [tc.to_dict() for tc in stored_cases]
        
        # Get AI provider status for response
        provider_status = ai_service.get_provider_status()
        
        return jsonify({
            'generated_cases': response_cases,
            'count': len(response_cases),
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'status': 'success',
            'ai_provider': provider_status['primary_provider'],
            'provider_details': provider_status.get('provider_details', {}),
            'stored_in_database': True
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to generate test cases: {str(e)}',
            'status': 'failed',
            'generated_at': datetime.now(timezone.utc).isoformat()
        }), 500

# Test Runs API
@app.route('/api/test-runs', methods=['GET', 'POST'])
def api_test_runs():
    """Test runs CRUD API"""
    if request.method == 'GET':
        # Filter by status if provided
        status = request.args.get('status')
        
        query = TestRun.query
        if status:
            query = query.filter_by(status=status)
        
        test_runs = query.order_by(TestRun.created_at.desc()).all()
        return jsonify([tr.to_dict() for tr in test_runs])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data or not data.get('name', '').strip():
                return jsonify({'error': 'Test run name is required'}), 400
            
            # Create new test run
            test_run = TestRun(
                name=data.get('name', '').strip(),
                test_suite_id=data.get('test_suite_id', ''),
                status='Not Started',
                executed_by=data.get('executed_by', 'admin')
            )
            
            # If auto_start is requested, start the run
            if data.get('auto_start', False):
                test_run.status = 'In Progress'
                test_run.started_at = datetime.utcnow()
            
            db.session.add(test_run)
            db.session.commit()
            
            return jsonify(test_run.to_dict()), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creating test run: {str(e)}'}), 500

@app.route('/api/test-runs/<test_run_id>/start', methods=['POST'])
def api_start_test_run(test_run_id):
    """Start a test run"""
    test_run = TestRun.query.get_or_404(test_run_id)
    
    try:
        test_run.status = 'In Progress'
        test_run.started_at = datetime.utcnow()
        
        # Simulate test execution with some mock results
        mock_results = {
            'sample_test_1': 'Passed',
            'sample_test_2': 'Failed',
            'sample_test_3': 'Passed'
        }
        test_run.set_results(mock_results)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Test run started successfully',
            'test_run': test_run.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error starting test run: {str(e)}'}), 500

@app.route('/api/test-runs/<test_run_id>/complete', methods=['POST'])
def api_complete_test_run(test_run_id):
    """Complete a test run"""
    test_run = TestRun.query.get_or_404(test_run_id)
    
    try:
        data = request.get_json()
        
        test_run.status = 'Completed'
        test_run.completed_at = datetime.utcnow()
        
        # Update results if provided
        if data and data.get('results'):
            test_run.set_results(data.get('results'))
        
        db.session.commit()
        
        return jsonify({
            'message': 'Test run completed successfully',
            'test_run': test_run.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error completing test run: {str(e)}'}), 500

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """Dashboard statistics API"""
    try:
        stats = {
            'total_projects': Project.query.count(),
            'total_test_cases': TestCase.query.count(),
            'total_test_suites': TestSuite.query.count(),
            'total_test_runs': TestRun.query.count(),
            'active_test_runs': TestRun.query.filter_by(status='In Progress').count(),
            'recent_activity': [],
            'test_case_stats': {
                'draft': TestCase.query.filter_by(status='Draft').count(),
                'approved': TestCase.query.filter_by(status='Approved').count(),
                'under_review': TestCase.query.filter_by(status='Under Review').count()
            },
            'health': 'healthy',
            'database': 'sqlite',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Add recent activity
        recent_test_cases = TestCase.query.order_by(TestCase.created_at.desc()).limit(5).all()
        for tc in recent_test_cases:
            stats['recent_activity'].append({
                'type': 'test_case_created',
                'title': tc.title,
                'project_id': tc.project_id,
                'created_at': tc.created_at.isoformat() if tc.created_at else None
            })
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': f'Error fetching dashboard stats: {str(e)}',
            'health': 'degraded'
        }), 500

@app.route('/api/ai-status', methods=['GET'])
def api_ai_status():
    """AI provider status API"""
    try:
        provider_status = ai_service.get_provider_status()
        return jsonify({
            'ai_providers': provider_status,
            'capabilities': [
                'test_case_generation',
                'multiple_test_types',
                'requirements_analysis'
            ],
            'database_integration': True,
            'status': 'operational'
        })
    except Exception as e:
        return jsonify({
            'error': f'Error checking AI status: {str(e)}',
            'status': 'error'
        }), 500

# Initialize sample data on first run
def init_sample_data():
    """Initialize sample data if database is empty"""
    if Project.query.count() == 0:
        print("🗄️ Database is empty, initializing with sample data...")
        
        # Create a sample project
        sample_project = Project(
            name='Sample Project',
            description='Auto-generated sample project for demonstration'
        )
        db.session.add(sample_project)
        db.session.commit()
        
        print("✅ Sample project created")

if __name__ == '__main__':
    with app.app_context():
        init_sample_data()
    
    print("🚀 Starting TestGenie Enterprise Platform with SQLite Database")
    print("=" * 60)
    print("🌐 Main Application: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/")
    print("📁 Projects: http://localhost:5000/projects")
    print("📝 Test Cases: http://localhost:5000/test-cases")
    print("🤖 AI Generator: http://localhost:5000/ai-generator")
    print("🔍 API Health: http://localhost:5000/api/health")
    print("=" * 60)
    print("🗄️ Database: SQLite (testgenie.db)")
    print("🤖 AI Provider: Azure OpenAI")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
