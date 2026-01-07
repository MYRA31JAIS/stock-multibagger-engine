# 🚀 Multi-Agent AI Research System for Indian Multibagger Discovery

A sophisticated AI-powered system that discovers high-probability Indian multibagger stocks (5x–20x returns over 2–5 years) using multi-agent analysis of NSE & BSE listed companies.

## 🎯 Core Objective

**Identify companies transitioning from:**
`ignored/distressed → structurally improving → market leaders`

The system performs **probability discovery based on inflection analysis**, NOT price prediction.

## 🧠 Multi-Agent Architecture

### 9 Specialized AI Agents

1. **🔍 Fundamental Agent** - Financial inflection analysis
2. **👥 Management & Promoter Change Agent** - Governance upgrades
3. **📈 Technical & Market Structure Agent** - Base formation & breakouts
4. **💰 Smart Money Agent** - Institutional accumulation tracking
5. **🏛️ Government & Sector Policy Agent** - Policy tailwind mapping
6. **🏦 RBI & Monetary Cycle Agent** - Macro environment analysis
7. **💼 Budget & Capex Agent** - Government spending beneficiaries
8. **📊 Quarterly Results & Guidance Agent** - Earnings momentum
9. **🌍 Global Demand & Geopolitics Agent** - International opportunities
10. **🎯 Supervisor Agent** - Multi-agent synthesis & ranking

## 🏗️ System Design

### Agent Independence
- Each agent operates independently
- No shared internal logic
- Communication only via Supervisor
- Structured JSON outputs
- Modular implementation

### Weighted Scoring System
| Factor | Weight |
|--------|--------|
| Fundamentals | 35% |
| Management & Governance | 15% |
| Policy & Macro | 20% |
| Smart Money | 15% |
| Technicals | 15% |

## 📊 Sample Output

```json
{
  "high_probability_multibaggers": [
    {
      "symbol": "EXAMPLE.NS",
      "sector": "Power Equipment",
      "market_cap": "₹3,200 Cr",
      "multibagger_probability": 0.82,
      "expected_timeframe": "3–5 years",
      "key_triggers": [
        "Revenue CAGR improving: 25.3%",
        "Operating margin expanding: 12.5%",
        "Smart money: FII/DII net buyers",
        "Policy tailwinds: strong"
      ],
      "major_risks": [
        "Market volatility",
        "Execution risk"
      ],
      "agent_consensus": "STRONG BUY (High Conviction)"
    }
  ],
  "early_watchlist": [],
  "rejected_stocks": [],
  "disclaimer": "For research & learning only. Not financial advice."
}
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd multibagger_system

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Add your API keys to .env
OPENAI_API_KEY=your_openai_key
NSE_API_KEY=your_nse_key  # Optional
BSE_API_KEY=your_bse_key  # Optional
```

### 3. Run the System

#### Command Line Interface
```bash
# Run full analysis
python main_system.py

# Analyze specific stocks
python -c "
from main_system import MultibaggerResearchSystem
system = MultibaggerResearchSystem()
result = system.analyze_single_stock('TANLA.NS')
print(result)
"
```

#### Web Interface (Streamlit)
```bash
# Launch web interface
streamlit run streamlit_app.py
```

Access the web interface at `http://localhost:8501`

## 🔧 Agent Details

### 1. Fundamental Agent
**Input:** 10 years financial data for NSE/BSE stocks
**Analysis:**
- Revenue CAGR & PAT CAGR
- Operating margin trends
- ROCE/ROE improvement
- Debt reduction patterns
- Cash flow quality (OCF vs PAT)
- Capital allocation efficiency

**Output:**
```json
{
  "fundamental_score": 8.5,
  "key_improving_metrics": [
    "Revenue CAGR improving: 22.1%",
    "Operating margin expanding: 15.2%"
  ],
  "red_flags": []
}
```

### 2. Management & Promoter Change Agent
**Analysis:**
- Promoter holding changes
- Professional management induction
- PE/strategic investor entry
- Related-party transaction cleanup
- Governance quality assessment

**Output:**
```json
{
  "management_quality_score": 7.2,
  "evidence_of_change": [
    "Professional management team in place",
    "Strategic investor entry detected"
  ],
  "minority_shareholder_alignment": "HIGH"
}
```

### 3. Technical & Market Structure Agent
**Analysis:**
- 3-5 year base formation
- Long-term breakout confirmation
- Relative strength vs NIFTY
- Volume expansion patterns
- Trend change validation

**Output:**
```json
{
  "technical_stage": "BREAKOUT",
  "risk_reward_ratio": "1:3"
}
```

### 4. Smart Money Agent
**Analysis:**
- FII/DII flows tracking
- Mutual fund accumulation
- Bulk & block deals
- PE/VC entry detection
- Promoter buying patterns

**Output:**
```json
{
  "smart_money_conviction_score": 8.0,
  "investors_detected": [
    "FII/DII net buyers",
    "HDFC Small Cap Fund"
  ],
  "accumulation_trend": "YES"
}
```

### 5. Policy Agent
**Analysis:**
- PLI scheme beneficiaries
- Defense/infra/power/rail policies
- Import substitution opportunities
- PSU reforms & privatization

**Output:**
```json
{
  "policy_tailwind_strength": "STRONG",
  "time_horizon": "LONG"
}
```

## 📈 Historical Learning

The system learns patterns from successful Indian multibaggers:
- Tanla Solutions
- Dixon Technologies
- Trent Limited
- KPIT Technologies
- CG Power
- L&T Finance Holdings
- Tata Elxsi
- IRFC
- KEI Industries
- Deepak Nitrite
- KPI Green Energy
- Waaree Energies
- Praj Industries
- HAL
- BEL

