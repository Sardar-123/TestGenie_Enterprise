"""
AI Generator Debugging Script
This will help identify issues with the AI generator page
"""

import subprocess
import time
import requests
import json

def test_ai_generator():
    print("🔍 Testing AI Generator Issues")
    print("=" * 40)
    
    # First, let's start the server in the background
    print("1. Starting TestGenie server...")
    try:
        # Start server process
        server_process = subprocess.Popen([
            'python', 'enterprise_test_platform.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test server connectivity
        print("2. Testing server connectivity...")
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running")
        else:
            print(f"   ❌ Server health check failed: {response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Cannot start server: {e}")
        return
    
    try:
        # Test projects API
        print("3. Testing projects API...")
        projects_response = requests.get('http://localhost:5000/api/projects', timeout=5)
        
        if projects_response.status_code == 200:
            projects_data = projects_response.json()
            print(f"   ✅ Projects API working - Found {len(projects_data)} projects")
            
            if len(projects_data) == 0:
                print("   ⚠️  No projects found - creating a test project...")
                # Create a test project
                new_project = {
                    'name': 'Test Project',
                    'description': 'Automatically created test project'
                }
                create_response = requests.post('http://localhost:5000/api/projects', 
                                              json=new_project, timeout=5)
                if create_response.status_code == 201:
                    print("   ✅ Test project created successfully")
                else:
                    print(f"   ❌ Failed to create test project: {create_response.status_code}")
        else:
            print(f"   ❌ Projects API failed: {projects_response.status_code}")
            print(f"   Response: {projects_response.text}")
            
    except Exception as e:
        print(f"   ❌ Projects API error: {e}")
    
    try:
        # Test AI status API
        print("4. Testing AI status API...")
        ai_status_response = requests.get('http://localhost:5000/api/ai-status', timeout=5)
        
        if ai_status_response.status_code == 200:
            ai_data = ai_status_response.json()
            print(f"   ✅ AI Status API working")
            print(f"   🤖 Primary provider: {ai_data.get('ai_providers', {}).get('primary_provider', 'None')}")
        else:
            print(f"   ❌ AI Status API failed: {ai_status_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ AI Status API error: {e}")
    
    try:
        # Test AI generation with a simple request
        print("5. Testing AI generation...")
        test_request = {
            'requirements': 'Test user login functionality',
            'project_id': 'test-project',
            'test_type': 'functional',
            'count': 3
        }
        
        ai_gen_response = requests.post('http://localhost:5000/api/ai-generate', 
                                       json=test_request, timeout=30)
        
        if ai_gen_response.status_code == 200:
            ai_result = ai_gen_response.json()
            print(f"   ✅ AI Generation working - Generated {len(ai_result.get('generated_cases', []))} test cases")
        else:
            print(f"   ❌ AI Generation failed: {ai_gen_response.status_code}")
            print(f"   Response: {ai_gen_response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ AI Generation error: {e}")
    
    finally:
        # Clean up - terminate server
        if 'server_process' in locals():
            server_process.terminate()
            print("6. Server stopped")
    
    print("\n" + "=" * 40)
    print("🎯 Action Items:")
    print("1. Open browser to http://localhost:5000/ai-generator")
    print("2. Check browser console for JavaScript errors")
    print("3. Verify projects dropdown loads correctly")
    print("4. Test AI generation with sample requirements")
    print("\n💡 If issues persist:")
    print("- Check that virtual environment is activated")
    print("- Verify .env file has Azure OpenAI credentials")
    print("- Clear browser cache and reload page")

if __name__ == "__main__":
    test_ai_generator()
