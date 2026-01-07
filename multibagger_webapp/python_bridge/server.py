"""
Python Bridge Server - Connects Next.js frontend to Multi-Agent AI System
"""
import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

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
logging.basicConfig(level=logging.INFO)
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
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system_available': SYSTEM_AVAILABLE,
        'system_initialized': research_system is not None,
        'timestamp': datetime.now().isoformat()
    })

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
        logger.error(f"Initialization error: {e}")
        return jsonify({
            'success': False,
            'message': f'Initialization failed: {str(e)}'
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_stocks():
    """Analyze stocks using the Multi-Agent system"""
    try:
        if not research_system:
            return jsonify({
                'error': 'System not initialized. Please initialize first.'
            }), 400

        data = request.get_json()
        stocks = data.get('stocks', [])
        
        if not stocks:
            return jsonify({
                'error': 'No stocks provided for analysis'
            }), 400

        logger.info(f"Starting analysis for stocks: {stocks}")
        
        # Run the actual Multi-Agent analysis
        results = research_system.discover_multibaggers(stocks)
        
        logger.info(f"Analysis completed. Results: {len(results.get('high_probability_multibaggers', []))} high conviction stocks")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
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
        symbol = data.get('symbol', '')
        
        if not symbol:
            return jsonify({
                'error': 'No stock symbol provided'
            }), 400

        logger.info(f"Starting single stock analysis for: {symbol}")
        
        # Run single stock analysis
        results = research_system.analyze_single_stock(symbol)
        
        logger.info(f"Single stock analysis completed for {symbol}")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Single stock analysis error: {e}")
        return jsonify({
            'error': f'Single stock analysis failed: {str(e)}'
        }), 500

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Get current system status"""
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
        logger.error(f"Status check error: {e}")
        return jsonify({
            'error': f'Status check failed: {str(e)}'
        }), 500

@app.route('/api/predefined-sets', methods=['GET'])
def get_predefined_sets():
    """Get predefined stock sets for analysis"""
    sets = [
        {
            'name': 'Historical Multibaggers',
            'stocks': ['TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS'],
            'description': 'Proven 5x-20x performers from past cycles'
        },
        {
            'name': 'Defense & Aerospace',
            'stocks': ['HAL.NS', 'BEL.NS', 'KPIT.NS', 'IRFC.NS'],
            'description': 'Defense modernization and aerospace plays'
        },
        {
            'name': 'Green Energy & Infrastructure',
            'stocks': ['KPIGREEN.NS', 'WAAREE.NS', 'PRAJIND.NS', 'KEI.NS'],
            'description': 'Renewable energy and power infrastructure'
        },
        {
            'name': 'Power Equipment',
            'stocks': ['CGPOWER.NS', 'KEI.NS', 'PRAJIND.NS'],
            'description': 'Power transmission and equipment manufacturers'
        },
        {
            'name': 'High Growth Potential',
            'stocks': ['RELIANCE.NS', 'ADANIPORTS.NS', 'BAJFINANCE.NS'],
            'description': 'Large caps with multibagger potential'
        },
        {
            'name': 'Small Cap Gems',
            'stocks': ['DEEPAKNTR.NS', 'KPIGREEN.NS', 'TANLA.NS'],
            'description': 'High-growth small cap opportunities'
        }
    ]
    
    return jsonify({'sets': sets})

if __name__ == '__main__':
    print("🚀 Starting Python Bridge Server...")
    print("🔗 Connecting Next.js Frontend to Multi-Agent AI System")
    print(f"📊 System Available: {SYSTEM_AVAILABLE}")
    
    # Try to initialize system on startup
    if SYSTEM_AVAILABLE:
        if initialize_system():
            print("✅ Multi-Agent System initialized successfully")
        else:
            print("⚠️  System initialization failed - will retry on first request")
    else:
        print("⚠️  Multi-Agent system dependencies not available")
        print("   Make sure you're in the correct directory and dependencies are installed")
    
    print("🌐 Server running on http://localhost:5000")
    print("📡 Ready to receive analysis requests from frontend")
    
    app.run(host='0.0.0.0', port=5000, debug=True)