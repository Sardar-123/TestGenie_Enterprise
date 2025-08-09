"""
TestGenie - Simplified Runnable Version
A simplified version for immediate testing and development
"""
from flask import Flask, render_template, request, flash, jsonify
import os
import json
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Create uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """API Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0-dev',
        'timestamp': datetime.utcnow().isoformat(),
        'message': 'TestGenie Enterprise API is running'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """File upload endpoint"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    return jsonify({
        'message': 'File uploaded successfully',
        'filename': filename,
        'size': os.path.getsize(filepath),
        'upload_time': datetime.utcnow().isoformat()
    })

@app.route('/api/generate-test-cases', methods=['POST'])
def generate_test_cases():
    """Mock test case generation"""
    data = request.get_json()
    
    # Mock response for testing
    mock_test_cases = f"""
# Generated Test Cases

## Test Case 1: Basic Functionality Test
**Objective**: Verify basic system functionality
**Steps**:
1. Open the application
2. Navigate to main page
3. Verify all elements load correctly
**Expected Result**: All page elements display properly

## Test Case 2: File Upload Test
**Objective**: Test file upload functionality
**Steps**:
1. Click upload button
2. Select a valid file
3. Click submit
**Expected Result**: File uploads successfully

## Test Case 3: Error Handling Test
**Objective**: Verify error handling
**Steps**:
1. Try to upload invalid file
2. Observe error message
**Expected Result**: Appropriate error message displayed

Generated on: {datetime.utcnow().isoformat()}
Configuration: {json.dumps(data, indent=2) if data else 'Default'}
"""
    
    return jsonify({
        'test_cases': mock_test_cases,
        'generated_at': datetime.utcnow().isoformat(),
        'status': 'success'
    })

@app.route('/api/status')
def system_status():
    """System status endpoint"""
    return jsonify({
        'application': 'TestGenie Enterprise',
        'version': '2.0.0-dev',
        'status': 'running',
        'features': {
            'file_upload': True,
            'test_generation': True,
            'api_endpoints': True,
            'health_monitoring': True
        },
        'endpoints': {
            'health': '/api/health',
            'upload': '/api/upload',
            'generate': '/api/generate-test-cases',
            'status': '/api/status'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting TestGenie Enterprise Development Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔍 API Health Check: http://localhost:5000/api/health")
    print("📊 System Status: http://localhost:5000/api/status")
    print("📁 Upload Endpoint: http://localhost:5000/api/upload")
    print("🤖 Generate Test Cases: http://localhost:5000/api/generate-test-cases")
    print("\n✅ Ready for testing!")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
