#!/usr/bin/env python3
"""
WSGI configuration for production deployment
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

# This is what gunicorn will use
application = app

if __name__ == "__main__":
    app.run()