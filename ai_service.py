"""
AI Service Module for TestGenie Enterprise
Supports multiple AI providers with easy switching capability
Currently configured for Azure OpenAI with fallback options
"""

import os
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dataclasses import asdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """
    Flexible AI service that can work with multiple providers
    Currently supports Azure OpenAI with extensibility for other providers
    """
    
    def __init__(self):
        self.primary_provider = os.getenv('AI_PRIMARY_PROVIDER', 'azure')
        self.setup_providers()
    
    def setup_providers(self):
        """Initialize AI providers based on available credentials"""
        self.providers = {}
        
        # Azure OpenAI Setup
        if self._has_azure_credentials():
            try:
                from openai import AzureOpenAI
                
                # Try multiple initialization methods for compatibility
                try:
                    # Method 1: Standard initialization
                    self.providers['azure'] = AzureOpenAI(
                        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                        api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
                        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
                    )
                    logger.info("✅ Azure OpenAI provider initialized successfully (standard method)")
                except Exception as e1:
                    logger.warning(f"⚠️ Standard initialization failed: {e1}")
                    try:
                        # Method 2: Basic initialization without optional parameters
                        self.providers['azure'] = AzureOpenAI(
                            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                            api_version=os.getenv('AZURE_OPENAI_API_VERSION')
                        )
                        logger.info("✅ Azure OpenAI provider initialized successfully (basic method)")
                    except Exception as e2:
                        logger.error(f"❌ Basic initialization also failed: {e2}")
                        raise e2
                        
            except Exception as e:
                logger.error(f"❌ Failed to initialize Azure OpenAI: {e}")
                logger.error(f"❌ OpenAI library version might be incompatible")
        
        # OpenAI Setup (fallback)
        if self._has_openai_credentials():
            try:
                from openai import OpenAI
                self.providers['openai'] = OpenAI(
                    api_key=os.getenv('OPENAI_API_KEY')
                )
                logger.info("✅ OpenAI provider initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI: {e}")
        
        # Future providers can be added here
        # self._setup_anthropic()
        # self._setup_gemini()
        
        if not self.providers:
            logger.warning("⚠️ No AI providers available, falling back to mock generation")
    
    def _has_azure_credentials(self) -> bool:
        """Check if Azure OpenAI credentials are available"""
        # Log what we're seeing for debugging
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION')
        
        logger.info(f"🔍 Azure OpenAI Environment Check:")
        logger.info(f"   API_KEY: {'✅ Set' if api_key else '❌ Missing'}")
        logger.info(f"   ENDPOINT: {'✅ Set' if endpoint else '❌ Missing'} - {endpoint}")
        logger.info(f"   DEPLOYMENT: {'✅ Set' if deployment else '❌ Missing'} - {deployment}")
        logger.info(f"   API_VERSION: {'✅ Set' if api_version else '❌ Missing'} - {api_version}")
        
        has_credentials = all([api_key, endpoint, deployment])
        logger.info(f"🎯 Azure credentials check result: {'✅ PASS' if has_credentials else '❌ FAIL'}")
        
        return has_credentials
    
    def _has_openai_credentials(self) -> bool:
        """Check if OpenAI credentials are available"""
        return bool(os.getenv('OPENAI_API_KEY'))
    
    def generate_test_cases(self, requirements: str, project_id: str, 
                          test_type: str, count: int) -> List[Dict[str, Any]]:
        """
        Generate test cases using AI based on requirements
        
        Args:
            requirements: User requirements or description
            project_id: Target project ID
            test_type: Type of test (functional, api, performance, etc.)
            count: Number of test cases to generate
            
        Returns:
            List of generated test case dictionaries
        """
        
        # Try primary provider first
        if self.primary_provider in self.providers:
            try:
                return self._generate_with_provider(
                    self.primary_provider, requirements, project_id, test_type, count
                )
            except Exception as e:
                logger.error(f"❌ Primary provider {self.primary_provider} failed: {e}")
        
        # Try fallback providers
        for provider_name, provider in self.providers.items():
            if provider_name != self.primary_provider:
                try:
                    logger.info(f"🔄 Trying fallback provider: {provider_name}")
                    return self._generate_with_provider(
                        provider_name, requirements, project_id, test_type, count
                    )
                except Exception as e:
                    logger.error(f"❌ Fallback provider {provider_name} failed: {e}")
        
        # Final fallback to mock generation
        logger.warning("⚠️ All AI providers failed, using mock generation")
        return self._generate_mock_test_cases(requirements, project_id, test_type, count)
    
    def _generate_with_provider(self, provider_name: str, requirements: str, 
                              project_id: str, test_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate test cases using a specific AI provider"""
        
        if provider_name == 'azure':
            return self._generate_with_azure(requirements, project_id, test_type, count)
        elif provider_name == 'openai':
            return self._generate_with_openai(requirements, project_id, test_type, count)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
    
    def _generate_with_azure(self, requirements: str, project_id: str, 
                           test_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate test cases using Azure OpenAI with timeout and error handling"""
        
        client = self.providers['azure']
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        if not deployment:
            logger.error("❌ AZURE_OPENAI_DEPLOYMENT not configured")
            raise ValueError("Azure OpenAI deployment name not configured")
        
        prompt = self._create_test_generation_prompt(requirements, test_type, count)
        
        try:
            logger.info(f"🤖 Generating {count} test cases using Azure OpenAI...")
            
            # Set timeout for Azure OpenAI API call (25 seconds max for Azure App Service)
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "You are an expert test case generator for software applications. Generate comprehensive, realistic test cases in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=int(os.getenv('AI_MAX_TOKENS', 2000)),  # Reduced for faster response
                temperature=float(os.getenv('AI_TEMPERATURE', 0.7)),
                timeout=25  # 25 second timeout to stay within Azure App Service limits
            )
            
            logger.info("✅ Azure OpenAI response received successfully")
            return self._parse_ai_response(response.choices[0].message.content, project_id)
            
        except Exception as e:
            logger.error(f"❌ Azure OpenAI API error: {str(e)}")
            # Return fallback test cases if AI fails
            return self._generate_fallback_test_cases(requirements, test_type, count, project_id)
    
    def _generate_with_openai(self, requirements: str, project_id: str, 
                            test_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate test cases using OpenAI"""
        
        client = self.providers['openai']
        model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        prompt = self._create_test_generation_prompt(requirements, test_type, count)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert test case generator for software applications. Generate comprehensive, realistic test cases in JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=int(os.getenv('AI_MAX_TOKENS', 4000)),
            temperature=float(os.getenv('AI_TEMPERATURE', 0.7))
        )
        
        return self._parse_ai_response(response.choices[0].message.content, project_id)
    
    def _create_test_generation_prompt(self, requirements: str, test_type: str, count: int) -> str:
        """Create a detailed prompt for AI test case generation"""
        
        return f"""
Generate {count} comprehensive test cases for {test_type} testing based on these requirements:

Requirements: {requirements}

Please generate test cases in the following JSON format:
{{
    "test_cases": [
        {{
            "title": "Clear, descriptive test case title",
            "description": "Detailed description of what this test verifies",
            "steps": [
                "Step 1: Clear action to perform",
                "Step 2: Next action to perform",
                "Step 3: Continue with detailed steps"
            ],
            "expected_result": "Clear description of expected outcome",
            "priority": "High|Medium|Low",
            "tags": ["tag1", "tag2", "{test_type}"]
        }}
    ]
}}

Guidelines:
- Make test cases specific and actionable
- Include edge cases and negative scenarios
- Ensure steps are clear and sequential
- Focus on {test_type} testing aspects
- Use realistic data and scenarios
- Vary priority levels appropriately

Return only valid JSON without any markdown formatting or additional text.
"""
    
    def _parse_ai_response(self, response_content: str, project_id: str) -> List[Dict[str, Any]]:
        """Parse AI response and convert to test case format"""
        
        try:
            # Clean the response (remove markdown formatting if present)
            cleaned_content = response_content.strip()
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]
            cleaned_content = cleaned_content.strip()
            
            # Parse JSON
            ai_response = json.loads(cleaned_content)
            test_cases = ai_response.get('test_cases', [])
            
            # Convert to our format
            formatted_cases = []
            for i, case in enumerate(test_cases):
                import uuid
                from datetime import datetime, timezone
                
                formatted_case = {
                    'id': str(uuid.uuid4()),
                    'title': case.get('title', f'AI Generated Test Case {i+1}'),
                    'description': case.get('description', ''),
                    'steps': case.get('steps', []),
                    'expected_result': case.get('expected_result', ''),
                    'priority': case.get('priority', 'Medium'),
                    'status': 'Draft',
                    'project_id': project_id,
                    'created_by': 'AI Generator (Azure OpenAI)',
                    'created_at': datetime.now(timezone.utc).isoformat(),
                    'tags': case.get('tags', ['ai-generated'])
                }
                formatted_cases.append(formatted_case)
            
            return formatted_cases
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse AI response as JSON: {e}")
            logger.error(f"Response content: {response_content[:500]}...")
            # Fallback to mock generation
            return self._generate_mock_test_cases("AI parsing failed", project_id, "functional", 3)
        except Exception as e:
            logger.error(f"❌ Error processing AI response: {e}")
            return self._generate_mock_test_cases("AI processing failed", project_id, "functional", 3)
    
    def _generate_mock_test_cases(self, requirements: str, project_id: str, 
                                test_type: str, count: int) -> List[Dict[str, Any]]:
        """Fallback mock test case generation"""
        
        logger.info("🎭 Using mock test case generation as fallback")
        
        mock_cases = []
        
        templates = {
            'functional': {
                'prefix': 'Functional Test',
                'scenarios': [
                    'User login with valid credentials',
                    'User login with invalid credentials', 
                    'User profile update functionality',
                    'Password reset workflow',
                    'User logout functionality'
                ]
            },
            'api': {
                'prefix': 'API Test',
                'scenarios': [
                    'GET endpoint returns valid data',
                    'POST endpoint creates new resource',
                    'PUT endpoint updates existing resource', 
                    'DELETE endpoint removes resource',
                    'API authentication validation'
                ]
            },
            'performance': {
                'prefix': 'Performance Test',
                'scenarios': [
                    'Page load time under normal load',
                    'System response under high load',
                    'Memory usage optimization',
                    'Database query performance',
                    'API response time validation'
                ]
            }
        }
        
        template = templates.get(test_type, templates['functional'])
        
        for i in range(count):
            import uuid
            from datetime import datetime, timezone
            
            scenario = template['scenarios'][i % len(template['scenarios'])]
            
            mock_case = {
                'id': str(uuid.uuid4()),
                'title': f"{template['prefix']}: {scenario}",
                'description': f"Mock generated test case for {test_type} testing based on: {requirements[:100]}...",
                'steps': [
                    "Navigate to the application",
                    "Perform the required action",
                    "Verify the expected behavior",
                    "Validate the outcome"
                ],
                'expected_result': "System should behave as expected without errors",
                'priority': ['High', 'Medium', 'Low'][i % 3],
                'status': 'Draft',
                'project_id': project_id,
                'created_by': 'AI Generator (Mock)',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'tags': [test_type, 'mock-generated']
            }
            mock_cases.append(mock_case)
        
        return mock_cases
    
    def _generate_fallback_test_cases(self, requirements: str, test_type: str, 
                                     count: int, project_id: str) -> List[Dict[str, Any]]:
        """Generate basic fallback test cases when AI providers fail"""
        logger.info(f"🔄 Generating {count} fallback test cases...")
        
        fallback_cases = []
        
        # Basic test case templates based on type
        templates = {
            'functional': {
                'prefix': 'Functional Test',
                'scenarios': [
                    'Verify main functionality works as expected',
                    'Test input validation and error handling',
                    'Validate output format and accuracy',
                    'Check boundary conditions',
                    'Test normal workflow execution'
                ]
            },
            'ui': {
                'prefix': 'UI Test',
                'scenarios': [
                    'Verify UI elements are displayed correctly',
                    'Test responsive design across screen sizes',
                    'Validate user interactions and feedback',
                    'Check accessibility compliance',
                    'Test navigation and user flow'
                ]
            },
            'api': {
                'prefix': 'API Test',
                'scenarios': [
                    'Verify API endpoints respond correctly',
                    'Test request/response format validation',
                    'Check authentication and authorization',
                    'Validate error responses and status codes',
                    'Test API performance and rate limiting'
                ]
            },
            'integration': {
                'prefix': 'Integration Test',
                'scenarios': [
                    'Verify system components work together',
                    'Test data flow between modules',
                    'Check third-party service integrations',
                    'Validate end-to-end workflows',
                    'Test system resilience and failover'
                ]
            }
        }
        
        template = templates.get(test_type, templates['functional'])
        
        for i in range(count):
            scenario = template['scenarios'][i % len(template['scenarios'])]
            
            fallback_case = {
                'id': str(uuid.uuid4()),
                'title': f"{template['prefix']}: {scenario}",
                'description': f"Fallback test case for {test_type} testing. Requirements: {requirements[:150]}...",
                'steps': [
                    "Setup test environment and data",
                    "Execute the test scenario",
                    "Verify expected behavior",
                    "Clean up test data"
                ],
                'expected_result': f"The {test_type} functionality should work correctly without errors",
                'priority': 'Medium',
                'status': 'Draft',
                'project_id': project_id,
                'created_by': 'AI Generator (Fallback)',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'tags': [test_type, 'fallback-generated', 'ai-assisted']
            }
            fallback_cases.append(fallback_case)
        
        logger.info(f"✅ Generated {len(fallback_cases)} fallback test cases")
        return fallback_cases
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all AI providers"""
        status = {
            'primary_provider': self.primary_provider,
            'available_providers': list(self.providers.keys()),
            'provider_details': {}
        }
        
        if 'azure' in self.providers:
            status['provider_details']['azure'] = {
                'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
                'deployment': os.getenv('AZURE_OPENAI_DEPLOYMENT'),
                'model': os.getenv('AZURE_OPENAI_MODEL'),
                'api_version': os.getenv('AZURE_OPENAI_API_VERSION')
            }
        
        if 'openai' in self.providers:
            status['provider_details']['openai'] = {
                'model': os.getenv('OPENAI_MODEL')
            }
        
        return status

# Global AI service instance
ai_service = AIService()
