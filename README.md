# 🎯 Stock Multibagger Engine

AI-powered multibagger stock discovery system using 6 specialized agents for Indian stock market analysis.

## 🚀 Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/MYRA31JAIS/stock-multibagger-engine
   cd stock-multibagger-engine
   ```

2. **Configure API Keys**
   ```bash
   # Copy and edit environment files
   cp .env.example .env
   cp multibagger_webapp/python_bridge/.env.example multibagger_webapp/python_bridge/.env
   
   # Add your API keys to both .env files
   ```

3. **Run System**
   ```bash
   # Start Python backend
   cd multibagger_webapp/python_bridge
   python server.py
   
   # Start Next.js frontend (new terminal)
   cd multibagger_webapp
   npm install && npm run dev
   ```

4. **Access**: http://localhost:3000

## 📊 System Features

- **6 AI Agents**: Fundamental, Technical, Management, Smart Money, Policy, Supervisor
- **Real Data**: Live NSE prices, financials, news sentiment, FII/DII flows
- **AI Analysis**: Multiple providers (Groq, Gemini, Hugging Face) with fallback
- **Multibagger Scoring**: 0-100% probability with detailed insights

## 🌐 Deploy to Render

Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide for production deployment.

## 🔑 Required APIs

**Free APIs** (choose at least one AI provider):
- Groq API (recommended)
- Google Gemini API  
- Hugging Face API
- NewsAPI
- Alpha Vantage API
- Finnhub API

## 📈 Example Results

**TCS.NS Analysis**: 60.9% multibagger probability
- Fundamental Score: 6.0/10
- Technical Stage: BASE
- Smart Money: Institutional interest
- Policy Impact: STRONG

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: Python Flask, Multi-Agent AI System
- **Data**: yfinance, NSE API, NewsAPI, Alpha Vantage
- **AI**: Groq, Gemini, Hugging Face APIs

## 📝 License

MIT License - See LICENSE file for details.