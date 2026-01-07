"""
Streamlit Web Interface for Multi-Agent AI Research System
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import logging

# Import the main system
from main_system import MultibaggerResearchSystem

# Configure page
st.set_page_config(
    page_title="AI Multibagger Research System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stock-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .high-conviction {
        border-left: 4px solid #28a745;
    }
    .medium-conviction {
        border-left: 4px solid #ffc107;
    }
    .low-conviction {
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'analysis_running' not in st.session_state:
    st.session_state.analysis_running = False

def initialize_system():
    """Initialize the research system"""
    try:
        with st.spinner("Initializing AI Research System..."):
            system = MultibaggerResearchSystem()
            st.session_state.system = system
            st.success("✅ System initialized successfully!")
            return True
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {e}")
        return False

def display_system_status():
    """Display system status in sidebar"""
    if st.session_state.system:
        status = st.session_state.system.get_system_status()
        
        st.sidebar.markdown("### 🔧 System Status")
        st.sidebar.success("🟢 Operational")
        
        with st.sidebar.expander("Agent Details"):
            for agent_name, agent_class in status.get('agents', {}).items():
                st.write(f"**{agent_name.replace('_', ' ').title()}**")
                st.write(f"Status: ✅ Active")
        
        with st.sidebar.expander("Configuration"):
            st.write("**Agent Weights:**")
            weights = status.get('agent_weights', {})
            for agent, weight in weights.items():
                st.write(f"- {agent.title()}: {weight:.1%}")
            
            st.write("**Thresholds:**")
            thresholds = status.get('thresholds', {})
            for threshold, value in thresholds.items():
                st.write(f"- {threshold.replace('_', ' ').title()}: {value:.1%}")

def run_analysis(stock_symbols):
    """Run the multibagger analysis"""
    try:
        st.session_state.analysis_running = True
        
        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        status_text.text("🔍 Fetching stock data...")
        progress_bar.progress(20)
        
        # Run analysis
        status_text.text("🤖 Running AI agent analysis...")
        progress_bar.progress(60)
        
        results = st.session_state.system.discover_multibaggers(stock_symbols)
        
        status_text.text("📊 Synthesizing results...")
        progress_bar.progress(90)
        
        # Store results
        st.session_state.results = results
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed!")
        
        st.session_state.analysis_running = False
        return True
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {e}")
        st.session_state.analysis_running = False
        return False

def display_results():
    """Display analysis results"""
    if not st.session_state.results:
        return
    
    results = st.session_state.results
    
    if "error" in results:
        st.error(f"Analysis Error: {results['error']}")
        return
    
    # Summary metrics
    st.markdown("## 📊 Analysis Summary")
    
    summary = results.get('analysis_summary', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Analyzed", 
            summary.get('total_stocks_analyzed', 0)
        )
    
    with col2:
        st.metric(
            "High Conviction", 
            summary.get('high_conviction_count', 0),
            delta=f"{summary.get('high_conviction_count', 0)} stocks"
        )
    
    with col3:
        st.metric(
            "Watchlist", 
            summary.get('watchlist_count', 0),
            delta=f"{summary.get('watchlist_count', 0)} stocks"
        )
    
    with col4:
        st.metric(
            "Rejected", 
            summary.get('rejected_count', 0),
            delta=f"{summary.get('rejected_count', 0)} stocks"
        )
    
    # High Probability Multibaggers
    st.markdown("## 🚀 High Probability Multibaggers")
    
    high_conviction = results.get('high_probability_multibaggers', [])
    
    if high_conviction:
        for stock in high_conviction:
            display_stock_card(stock, "high-conviction")
    else:
        st.info("No high conviction multibaggers found in current analysis.")
    
    # Early Watchlist
    st.markdown("## 👀 Early Watchlist")
    
    watchlist = results.get('early_watchlist', [])
    
    if watchlist:
        for stock in watchlist:
            display_stock_card(stock, "medium-conviction")
    else:
        st.info("No watchlist stocks found in current analysis.")
    
    # Analysis Charts
    display_analysis_charts(results)

def display_stock_card(stock, conviction_class):
    """Display individual stock analysis card"""
    
    st.markdown(f"""
    <div class="stock-card {conviction_class}">
        <h3>{stock['symbol']} - {stock['sector']}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <strong>Probability: {stock['multibagger_probability']:.1%}</strong><br>
                <span style="color: #666;">Market Cap: {stock['market_cap']}</span>
            </div>
            <div style="text-align: right;">
                <span style="background-color: #e3f2fd; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.8rem;">
                    {stock['agent_consensus']}
                </span><br>
                <span style="color: #666; font-size: 0.9rem;">Expected: {stock['expected_timeframe']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expandable details
    with st.expander(f"📋 Detailed Analysis - {stock['symbol']}"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Key Triggers:**")
            for trigger in stock.get('key_triggers', []):
                st.write(f"• {trigger}")
            
            st.markdown("**📊 Detailed Scores:**")
            scores = stock.get('detailed_scores', {})
            for score_name, score_value in scores.items():
                if isinstance(score_value, (int, float)):
                    st.write(f"• {score_name.replace('_', ' ').title()}: {score_value}")
                else:
                    st.write(f"• {score_name.replace('_', ' ').title()}: {score_value}")
        
        with col2:
            st.markdown("**⚠️ Major Risks:**")
            for risk in stock.get('major_risks', []):
                st.write(f"• {risk}")
            
            # Score visualization
            if 'detailed_scores' in stock:
                scores = stock['detailed_scores']
                score_data = []
                
                for key, value in scores.items():
                    if isinstance(value, (int, float)):
                        score_data.append({
                            'Metric': key.replace('_', ' ').title(),
                            'Score': value
                        })
                
                if score_data:
                    df_scores = pd.DataFrame(score_data)
                    fig = px.bar(
                        df_scores, 
                        x='Score', 
                        y='Metric',
                        orientation='h',
                        title=f"Score Breakdown - {stock['symbol']}"
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

def display_analysis_charts(results):
    """Display analysis visualization charts"""
    
    st.markdown("## 📈 Analysis Visualization")
    
    # Combine all stocks for visualization
    all_stocks = (
        results.get('high_probability_multibaggers', []) +
        results.get('early_watchlist', []) +
        results.get('rejected_stocks', [])[:5]  # Top 5 rejected
    )
    
    if not all_stocks:
        st.info("No data available for visualization.")
        return
    
    # Create DataFrame for visualization
    viz_data = []
    for stock in all_stocks:
        category = "High Conviction" if stock in results.get('high_probability_multibaggers', []) else \
                  "Watchlist" if stock in results.get('early_watchlist', []) else "Rejected"
        
        viz_data.append({
            'Symbol': stock['symbol'],
            'Sector': stock['sector'],
            'Probability': stock['multibagger_probability'],
            'Category': category,
            'Market_Cap': stock['market_cap']
        })
    
    df_viz = pd.DataFrame(viz_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Probability distribution
        fig1 = px.scatter(
            df_viz,
            x='Symbol',
            y='Probability',
            color='Category',
            size='Probability',
            hover_data=['Sector', 'Market_Cap'],
            title="Multibagger Probability by Stock"
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Sector distribution
        sector_counts = df_viz['Sector'].value_counts()
        fig2 = px.pie(
            values=sector_counts.values,
            names=sector_counts.index,
            title="Sector Distribution"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 AI Multibagger Research System</h1>', unsafe_allow_html=True)
    st.markdown("**Discover high-probability Indian multibagger stocks using Multi-Agent AI analysis**")
    
    # Sidebar
    st.sidebar.markdown("# 🎛️ Control Panel")
    
    # Initialize system
    if st.session_state.system is None:
        if st.sidebar.button("🚀 Initialize System", type="primary"):
            initialize_system()
    else:
        display_system_status()
        
        st.sidebar.markdown("---")
        
        # Analysis controls
        st.sidebar.markdown("### 📊 Run Analysis")
        
        analysis_type = st.sidebar.radio(
            "Analysis Type:",
            ["Predefined Stocks", "Custom Stocks", "Single Stock"]
        )
        
        stock_symbols = []
        
        if analysis_type == "Predefined Stocks":
            st.sidebar.info("Using historical multibagger stocks for testing")
            stock_symbols = ['TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS']
        
        elif analysis_type == "Custom Stocks":
            custom_stocks = st.sidebar.text_area(
                "Enter stock symbols (one per line):",
                placeholder="RELIANCE.NS\nTCS.NS\nINFY.NS"
            )
            if custom_stocks:
                stock_symbols = [s.strip() for s in custom_stocks.split('\n') if s.strip()]
        
        elif analysis_type == "Single Stock":
            single_stock = st.sidebar.text_input(
                "Enter stock symbol:",
                placeholder="RELIANCE.NS"
            )
            if single_stock:
                stock_symbols = [single_stock.strip()]
        
        # Run analysis button
        if stock_symbols and not st.session_state.analysis_running:
            if st.sidebar.button("🔍 Run Analysis", type="primary"):
                if analysis_type == "Single Stock":
                    # Single stock analysis
                    with st.spinner("Analyzing stock..."):
                        results = st.session_state.system.analyze_single_stock(stock_symbols[0])
                        st.session_state.results = results
                else:
                    # Multi-stock analysis
                    run_analysis(stock_symbols)
        
        elif st.session_state.analysis_running:
            st.sidebar.warning("⏳ Analysis in progress...")
        
        # Clear results
        if st.sidebar.button("🗑️ Clear Results"):
            st.session_state.results = None
            st.rerun()
    
    # Main content area
    if st.session_state.system is None:
        st.info("👆 Please initialize the system using the sidebar to begin analysis.")
        
        # System overview
        st.markdown("## 🧠 System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🔍 Fundamental Agent**
            - Revenue & profit growth analysis
            - Margin expansion detection
            - Capital efficiency metrics
            - Cash flow quality assessment
            """)
        
        with col2:
            st.markdown("""
            **👥 Management Agent**
            - Promoter holding analysis
            - Governance quality assessment
            - Management track record
            - Minority shareholder alignment
            """)
        
        with col3:
            st.markdown("""
            **📈 Technical Agent**
            - Base formation patterns
            - Breakout confirmation
            - Relative strength analysis
            - Volume expansion detection
            """)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            **💰 Smart Money Agent**
            - FII/DII flow tracking
            - Mutual fund accumulation
            - Bulk deal analysis
            - PE/VC investor presence
            """)
        
        with col5:
            st.markdown("""
            **🏛️ Policy Agent**
            - Government scheme mapping
            - Sector policy analysis
            - PSU reform benefits
            - Capex cycle alignment
            """)
        
        with col6:
            st.markdown("""
            **🎯 Supervisor Agent**
            - Multi-agent synthesis
            - Weighted scoring system
            - Risk-reward assessment
            - Final ranking & categorization
            """)
    
    else:
        # Display results if available
        if st.session_state.results:
            display_results()
        else:
            st.info("👆 Configure analysis parameters in the sidebar and click 'Run Analysis' to discover multibaggers.")
            
            # Show sample results format
            st.markdown("## 📋 Expected Output Format")
            
            sample_output = {
                "high_probability_multibaggers": [
                    {
                        "symbol": "EXAMPLE.NS",
                        "sector": "Technology",
                        "market_cap": "₹5,000 Cr",
                        "multibagger_probability": 0.85,
                        "expected_timeframe": "3-5 years",
                        "key_triggers": ["Revenue growth acceleration", "Margin expansion", "Smart money accumulation"],
                        "major_risks": ["Market volatility", "Execution risk"],
                        "agent_consensus": "STRONG BUY (High Conviction)"
                    }
                ],
                "early_watchlist": [],
                "rejected_stocks": []
            }
            
            st.json(sample_output)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>⚠️ <strong>Disclaimer:</strong> This system is for research and educational purposes only. 
        Not financial advice. Always do your own research before making investment decisions.</p>
        <p>Built with ❤️ using Multi-Agent AI Architecture</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()