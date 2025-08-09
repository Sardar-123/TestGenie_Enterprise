"""
Azure Deployment Readiness Check
Verifies that all components are ready for Azure deployment
"""

import os
import sys

def check_deployment_readiness():
    print("🔍 Azure Deployment Readiness Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 6
    
    # Check 1: Pipeline configuration
    print("\n1. Checking pipeline configuration...")
    if os.path.exists('azure-pipelines.yml'):
        with open('azure-pipelines.yml', 'r') as f:
            content = f.read()
            if 'cts-vibeappso2111-5' in content and 'CTS-VibeAppso211' in content:
                print("   ✅ Pipeline configured with correct Azure resources")
                checks_passed += 1
            else:
                print("   ❌ Pipeline configuration needs update")
    else:
        print("   ❌ azure-pipelines.yml not found")
    
    # Check 2: Application entry point
    print("\n2. Checking application entry point...")
    if os.path.exists('application.py'):
        print("   ✅ application.py exists for Azure App Service")
        checks_passed += 1
    else:
        print("   ❌ application.py not found")
    
    # Check 3: Requirements file
    print("\n3. Checking requirements...")
    if os.path.exists('requirements.txt'):
        print("   ✅ requirements.txt exists")
        checks_passed += 1
    else:
        print("   ❌ requirements.txt not found")
    
    # Check 4: Main application file
    print("\n4. Checking main application...")
    if os.path.exists('enterprise_test_platform_sqlite.py'):
        print("   ✅ Main application file exists")
        checks_passed += 1
    else:
        print("   ❌ Main application file not found")
    
    # Check 5: Models and database
    print("\n5. Checking database models...")
    if os.path.exists('models.py'):
        print("   ✅ Database models exist")
        checks_passed += 1
    else:
        print("   ❌ models.py not found")
    
    # Check 6: Templates
    print("\n6. Checking templates...")
    if os.path.exists('templates') and os.path.isdir('templates'):
        template_count = len([f for f in os.listdir('templates') if f.endswith('.html')])
        print(f"   ✅ {template_count} HTML templates found")
        checks_passed += 1
    else:
        print("   ❌ Templates directory not found")
    
    # Summary
    print(f"\n📊 Summary: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("\n🎉 Ready for Azure deployment!")
        print("\n📋 Next steps:")
        print("1. Go to Azure DevOps: https://dev.azure.com/Vibects5/2148336")
        print("2. Create new pipeline from azure-pipelines.yml")
        print("3. Configure service connection")
        print("4. Run the pipeline")
        print("\n🌐 Your app will be deployed to:")
        print("https://cts-vibeappso2111-5.azurewebsites.net")
        return True
    else:
        print("\n⚠️ Some issues need to be resolved before deployment")
        return False

if __name__ == '__main__':
    check_deployment_readiness()
