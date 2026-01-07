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

# Expose the app for gunicorn
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    print(f"🚀 Starting Stock Multibagger Engine API Server...")
    print(f"🌐 Server running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)