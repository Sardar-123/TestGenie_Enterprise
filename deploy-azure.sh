#!/bin/bash
# Azure App Service Deployment Script

echo "🚀 Starting Azure deployment preparation..."

# Create deployment package
echo "📦 Creating deployment package..."
zip -r testgenie-deploy.zip . -x "venv/*" "__pycache__/*" "*.pyc" ".git/*" "*.db"

echo "✅ Deployment package created: testgenie-deploy.zip"
echo ""
echo "📋 Next steps:"
echo "1. Upload testgenie-deploy.zip to Azure App Service"
echo "2. Set environment variables in Azure portal"
echo "3. Configure startup command: python application.py"
echo "4. Test your deployment"
echo ""
echo "🌐 Your app will be available at: https://your-app-name.azurewebsites.net"
