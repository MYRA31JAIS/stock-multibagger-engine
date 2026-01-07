#!/usr/bin/env python3
"""
Startup script for the Enhanced Python Bridge Server
Handles environment setup, dependency checks, and server startup
"""
import os
import sys
import subprocess
import importlib
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask_cors',
        'pandas',
        'numpy',
        'yfinance',
        'requests',
        'python-dotenv',
        'beautifulsoup4',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Handle package name variations
            import_name = package.replace('-', '_')
            if import_name == 'flask_cors':
                import_name = 'flask_cors'
            elif import_name == 'beautifulsoup4':
                import_name = 'bs4'
            elif import_name == 'scikit_learn':
                import_name = 'sklearn'
            
            importlib.import_module(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(missing_packages):
    """Install missing dependencies"""
    if not missing_packages:
        return True
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    
    try:
        cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        'GROQ_API_KEY',
        'NEWS_API_KEY',
        'ALPHA_VANTAGE_API_KEY',
        'FINNHUB_API_KEY'
    ]
    
    optional_vars = [
        'GOOGLE_GEMINI_API_KEY',
        'HUGGINGFACE_API_KEY',
        'ANTHROPIC_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    missing_required = []
    missing_optional = []
    
    # Check required variables
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('paste_your_') or value.startswith('your_'):
            missing_required.append(var)
            print(f"❌ {var} - Not set or placeholder")
        else:
            print(f"✅ {var} - Set")
    
    # Check optional variables
    for var in optional_vars:
        value = os.getenv(var)
        if not value or value.startswith('paste_your_') or value.startswith('your_'):
            missing_optional.append(var)
            print(f"⚠️  {var} - Not set (optional)")
        else:
            print(f"✅ {var} - Set")
    
    return missing_required, missing_optional

def check_directory_structure():
    """Check if required directories exist"""
    required_dirs = ['logs', 'results', 'data']
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def check_multibagger_system():
    """Check if the multibagger system is accessible"""
    try:
        # Add the multibagger_system to Python path
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multibagger_system'))
        
        from main_system import MultibaggerResearchSystem
        print("✅ Multibagger system accessible")
        return True
    except ImportError as e:
        print(f"❌ Multibagger system not accessible: {e}")
        print("   Make sure you're running from the correct directory")
        return False

def start_server():
    """Start the Flask server"""
    try:
        print("\n🚀 Starting Enhanced Python Bridge Server...")
        
        # Import and run the server
        from server import app
        
        port = int(os.environ.get('PORT', 5000))
        debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
        
        print(f"🌐 Server will start on http://0.0.0.0:{port}")
        print("📡 Press Ctrl+C to stop the server")
        print()
        
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🔧 PYTHON BRIDGE SERVER STARTUP")
    print("=" * 50)
    
    # 1. Check Python version
    print("\n1️⃣  Checking Python version...")
    if not check_python_version():
        return False
    
    # 2. Check dependencies
    print("\n2️⃣  Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"\n📦 Found {len(missing_packages)} missing packages")
        install_choice = input("Install missing packages? (y/n): ").lower().strip()
        
        if install_choice == 'y':
            if not install_dependencies(missing_packages):
                return False
        else:
            print("❌ Cannot start server without required dependencies")
            return False
    
    # 3. Check environment variables
    print("\n3️⃣  Checking environment variables...")
    missing_required, missing_optional = check_environment_variables()
    
    if missing_required:
        print(f"\n❌ Missing required environment variables: {missing_required}")
        print("   Please set these variables in your .env file")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional environment variables: {missing_optional}")
        print("   AI functionality may be limited")
    
    # 4. Check directory structure
    print("\n4️⃣  Checking directory structure...")
    if not check_directory_structure():
        return False
    
    # 5. Check multibagger system
    print("\n5️⃣  Checking multibagger system...")
    if not check_multibagger_system():
        return False
    
    # 6. Start server
    print("\n6️⃣  All checks passed!")
    time.sleep(1)
    
    return start_server()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Startup failed")
        sys.exit(1)