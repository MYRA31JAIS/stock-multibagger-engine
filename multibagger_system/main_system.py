"""
Main Multi-Agent AI Research System for Indian Multibagger Stock Discovery
"""
import logging
import json
import os
from typing import Dict, List
from datetime import datetime

# Import data sources
from data_sources.nse_data_fetcher import NSEDataFetcher

# Import all agents
from agents.fundamental_agent import FundamentalAgent
from agents.management_agent import ManagementAgent
from agents.technical_agent import TechnicalAgent
from agents.smart_money_agent import SmartMoneyAgent
from agents.policy_agent import PolicyAgent
from agents.supervisor_agent import SupervisorAgent

# Import configuration
from config import *

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/multibagger_system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MultibaggerResearchSystem:
    def __init__(self):
        """Initialize the Multi-Agent Research System"""
        logger.info("Initializing Multi-Agent AI Research System")
        
        # Initialize data fetcher
        self.data_fetcher = NSEDataFetcher()
        
        # Initialize all agents
        self.fundamental_agent = FundamentalAgent()
        self.management_agent = ManagementAgent()
        self.technical_agent = TechnicalAgent()
        self.smart_money_agent = SmartMoneyAgent()
        self.policy_agent = PolicyAgent()
        self.supervisor_agent = SupervisorAgent(AGENT_WEIGHTS)
        
        logger.info("All agents initialized successfully")
    
    def discover_multibaggers(self, stock_symbols: List[str] = None) -> Dict:
        """
        Main function to discover high-probability multibagger stocks
        
        Args:
            stock_symbols: List of stock symbols to analyze. If None, fetches from NSE
            
        Returns:
            Dict: Final analysis results with ranked multibagger candidates
        """
        try:
            logger.info("Starting multibagger discovery process")
            
            # Get stock list if not provided
            if stock_symbols is None:
                logger.info("Fetching NSE stock list")
                stock_symbols = self.data_fetcher.get_nse_stock_list()
                logger.info(f"Found {len(stock_symbols)} stocks to analyze")
            
            if not stock_symbols:
                logger.error("No stocks found for analysis")
                return {"error": "No stocks found for analysis"}
            
            # Analyze each stock
            stock_analyses = []
            
            for i, symbol in enumerate(stock_symbols[:20]):  # Limit to 20 for prototype
                try:
                    logger.info(f"Analyzing stock {i+1}/{min(20, len(stock_symbols))}: {symbol}")
                    
                    # Get comprehensive data for the stock
                    stock_data = self._get_comprehensive_stock_data(symbol)
                    
                    if not stock_data:
                        logger.warning(f"Insufficient data for {symbol}, skipping")
                        continue
                    
                    # Run all agent analyses
                    stock_analysis = self._run_multi_agent_analysis(symbol, stock_data)
                    
                    if stock_analysis:
                        stock_analyses.append(stock_analysis)
                        logger.info(f"Completed analysis for {symbol}")
                    
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                    continue
            
            logger.info(f"Completed individual analyses for {len(stock_analyses)} stocks")
            
            # Run supervisor synthesis
            logger.info("Running supervisor synthesis")
            final_results = self.supervisor_agent.synthesize_analysis(stock_analyses)
            
            # Save results
            self._save_results(final_results)
            
            logger.info("Multibagger discovery process completed successfully")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in multibagger discovery: {e}")
            return {"error": f"Discovery process failed: {str(e)}"}
    
    def _get_comprehensive_stock_data(self, symbol: str) -> Dict:
        """Get all required data for a stock from various sources"""
        try:
            logger.debug(f"Fetching comprehensive data for {symbol}")
            
            # Get financial data
            financial_data = self.data_fetcher.get_financial_data(symbol)
            if not financial_data:
                return {}
            
            # Get shareholding data
            shareholding_data = self.data_fetcher.get_shareholding_pattern(symbol)
            
            # Get technical data
            technical_data = self.data_fetcher.get_technical_indicators(symbol)
            
            # Get smart money data
            fii_dii_data = self.data_fetcher.get_fii_dii_data(symbol)
            mf_holdings = self.data_fetcher.get_mutual_fund_holdings(symbol)
            bulk_deals = self.data_fetcher.get_bulk_block_deals(symbol)
            
            # Get quarterly results
            quarterly_results = self.data_fetcher.get_quarterly_results(symbol)
            
            return {
                'symbol': symbol,
                'financial_data': financial_data,
                'shareholding_data': shareholding_data,
                'technical_data': technical_data,
                'fii_dii_data': fii_dii_data,
                'mf_holdings': mf_holdings,
                'bulk_deals': bulk_deals,
                'quarterly_results': quarterly_results
            }
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return {}
    
    def _run_multi_agent_analysis(self, symbol: str, stock_data: Dict) -> Dict:
        """Run analysis from all agents for a single stock"""
        try:
            logger.debug(f"Running multi-agent analysis for {symbol}")
            
            # Extract data components
            financial_data = stock_data.get('financial_data', {})
            shareholding_data = stock_data.get('shareholding_data', {})
            technical_data = stock_data.get('technical_data', {})
            fii_dii_data = stock_data.get('fii_dii_data', {})
            mf_holdings = stock_data.get('mf_holdings', [])
            bulk_deals = stock_data.get('bulk_deals', [])
            
            # Get news sentiment for policy analysis
            company_name = financial_data.get('info', {}).get('longName', '')
            news_sentiment = self.data_fetcher.get_news_sentiment(symbol, company_name)
            
            # Run each agent analysis
            analyses = {}
            
            # 1. Fundamental Agent
            try:
                fundamental_analysis = self.fundamental_agent.analyze(financial_data)
                analyses['fundamental_analysis'] = fundamental_analysis
                logger.debug(f"Fundamental analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Fundamental analysis failed for {symbol}: {e}")
                analyses['fundamental_analysis'] = {'fundamental_score': 0, 'key_improving_metrics': [], 'red_flags': ['Analysis failed']}
            
            # 2. Management Agent
            try:
                management_analysis = self.management_agent.analyze(financial_data, shareholding_data)
                analyses['management_analysis'] = management_analysis
                logger.debug(f"Management analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Management analysis failed for {symbol}: {e}")
                analyses['management_analysis'] = {'management_quality_score': 0, 'evidence_of_change': [], 'minority_shareholder_alignment': 'LOW'}
            
            # 3. Technical Agent
            try:
                technical_analysis = self.technical_agent.analyze(financial_data, technical_data)
                analyses['technical_analysis'] = technical_analysis
                logger.debug(f"Technical analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Technical analysis failed for {symbol}: {e}")
                analyses['technical_analysis'] = {'technical_stage': 'BASE', 'risk_reward_ratio': '1:1'}
            
            # 4. Smart Money Agent (Enhanced with real data)
            try:
                smart_money_analysis = self.smart_money_agent.analyze(
                    financial_data, fii_dii_data, mf_holdings, bulk_deals
                )
                analyses['smart_money_analysis'] = smart_money_analysis
                logger.debug(f"Smart money analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Smart money analysis failed for {symbol}: {e}")
                analyses['smart_money_analysis'] = {'smart_money_score': 0, 'institutional_interest': 'LOW'}
            
            # 5. Policy Agent (Enhanced with news sentiment)
            try:
                policy_analysis = self.policy_agent.analyze(financial_data, news_sentiment)
                analyses['policy_analysis'] = policy_analysis
                logger.debug(f"Policy analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Policy analysis failed for {symbol}: {e}")
                analyses['policy_analysis'] = {'policy_tailwind_strength': 'WEAK', 'time_horizon': 'SHORT'}
            
            # Add symbol and metadata
            analyses['symbol'] = symbol
            analyses['financial_data'] = financial_data  # Add the financial data for supervisor
            analyses['analysis_timestamp'] = datetime.now().isoformat()
            analyses['data_sources'] = {
                'financial': 'yfinance + alpha_vantage',
                'news': 'newsapi' if news_sentiment.get('data_source') == 'NewsAPI' else 'unavailable',
                'bulk_deals': fii_dii_data.get('data_source', 'nse_api'),
                'technical': 'yfinance_enhanced'
            }
            
            return analyses
            
        except Exception as e:
            logger.error(f"Error in multi-agent analysis for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'fundamental_analysis': {'fundamental_score': 0},
                'management_analysis': {'management_quality_score': 0},
                'technical_analysis': {'technical_stage': 'BASE'},
                'smart_money_analysis': {'smart_money_score': 0},
                'policy_analysis': {'policy_tailwind_strength': 'WEAK'}
            }
            try:
                smart_money_analysis = self.smart_money_agent.analyze(
                    financial_data, fii_dii_data, mf_holdings, bulk_deals
                )
                analyses['smart_money_analysis'] = smart_money_analysis
                logger.debug(f"Smart money analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Smart money analysis failed for {symbol}: {e}")
                analyses['smart_money_analysis'] = {'smart_money_conviction_score': 0, 'investors_detected': [], 'accumulation_trend': 'NO'}
            
            # 5. Policy Agent
            try:
                policy_analysis = self.policy_agent.analyze(financial_data)
                analyses['policy_analysis'] = policy_analysis
                logger.debug(f"Policy analysis completed for {symbol}")
            except Exception as e:
                logger.error(f"Policy analysis failed for {symbol}: {e}")
                analyses['policy_analysis'] = {'policy_tailwind_strength': 'WEAK', 'time_horizon': 'SHORT'}
            
            # Add metadata
            analyses['symbol'] = symbol
            analyses['financial_data'] = financial_data
            analyses['analysis_timestamp'] = datetime.now().isoformat()
            
            return analyses
            
        except Exception as e:
            logger.error(f"Error in multi-agent analysis for {symbol}: {e}")
            return None
    
    def _save_results(self, results: Dict) -> None:
        """Save analysis results to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{RESULTS_DIR}/multibagger_analysis_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results saved to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def analyze_single_stock(self, symbol: str) -> Dict:
        """Analyze a single stock for testing purposes"""
        try:
            logger.info(f"Analyzing single stock: {symbol}")
            
            # Get comprehensive data
            stock_data = self._get_comprehensive_stock_data(symbol)
            
            if not stock_data:
                return {"error": f"Insufficient data for {symbol}"}
            
            # Run multi-agent analysis
            stock_analysis = self._run_multi_agent_analysis(symbol, stock_data)
            
            if not stock_analysis:
                return {"error": f"Analysis failed for {symbol}"}
            
            # Run supervisor synthesis on single stock
            final_results = self.supervisor_agent.synthesize_analysis([stock_analysis])
            
            return final_results
            
        except Exception as e:
            logger.error(f"Error analyzing single stock {symbol}: {e}")
            return {"error": f"Single stock analysis failed: {str(e)}"}
    
    def get_system_status(self) -> Dict:
        """Get system status and health check"""
        try:
            return {
                "system_name": "Multi-Agent AI Research System",
                "version": "1.0",
                "status": "operational",
                "agents": {
                    "fundamental_agent": self.fundamental_agent.name,
                    "management_agent": self.management_agent.name,
                    "technical_agent": self.technical_agent.name,
                    "smart_money_agent": self.smart_money_agent.name,
                    "policy_agent": self.policy_agent.name,
                    "supervisor_agent": self.supervisor_agent.name
                },
                "agent_weights": self.supervisor_agent.agent_weights,
                "thresholds": {
                    "multibagger_threshold": self.supervisor_agent.multibagger_threshold,
                    "watchlist_threshold": self.supervisor_agent.watchlist_threshold,
                    "rejection_threshold": self.supervisor_agent.rejection_threshold
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"status": "error", "message": str(e)}


def main():
    """Main function for testing the system"""
    try:
        # Initialize system
        system = MultibaggerResearchSystem()
        
        # Get system status
        status = system.get_system_status()
        print("System Status:")
        print(json.dumps(status, indent=2))
        
        # Test with a few known stocks
        test_stocks = ['TANLA.NS', 'DIXON.NS', 'TRENT.NS']
        
        print(f"\nTesting with stocks: {test_stocks}")
        
        # Run discovery
        results = system.discover_multibaggers(test_stocks)
        
        # Print results summary
        print("\n" + "="*50)
        print("MULTIBAGGER DISCOVERY RESULTS")
        print("="*50)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            return
        
        print(f"\nHigh Probability Multibaggers: {len(results.get('high_probability_multibaggers', []))}")
        for stock in results.get('high_probability_multibaggers', []):
            print(f"  {stock['symbol']} - {stock['multibagger_probability']:.3f} - {stock['agent_consensus']}")
        
        print(f"\nEarly Watchlist: {len(results.get('early_watchlist', []))}")
        for stock in results.get('early_watchlist', []):
            print(f"  {stock['symbol']} - {stock['multibagger_probability']:.3f} - {stock['agent_consensus']}")
        
        print(f"\nAnalysis Summary:")
        summary = results.get('analysis_summary', {})
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()