## 🛠️ Technical Implementation

### Architecture
```
multibagger_system/
├── agents/                 # Individual AI agents
│   ├── fundamental_agent.py
│   ├── management_agent.py
│   ├── technical_agent.py
│   ├── smart_money_agent.py
│   ├── policy_agent.py
│   └── supervisor_agent.py
├── data_sources/          # Data fetching modules
│   └── nse_data_fetcher.py
├── main_system.py         # Main orchestrator
├── streamlit_app.py       # Web interface
├── config.py             # Configuration
└── requirements.txt      # Dependencies
```

### Key Features
- **Modular Design:** Each agent is independently implementable
- **Pluggable Data Sources:** Easy to add new data providers
- **Deterministic Scoring:** Explainable and transparent
- **Comprehensive Logging:** Full audit trail
- **Web Interface:** User-friendly Streamlit dashboard

## 📊 Data Sources

### Current Implementation
- **Yahoo Finance:** Historical price & financial data
- **NSE/BSE APIs:** Real-time market data (when available)
- **Simulated Data:** For bulk deals, MF holdings (prototype)

### Production Ready
- NSE Official APIs
- BSE Data Services
- Mutual Fund Holdings APIs
- FII/DII Flow Data
- Corporate Announcements
- Bulk Deal Databases

## ⚙️ Configuration

### Agent Weights (Customizable)
```python
AGENT_WEIGHTS = {
    'fundamentals': 0.35,    # 35% weight
    'management': 0.15,      # 15% weight
    'policy_macro': 0.20,    # 20% weight
    'smart_money': 0.15,     # 15% weight
    'technicals': 0.15       # 15% weight
}
```

### Scoring Thresholds
```python
MULTIBAGGER_THRESHOLD = 0.75  # High probability
WATCHLIST_THRESHOLD = 0.60    # Medium probability
REJECTION_THRESHOLD = 0.40    # Low probability
```

## 🧪 Testing & Validation

### Unit Testing
```bash
# Run individual agent tests
python -m pytest tests/test_fundamental_agent.py
python -m pytest tests/test_management_agent.py
```

### Integration Testing
```bash
# Test full system with known multibaggers
python test_historical_multibaggers.py
```

### Backtesting
```bash
# Validate against historical data
python backtest_system.py --start_date 2019-01-01 --end_date 2024-01-01
```

## 📋 Usage Examples

### 1. Analyze Single Stock
```python
from main_system import MultibaggerResearchSystem

system = MultibaggerResearchSystem()
result = system.analyze_single_stock('TANLA.NS')
print(f"Probability: {result['high_probability_multibaggers'][0]['multibagger_probability']:.1%}")
```

### 2. Batch Analysis
```python
stocks = ['DIXON.NS', 'TRENT.NS', 'KPIT.NS']
results = system.discover_multibaggers(stocks)

for stock in results['high_probability_multibaggers']:
    print(f"{stock['symbol']}: {stock['multibagger_probability']:.1%}")
```

### 3. Custom Screening
```python
# Screen by sector
tech_stocks = ['TCS.NS', 'INFY.NS', 'WIPRO.NS']
results = system.discover_multibaggers(tech_stocks)

# Filter by probability
high_conviction = [s for s in results['high_probability_multibaggers'] 
                  if s['multibagger_probability'] > 0.8]
```

## 🔍 Monitoring & Alerts

### Weekly Refresh
```bash
# Set up cron job for weekly analysis
0 9 * * 1 cd /path/to/system && python main_system.py --mode weekly
```

### Real-time Monitoring
```python
# Monitor specific watchlist
watchlist = ['STOCK1.NS', 'STOCK2.NS']
system.monitor_watchlist(watchlist, alert_threshold=0.75)
```

## 🚨 Risk Management

### Built-in Safeguards
- **Diversification Checks:** Prevents sector concentration
- **Liquidity Filters:** Ensures adequate trading volume
- **Volatility Assessment:** Risk-adjusted scoring
- **Correlation Analysis:** Avoids similar bets

### Risk Metrics
- Maximum position size: 5% per stock
- Sector exposure limit: 25% per sector
- Minimum market cap: ₹500 Cr
- Minimum daily volume: ₹10 Cr

## 📚 Documentation

### API Reference
- [Agent APIs](docs/agent_apis.md)
- [Data Sources](docs/data_sources.md)
- [Configuration Guide](docs/configuration.md)

### Tutorials
- [Getting Started](docs/getting_started.md)
- [Custom Agent Development](docs/custom_agents.md)
- [Backtesting Guide](docs/backtesting.md)

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Adding New Agents
1. Inherit from `BaseAgent` class
2. Implement `analyze()` method
3. Return structured JSON output
4. Add to supervisor weights
5. Update documentation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This system is for research and educational purposes only.**

- Not financial advice
- Past performance doesn't guarantee future results
- Always do your own research
- Consult qualified financial advisors
- Understand risks before investing

## 🆘 Support

### Issues & Bugs
- GitHub Issues: [Report bugs](https://github.com/your-repo/issues)
- Documentation: [Wiki](https://github.com/your-repo/wiki)

### Community
- Discord: [Join community](https://discord.gg/your-server)
- Telegram: [Discussion group](https://t.me/your-group)

---

**Built with ❤️ for the Indian stock market research community**

*"In the business world, the rearview mirror is always clearer than the windshield." - Warren Buffett*