# Multibagger Stock Analysis System

A sophisticated AI-powered system for discovering multibagger stocks in the Indian market using 6 specialized AI agents.

## 🏗️ System Architecture

```
User Browser
    ↓
Next.js Frontend (multibagger_webapp) - Port 3000
    ↓
Next.js API Routes (/api/initialize, /api/analyze, /api/status)
    ↓
Python Bridge Server (Flask) - Port 5000
    ↓
Multi-Agent AI System (multibagger_system)
    ├── Fundamental Agent - Financial analysis
    ├── Management Agent - Leadership quality
    ├── Technical Agent - Chart patterns
    ├── Smart Money Agent - Institutional activity
    ├── Policy Agent - Regulatory impact
    └── Supervisor Agent - Final synthesis
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Option 1: Automated Setup (Windows)
```bash
# Run the setup script
start_system.bat
```

### Option 2: Manual Setup

#### Step 1: Configure Environment Variables
1. Edit `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

2. Edit `multibagger_system/.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

#### Step 2: Install Dependencies
```bash
# Install Python dependencies
cd multibagger_system
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
cd multibagger_webapp
npm install
cd ..
```

#### Step 3: Start the System (2 terminals required)

**Terminal 1 - Python Backend:**
```bash
cd multibagger_webapp/python_bridge
python server.py
```
Wait for: "✅ Multi-Agent System initialized successfully"

**Terminal 2 - Next.js Frontend:**
```bash
cd multibagger_webapp
npm run dev
```
Wait for: "Ready on http://localhost:3000"

#### Step 4: Access the System
Open http://localhost:3000 in your browser

## 🎯 How to Use

1. **Initialize System**: Click "Initialize AI System" button
2. **Select Stocks**: Choose from predefined sets or enter custom symbols
3. **Run Analysis**: Click "Analyze Stocks" to start AI analysis
4. **View Results**: See high-conviction multibagger candidates

## 🤖 AI Agents

### 1. Fundamental Agent (35% weight)
- Revenue growth analysis
- Profit margin trends
- Debt-to-equity ratios
- Return on equity patterns
- Cash flow analysis

### 2. Management Agent (15% weight)
- Leadership quality assessment
- Corporate governance
- Strategic vision evaluation
- Execution track record

### 3. Technical Agent (15% weight)
- Chart pattern recognition
- Support/resistance levels
- Volume analysis
- Momentum indicators

### 4. Smart Money Agent (15% weight)
- Institutional buying/selling
- Mutual fund holdings
- FII/DII activity
- Bulk/block deals

### 5. Policy Agent (20% weight)
- Regulatory environment
- Government policy impact
- Sector-specific policies
- Macroeconomic factors

### 6. Supervisor Agent
- Synthesizes all agent outputs
- Applies weighted scoring
- Categorizes stocks by conviction level

## 📊 Stock Categories

- **High Probability Multibaggers** (Score ≥ 60%): Strong buy candidates
- **Early Watchlist** (Score 45-59%): Monitor for entry points
- **Rejected** (Score < 45%): Avoid or wait for better setup

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for AI analysis
- `NSE_API_KEY`: Optional, for real NSE data
- `ALPHA_VANTAGE_API_KEY`: Optional, for stock prices
- `FINNHUB_API_KEY`: Optional, for market data

### System Settings (config.py)
- `MULTIBAGGER_THRESHOLD`: 0.60 (60% minimum score)
- `WATCHLIST_THRESHOLD`: 0.45 (45% minimum score)
- `AGENT_WEIGHTS`: Configurable agent importance

## 🐛 Troubleshooting

### "Python AI system is not running"
- Ensure Python backend is started first
- Check if port 5000 is available
- Verify Python dependencies are installed

### "System initialization failed"
- Check if OPENAI_API_KEY is set correctly
- Verify internet connection for API calls
- Check Python console for error messages

### Analysis takes too long
- Reduce number of stocks analyzed
- Check OpenAI API rate limits
- Ensure stable internet connection

## 📁 Project Structure

```
├── multibagger_webapp/          # Next.js frontend
│   ├── app/                     # Next.js 13+ app directory
│   ├── python_bridge/           # Flask server connecting to AI system
│   └── package.json
├── multibagger_system/          # Python AI system
│   ├── agents/                  # 6 AI agents
│   ├── data_sources/            # Data fetching modules
│   ├── config.py                # System configuration
│   └── main_system.py           # Main orchestrator
├── .env                         # Root environment variables
└── README.md                    # This file
```

## 🔮 Future Enhancements

- Real-time NSE/BSE data integration
- Portfolio tracking and management
- Backtesting engine for strategy validation
- Mobile app for on-the-go analysis
- Advanced charting and visualization
- Email/SMS alerts for opportunities

## ⚠️ Disclaimer

This system is for educational and research purposes only. Not financial advice. Always do your own research and consult with financial advisors before making investment decisions.

## 📄 License

MIT License - See LICENSE file for details