# Azure App Service Entry Point
# This file ensures Azure can find and start your application

import os
from enterprise_test_platform_sqlite import app

if __name__ == "__main__":
    # Azure App Service expects the app to run on the port specified by the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
