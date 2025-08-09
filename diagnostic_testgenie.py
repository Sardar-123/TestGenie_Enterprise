import os
import sys
import traceback
from flask import Flask

def create_diagnostic_app():
    """Create a diagnostic Flask app to identify issues"""
    app = Flask(__name__)
    
    @app.route('/')
    def diagnostic_home():
        return """
        <h1>TestGenie Diagnostic Mode</h1>
        <p>Identifying startup issues...</p>
        <ul>
            <li><a href="/check-environment">Check Environment</a></li>
            <li><a href="/check-imports">Check Imports</a></li>
            <li><a href="/check-database">Check Database</a></li>
            <li><a href="/test-main-app">Test Main App</a></li>
            <li><a href="/check-files">Check Files</a></li>
        </ul>
        """
    
    @app.route('/check-environment')
    def check_environment():
        env_info = []
        env_vars = [
            'PORT', 'AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_VERSION', 'AZURE_OPENAI_DEPLOYMENT_NAME'
        ]
        
        for var in env_vars:
            value = os.environ.get(var, 'NOT SET')
            if 'KEY' in var and value != 'NOT SET':
                value = value[:10] + "..." # Hide sensitive data
            env_info.append(f"{var}: {value}")
        
        env_info.append(f"Working Directory: {os.getcwd()}")
        env_info.append(f"Python Version: {sys.version}")
        
        return "<br>".join(env_info)
    
    @app.route('/check-imports')
    def check_imports():
        results = []
        
        imports_to_test = [
            ('flask', 'Flask'),
            ('flask_sqlalchemy', 'SQLAlchemy'),
            ('openai', 'OpenAI client'),
            ('dotenv', 'load_dotenv'),
            ('models', 'TestGenie models'),
            ('ai_service', 'AI service')
        ]
        
        for module, description in imports_to_test:
            try:
                __import__(module)
                results.append(f"✅ {description} - OK")
            except Exception as e:
                results.append(f"❌ {description} - ERROR: {str(e)}")
        
        return "<br>".join(results)
    
    @app.route('/check-files')
    def check_files():
        files_info = []
        
        # Check if required files exist
        required_files = [
            'enterprise_test_platform_sqlite.py',
            'models.py',
            'ai_service.py',
            'requirements.txt'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                files_info.append(f"✅ {file} - {size} bytes")
            else:
                files_info.append(f"❌ {file} - NOT FOUND")
        
        # List all Python files
        files_info.append("<br><strong>All Python files:</strong>")
        for file in os.listdir('.'):
            if file.endswith('.py'):
                files_info.append(f"📄 {file}")
        
        return "<br>".join(files_info)
    
    @app.route('/check-database')
    def check_database():
        try:
            from models import db, Project
            return "✅ Database models imported successfully"
        except Exception as e:
            return f"❌ Database check failed: {str(e)}<br><pre>{traceback.format_exc()}</pre>"
    
    @app.route('/test-main-app')
    def test_main_app():
        try:
            # Try to import the main application
            sys.path.insert(0, os.getcwd())
            import enterprise_test_platform_sqlite as main_app
            
            # Try to get the Flask app
            if hasattr(main_app, 'app'):
                return "✅ Main application imported successfully! Flask app found."
            else:
                return "⚠️ Main application imported but no 'app' object found."
                
        except Exception as e:
            error_details = traceback.format_exc()
            return f"❌ Main application import failed:<br><pre>{str(e)}</pre><br><strong>Full traceback:</strong><br><pre>{error_details}</pre>"
    
    return app

if __name__ == "__main__":
    try:
        app = create_diagnostic_app()
        port = int(os.environ.get('PORT', 8000))
        print(f"Starting TestGenie diagnostic mode on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"Failed to start diagnostic app: {e}")
        traceback.print_exc()