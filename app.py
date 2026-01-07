#!/usr/bin/env python3
"""
Root application file for Render deployment
This file starts the Python Bridge Server from the root directory
"""
import sys
import os
from pathlib import Path

# Add the multibagger_webapp/python_bridge to the Python path
bridge_path = Path(__file__).parent / "multibagger_webapp" / "python_bridge"
sys.path.insert(0, str(bridge_path))

# Change working directory to the bridge directory
os.chdir(bridge_path)

# Import the Flask app
from server import app

# Expose the app for gunicorn (this is what Render expects)
application = app

# For gunicorn compatibility
if __name__ == "__main__":
    # Render provides PORT environment variable
    port = int(os.environ.get('PORT', 10000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    print(f"🚀 Starting Stock Multibagger Engine API Server...")
    print(f"🌐 Server will run on 0.0.0.0:{port}")
    print(f"📡 PORT environment variable: {os.environ.get('PORT', 'Not set')}")
    print(f"🔗 Expected URL: https://stock-multibagger-engine.onrender.com")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
else:
    # When run by gunicorn, just expose the app
    print(f"📡 Gunicorn starting - PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"🔗 App exposed for gunicorn as 'application'")