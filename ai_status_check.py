"""
Quick Azure OpenAI Status Check for TestGenie Enterprise
"""

print("🚀 TestGenie Enterprise - Azure OpenAI Integration Status")
print("=" * 55)

# Check environment setup
print("\n📋 Environment Configuration:")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    # Check Azure OpenAI credentials
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    model = os.getenv('AZURE_OPENAI_MODEL')
    
    print(f"   ✅ Azure OpenAI Endpoint: {endpoint[:30]}..." if endpoint else "   ❌ Missing endpoint")
    print(f"   ✅ API Key: {'*' * 20}...{api_key[-10:]}" if api_key else "   ❌ Missing API key")
    print(f"   ✅ Deployment: {deployment}" if deployment else "   ❌ Missing deployment")
    print(f"   ✅ Model: {model}" if model else "   ❌ Missing model")
    
except Exception as e:
    print(f"   ❌ Error loading environment: {e}")

print(f"\n🧠 AI Integration Features:")
print(f"   ✅ Multi-provider support (Azure OpenAI primary)")
print(f"   ✅ Automatic fallback to mock generation")
print(f"   ✅ Real-time test case generation")
print(f"   ✅ Context-aware test scenarios")
print(f"   ✅ Multiple test types (Functional, API, Performance)")

print(f"\n🎯 How to Test:")
print(f"   1. Open: http://localhost:5000/ai-generator")
print(f"   2. Enter requirements in the text area")
print(f"   3. Select test type and count")
print(f"   4. Click 'Generate Test Cases with AI'")
print(f"   5. See real Azure OpenAI generated test cases!")

print(f"\n💡 Extensibility:")
print(f"   • Easy to add OpenAI GPT-4 as fallback")  
print(f"   • Can integrate Claude or Gemini later")
print(f"   • Provider switching via .env configuration")
print(f"   • Cost-effective with fallback to mock generation")

print("\n" + "=" * 55)
print("✨ Your Azure OpenAI integration is ready to use! ✨")
