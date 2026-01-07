#!/bin/bash

echo "🚀 Starting Multibagger Stock Analysis System..."
echo

echo "⚙️  Step 1: Installing Python dependencies..."
cd multibagger_system
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
cd ..

echo "⚙️  Step 2: Installing Node.js dependencies..."
cd multibagger_webapp
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi
cd ..

echo
echo "✅ Dependencies installed successfully!"
echo
echo "📋 IMPORTANT: Before starting the system, please:"
echo "   1. Edit .env file and add your OPENAI_API_KEY"
echo "   2. Edit multibagger_system/.env file and add your OPENAI_API_KEY"
echo
echo "🔑 Get your OpenAI API key from: https://platform.openai.com/api-keys"
echo
echo "🚀 To start the system, run these commands in separate terminals:"
echo
echo "Terminal 1 - Python Backend:"
echo "   cd multibagger_webapp/python_bridge"
echo "   python server.py"
echo
echo "Terminal 2 - Next.js Frontend:"
echo "   cd multibagger_webapp"
echo "   npm run dev"
echo
echo "Then open http://localhost:3000 in your browser"
echo