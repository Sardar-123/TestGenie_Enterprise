#!/bin/bash
# Quick Azure Configuration Helper
# Run this script to generate the correct pipeline configuration

echo "🔧 Azure DevOps Pipeline Configuration Helper"
echo "============================================="
echo ""

echo "Please provide the following information:"
echo ""

read -p "1. Your Azure Subscription Name: " SUBSCRIPTION_NAME
read -p "2. Your App Service Name (will be created): " APP_SERVICE_NAME
read -p "3. Your Resource Group Name (default: testgenie-rg): " RESOURCE_GROUP
RESOURCE_GROUP=${RESOURCE_GROUP:-testgenie-rg}

echo ""
echo "📝 Update your azure-pipelines.yml with these values:"
echo "=================================================="
echo ""
echo "variables:"
echo "  azureSubscription: '$SUBSCRIPTION_NAME'"
echo "  appServiceName: '$APP_SERVICE_NAME'"
echo "  resourceGroup: '$RESOURCE_GROUP'"
echo ""
echo "🌐 Your app will be accessible at:"
echo "https://$APP_SERVICE_NAME.azurewebsites.net"
echo ""
echo "✅ Copy these values and update your pipeline configuration!"
