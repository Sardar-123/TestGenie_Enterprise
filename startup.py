# Azure App Service Startup Configuration
import os
from enterprise_test_platform_sqlite import app

# Configure for Azure App Service
app.config['DEBUG'] = False
app.config['ENV'] = 'production'

# Use Azure's assigned port or default to 8000
port = int(os.environ.get('PORT', 8000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)
