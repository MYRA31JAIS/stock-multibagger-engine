"""
Python Bridge Server - Connects Next.js frontend to Multi-Agent AI System
Enhanced Production Version with Complete API Coverage
"""
import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the multibagger_system to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'multibagger_system'))

try:
    from main_system import MultibaggerResearchSystem
    SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Error importing MultibaggerResearchSystem: {e}")
    MultibaggerResearchSystem = None
    SYSTEM_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/python_bridge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global system instance
research_system = None

def initialize_system():
    """Initialize the Multi-Agent Research System"""
    global research_system
    try:
        if SYSTEM_AVAILABLE and MultibaggerResearchSystem:
            research_system = MultibaggerResearchSystem()
            logger.info("Multi-Agent Research System initialized successfully")
            return True
        else:
            logger.error("MultibaggerResearchSystem not available")
            return False
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        logger.error(traceback.format_exc())
        return False

def handle_error(error, context=""):
    """Centralized error handling"""
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg)
    logger.error(traceback.format_exc())
    return error_msg

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check system availability
        system_status = "healthy" if SYSTEM_AVAILABLE else "degraded"
        
        # Check if system is initialized
        system_initialized = research_system is not None
        
        # Check environment variables
        env_status = {
            'groq_api': bool(os.getenv('GROQ_API_KEY')),
            'gemini_api': bool(os.getenv('GOOGLE_GEMINI_API_KEY')),
            'huggingface_api': bool(os.getenv('HUGGINGFACE_API_KEY')),
            'news_api': bool(os.getenv('NEWS_API_KEY')),
            'alpha_vantage_api': bool(os.getenv('ALPHA_VANTAGE_API_KEY')),
            'finnhub_api': bool(os.getenv('FINNHUB_API_KEY'))
        }
        
        return jsonify({
            'status': system_status,
            'system_available': SYSTEM_AVAILABLE,
            'system_initialized': system_initialized,
            'environment_variables': env_status,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0',
            'uptime': 'running'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': handle_error(e, "Health check failed"),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def simple_health():
    """Simple health check for Render"""
    return "OK", 200

@app.route('/', methods=['GET', 'HEAD'])
def root():
    """Root endpoint for health checks"""
    return jsonify({
        'service': 'Stock Multibagger Engine API',
        'status': 'running',
        'version': '2.0',
        'endpoints': {
            'health': '/health',
            'api_health': '/api/health',
            'initialize': '/api/initialize',
            'analyze': '/api/analyze',
            'predefined_sets': '/api/predefined-sets'
        }
    })

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Get detailed system status"""
    try:
        if not research_system:
            return jsonify({
                'status': 'not_initialized',
                'agents_active': 0,
                'message': 'System not initialized',
                'system_available': SYSTEM_AVAILABLE
            })
        
        status = research_system.get_system_status()
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Status check failed")
        }), 500

# ============================================================================
# SYSTEM INITIALIZATION
# ============================================================================

@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize the AI system"""
    try:
        if not SYSTEM_AVAILABLE:
            return jsonify({
                'success': False,
                'message': 'Multi-Agent system dependencies not available. Please check Python environment.'
            }), 500

        success = initialize_system()
        if success:
            status = research_system.get_system_status()
            return jsonify({
                'success': True,
                'status': status,
                'message': 'System initialized successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to initialize system'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': handle_error(e, "Initialization failed")
        }), 500

# ============================================================================
# STOCK ANALYSIS ENDPOINTS
# ============================================================================

@app.route('/api/analyze', methods=['POST'])
def analyze_stocks():
    """Analyze stocks using the Multi-Agent system"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized. Please initialize first.'
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
            
        stocks = data.get('stocks', [])
        
        if not stocks:
            return jsonify({
                'error': 'No stocks provided for analysis'
            }), 400

        # Validate stock symbols
        if not isinstance(stocks, list):
            return jsonify({
                'error': 'Stocks must be provided as a list'
            }), 400

        logger.info(f"Starting analysis for {len(stocks)} stocks: {stocks}")
        
        # Run the actual Multi-Agent analysis
        results = research_system.discover_multibaggers(stocks)
        
        if 'error' in results:
            return jsonify({
                'error': results['error']
            }), 500
        
        logger.info(f"Analysis completed. Results: {len(results.get('high_probability_multibaggers', []))} high conviction stocks")
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Analysis failed")
        }), 500

@app.route('/api/analyze-single', methods=['POST'])
def analyze_single_stock():
    """Analyze a single stock in detail"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized. Please initialize first.'
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
            
        symbol = data.get('symbol', '').strip().upper()
        
        if not symbol:
            return jsonify({
                'error': 'No stock symbol provided'
            }), 400

        logger.info(f"Starting single stock analysis for: {symbol}")
        
        # Run single stock analysis
        results = research_system.analyze_single_stock(symbol)
        
        if 'error' in results:
            return jsonify({
                'error': results['error']
            }), 500
        
        logger.info(f"Single stock analysis completed for {symbol}")
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Single stock analysis failed")
        }), 500

