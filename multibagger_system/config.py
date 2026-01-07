"""
Configuration file for Multi-Agent AI Research System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NSE_API_KEY = os.getenv('NSE_API_KEY')
BSE_API_KEY = os.getenv('BSE_API_KEY')

# Market Configuration
MARKET_CAP_FILTER = 8000  # Crores - Small & Mid Cap filter
MIN_YEARS_DATA = 10  # Minimum years of historical data required
QUARTERS_TO_ANALYZE = 8  # Last 8 quarters for momentum analysis

# Agent Weights for Final Scoring
AGENT_WEIGHTS = {
    'fundamentals': 0.35,
    'management': 0.15,
    'policy_macro': 0.20,
    'smart_money': 0.15,
    'technicals': 0.15
}

# Scoring Thresholds
MULTIBAGGER_THRESHOLD = 0.60  # Minimum score for high probability (reduced from 0.75)
WATCHLIST_THRESHOLD = 0.45    # Minimum score for watchlist (reduced from 0.60)
REJECTION_THRESHOLD = 0.30    # Below this gets rejected (reduced from 0.40)

# Historical Multibaggers for Pattern Learning
HISTORICAL_MULTIBAGGERS = [
    'TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS',
    'L&TFH.NS', 'TATAELXSI.NS', 'IRFC.NS', 'KEI.NS', 'DEEPAKNTR.NS',
    'KPIGREEN.NS', 'WAAREE.NS', 'PRAJIND.NS', 'HAL.NS', 'BEL.NS'
]

# Data Sources
NSE_BASE_URL = "https://www.nseindia.com"
BSE_BASE_URL = "https://www.bseindia.com"
YAHOO_FINANCE_SUFFIX = ".NS"  # For NSE stocks
BSE_SUFFIX = ".BO"  # For BSE stocks

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# File Paths
DATA_DIR = "data"
RESULTS_DIR = "results"
LOGS_DIR = "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)