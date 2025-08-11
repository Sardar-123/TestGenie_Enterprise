"""
Azure App Service Entry Point for TestGenie Enterprise
This is the main entry point that Azure App Service will use.
"""
import os
import sys
import logging

# Configure logging for Azure
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import the main Flask application
    from enterprise_test_platform_sqlite import app
    logger.info("✅ Successfully imported Flask application")
    
    # For Azure App Service WSGI
    application = app
    
    if __name__ == '__main__':
        # For local development
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        
        logger.info(f"🚀 Starting TestGenie Enterprise on {host}:{port}")
        app.run(host=host, port=port, debug=False)
        
except Exception as e:
    logger.error(f"❌ Failed to start application: {str(e)}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"Directory contents: {os.listdir('.')}")
    raise