# ============================================================================
# STOCK DATA ENDPOINTS
# ============================================================================

@app.route('/api/stock-data/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Get comprehensive stock data for a symbol"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized. Please initialize first.'
            }), 400

        symbol = symbol.strip().upper()
        logger.info(f"Fetching stock data for: {symbol}")
        
        # Get comprehensive stock data
        stock_data = research_system._get_comprehensive_stock_data(symbol)
        
        if not stock_data:
            return jsonify({
                'error': f'No data available for {symbol}'
            }), 404
        
        return jsonify(stock_data)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, f"Failed to fetch data for {symbol}")
        }), 500

@app.route('/api/stock-list', methods=['GET'])
def get_stock_list():
    """Get list of available NSE stocks"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized. Please initialize first.'
            }), 400

        logger.info("Fetching NSE stock list")
        
        # Get stock list from data fetcher
        stock_list = research_system.data_fetcher.get_nse_stock_list()
        
        return jsonify({
            'stocks': stock_list,
            'count': len(stock_list),
            'source': 'NSE'
        })
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Failed to fetch stock list")
        }), 500

# ============================================================================
# PREDEFINED SETS & RECOMMENDATIONS
# ============================================================================

@app.route('/api/predefined-sets', methods=['GET'])
def get_predefined_sets():
    """Get predefined stock sets for analysis"""
    sets = [
        {
            'name': 'Historical Multibaggers',
            'stocks': ['TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS'],
            'description': 'Proven 5x-20x performers from past cycles',
            'category': 'proven'
        },
        {
            'name': 'Defense & Aerospace',
            'stocks': ['HAL.NS', 'BEL.NS', 'KPIT.NS', 'IRFC.NS', 'COCHINSHIP.NS'],
            'description': 'Defense modernization and aerospace plays',
            'category': 'thematic'
        },
        {
            'name': 'Green Energy & Infrastructure',
            'stocks': ['KPIGREEN.NS', 'WAAREE.NS', 'PRAJIND.NS', 'KEI.NS', 'SUZLON.NS'],
            'description': 'Renewable energy and power infrastructure',
            'category': 'thematic'
        },
        {
            'name': 'Power Equipment',
            'stocks': ['CGPOWER.NS', 'KEI.NS', 'PRAJIND.NS', 'SKIPPER.NS'],
            'description': 'Power transmission and equipment manufacturers',
            'category': 'sector'
        },
        {
            'name': 'High Growth Potential',
            'stocks': ['RELIANCE.NS', 'ADANIPORTS.NS', 'BAJFINANCE.NS', 'HDFCBANK.NS'],
            'description': 'Large caps with multibagger potential',
            'category': 'large_cap'
        },
        {
            'name': 'Small Cap Gems',
            'stocks': ['DEEPAKNTR.NS', 'KPIGREEN.NS', 'TANLA.NS', 'ROUTE.NS'],
            'description': 'High-growth small cap opportunities',
            'category': 'small_cap'
        },
        {
            'name': 'Technology & Digital',
            'stocks': ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'TECHM.NS', 'LTTS.NS'],
            'description': 'Technology and digital transformation leaders',
            'category': 'technology'
        },
        {
            'name': 'Healthcare & Pharma',
            'stocks': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'APOLLOHOSP.NS'],
            'description': 'Healthcare and pharmaceutical companies',
            'category': 'healthcare'
        }
    ]
    
    return jsonify({'sets': sets})

@app.route('/api/trending-stocks', methods=['GET'])
def get_trending_stocks():
    """Get trending/popular stocks for analysis"""
    try:
        # This could be enhanced to fetch real trending data
        trending = {
            'most_analyzed': ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS'],
            'recent_multibaggers': ['TANLA.NS', 'DIXON.NS', 'TRENT.NS'],
            'high_momentum': ['KPIT.NS', 'CGPOWER.NS', 'KEI.NS'],
            'ai_recommended': ['DEEPAKNTR.NS', 'KPIGREEN.NS', 'PRAJIND.NS']
        }
        
        return jsonify(trending)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Failed to fetch trending stocks")
        }), 500

# ============================================================================
# ANALYSIS HISTORY & RESULTS
# ============================================================================

@app.route('/api/analysis-history', methods=['GET'])
def get_analysis_history():
    """Get recent analysis history"""
    try:
        # This could be enhanced to store and retrieve actual history
        # For now, return a mock response
        history = {
            'recent_analyses': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'stocks_analyzed': ['RELIANCE.NS', 'TCS.NS'],
                    'multibaggers_found': 1,
                    'analysis_id': 'analysis_001'
                }
            ],
            'total_analyses': 1,
            'success_rate': 100.0
        }
        
        return jsonify(history)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Failed to fetch analysis history")
        }), 500

# ============================================================================
# CONFIGURATION & SETTINGS
# ============================================================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get system configuration"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized'
            }), 400
            
        config = {
            'agent_weights': {
                'fundamentals': 0.35,
                'management': 0.15,
                'policy_macro': 0.20,
                'smart_money': 0.15,
                'technicals': 0.15
            },
            'thresholds': {
                'multibagger_threshold': 0.60,
                'watchlist_threshold': 0.45,
                'rejection_threshold': 0.30
            },
            'analysis_limits': {
                'max_stocks_per_request': 20,
                'timeout_seconds': 300
            },
            'data_sources': {
                'financial': 'yfinance + alpha_vantage',
                'news': 'newsapi',
                'technical': 'yfinance_enhanced',
                'smart_money': 'nse_api'
            }
        }
        
        return jsonify(config)
        
    except Exception as e:
        return jsonify({
            'error': handle_error(e, "Failed to fetch configuration")
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# ============================================================================
# STARTUP & MAIN
# ============================================================================

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'results', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == '__main__':
    print("🚀 Starting Enhanced Python Bridge Server...")
    print("🔗 Connecting Next.js Frontend to Multi-Agent AI System")
    print(f"📊 System Available: {SYSTEM_AVAILABLE}")
    
    # Create necessary directories
    create_directories()
    
    # Try to initialize system on startup
    if SYSTEM_AVAILABLE:
        if initialize_system():
            print("✅ Multi-Agent System initialized successfully")
        else:
            print("⚠️  System initialization failed - will retry on first request")
    else:
        print("⚠️  Multi-Agent system dependencies not available")
        print("   Make sure you're in the correct directory and dependencies are installed")
    
    # Production configuration - Render provides PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    print(f"🌐 Server starting on 0.0.0.0:{port}")
    print(f"📡 PORT environment: {os.environ.get('PORT', 'Not set - using default 5000')}")
    print("📡 Ready to receive analysis requests from frontend")
    print("\n📋 Available Endpoints:")
    print("   GET  /health - Simple health check")
    print("   GET  /api/health - Comprehensive health check")
    print("   POST /api/initialize - Initialize AI system")
    print("   POST /api/analyze - Analyze multiple stocks")
    print("   POST /api/analyze-single - Analyze single stock")
    print("   GET  /api/stock-data/<symbol> - Get stock data")
    print("   GET  /api/stock-list - Get available stocks")
    print("   GET  /api/predefined-sets - Get stock sets")
    print("   GET  /api/system-status - Get system status")
    print("   GET  /api/config - Get configuration")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)