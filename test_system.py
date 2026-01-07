#!/usr/bin/env python3
"""
Quick test to verify the multibagger system can initialize
"""
import sys
import os

# Add the multibagger_system to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'multibagger_system'))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("🔍 Testing imports...")
        
        # Test basic imports
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import numpy as np
        print("✅ numpy imported successfully")
        
        import yfinance as yf
        print("✅ yfinance imported successfully")
        
        import openai
        print("✅ openai imported successfully")
        
        import flask
        print("✅ flask imported successfully")
        
        from flask_cors import CORS
        print("✅ flask-cors imported successfully")
        
        # Test system imports
        from config import OPENAI_API_KEY, AGENT_WEIGHTS
        print("✅ config imported successfully")
        
        from data_sources.nse_data_fetcher import NSEDataFetcher
        print("✅ NSEDataFetcher imported successfully")
        
        from agents.supervisor_agent import SupervisorAgent
        print("✅ SupervisorAgent imported successfully")
        
        from main_system import MultibaggerResearchSystem
        print("✅ MultibaggerResearchSystem imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_system_creation():
    """Test if the system can be created"""
    try:
        print("\n🚀 Testing system creation...")
        
        # Check if OpenAI API key is set
        from config import OPENAI_API_KEY
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠️  OpenAI API key not set - system will fail during AI analysis")
            print("   Please edit multibagger_system/.env and add your OpenAI API key")
            return False
        
        # Try to create the system
        from main_system import MultibaggerResearchSystem
        system = MultibaggerResearchSystem()
        print("✅ MultibaggerResearchSystem created successfully")
        
        # Test system status
        status = system.get_system_status()
        print(f"✅ System status: {status.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ System creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Multibagger Stock Analysis System")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test system creation
    if not test_system_creation():
        print("\n❌ System creation tests failed")
        return False
    
    print("\n🎉 All tests passed!")
    print("\n📋 Next steps:")
    print("1. Make sure you have set your OPENAI_API_KEY in multibagger_system/.env")
    print("2. Start the Python bridge server:")
    print("   cd multibagger_webapp/python_bridge")
    print("   python server.py")
    print("3. Start the Next.js frontend:")
    print("   cd multibagger_webapp")
    print("   npm run dev")
    print("4. Open http://localhost:3000 in your browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)