import streamlit as st
from news_collector import IndiaStockNewsCollector
from ai_analyzer import AINewsAnalyzer
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Page config
st.set_page_config(
    page_title="News Analyzer",
    page_icon="🇮🇳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.impact-high {
    background-color: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
.impact-positive {
    background-color: #d4edda;
    border-left: 5px solid #28a745;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
.impact-negative {
    background-color: #f8d7da;
    border-left: 5px solid #dc3545;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
.sector-badge {
    display: inline-block;
    background-color: #007bff;
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    margin: 5px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'collector' not in st.session_state:
    st.session_state.collector = IndiaStockNewsCollector()

# Header
st.title("🇮🇳 Stock Market News Analyzer")
st.markdown("**AI-Powered Analysis of Indian Stock Market News**")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    
    api_key = os.getenv('API_KEY')
    llm_endpoint = os.getenv('LLM_ENDPOINT')
        
    if not api_key:
        st.warning("⚠️ Please enter API key to use AI analysis")
    
    st.markdown("---")
    
    # Fetch settings
    st.subheader("📰 Fetch Settings")
    articles_per_source = 15 #st.slider("Articles per source", 5, 30, 15)
    
    # Analyze button
    analyze_btn = st.button("🔍 Fetch & Analyze News", type="primary", use_container_width=True)
    
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Sources info
    st.subheader("📡 News Sources")
    st.caption("""
    • MoneyControl
    • Economic Times
    • Business Standard
    • LiveMint
    • NDTV Profit
    • Reuters India
    """)
    
    st.markdown("---")
    st.caption("Made with ❤️ for Indian Markets")

# Main Analysis Logic
if analyze_btn:
    if not api_key:
        st.error("❌ Please provide API Key in sidebar to proceed")
        st.stop()
    
    # Initialize AI analyzer
    analyzer = AINewsAnalyzer(api_key, llm_endpoint)
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Fetch News
        status_text.text("📡 Fetching news from Indian financial sources...")
        progress_bar.progress(30)
        
        news = st.session_state.collector.fetch_news(articles_per_source)
        
        if not news:
            st.error("❌ No news fetched. Please check your internet connection.")
            st.stop()
        
        st.session_state.news = news
        
        # Step 2: AI Analysis
        status_text.text("🤖 Analyzing news with AI...")
        progress_bar.progress(60)
        
        analysis = analyzer.analyze_news(news)
        categories = analyzer.categorize_by_impact(news, analysis)
        
        st.session_state.analysis = analysis
        st.session_state.categories = categories
        st.session_state.last_updated = datetime.now()
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # Clear progress
        import time
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"✅ Successfully analyzed {len(news)} articles!")
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.stop()

# Display Results
if 'analysis' in st.session_state:
    
    analysis = st.session_state.analysis
    categories = st.session_state.categories
    news = st.session_state.news
    
    # Last updated timestamp
    st.caption(f"🕒 Last updated: {st.session_state.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    
    # Market Impact Overview
    st.subheader("📊 Market Impact Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        impact_color = "🟢" if analysis['market_impact'] == "Positive" else "🔴" if analysis['market_impact'] == "Negative" else "🟡"
        st.metric("Market Impact", f"{impact_color} {analysis['market_impact']}")
    
    with col2:
        sentiment = analysis['sentiment_score']
        sentiment_emoji = "😊" if sentiment >= 7 else "😐" if sentiment >= 4 else "😟"
        st.metric("Sentiment Score", f"{sentiment_emoji} {sentiment}/10")
    
    with col3:
        st.metric("Total News", len(news))
    
    with col4:
        st.metric("High Impact", len(categories['high_impact']))
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Summary", "⚠️ High Impact", "📈 Categories", "📰 All News"])
    
    # ==================== TAB 1: AI SUMMARY ====================
    with tab1:
        st.markdown("### 🤖 AI-Generated Market Analysis")
        
        # Market Impact Box
        if analysis['market_impact'] == "Positive":
            st.markdown(f'<div class="impact-positive"><h4>📈 {analysis["market_impact"]} Market Outlook</h4></div>', unsafe_allow_html=True)
        elif analysis['market_impact'] == "Negative":
            st.markdown(f'<div class="impact-negative"><h4>📉 {analysis["market_impact"]} Market Outlook</h4></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="impact-high"><h4>➡️ {analysis["market_impact"]} Market Outlook</h4></div>', unsafe_allow_html=True)
        
        # Executive Summary
        st.markdown("#### 📝 Executive Summary")
        st.info(analysis['summary'])
        
        # Affected Sectors
        if analysis['affected_sectors']:
            st.markdown("#### 🏭 Affected Sectors")
            sector_html = ""
            for sector in analysis['affected_sectors']:
                sector_html += f'<span class="sector-badge">{sector}</span>'
            st.markdown(sector_html, unsafe_allow_html=True)
        
        # Specific Stocks to Watch
        if analysis['specific_stocks']:
            st.markdown("#### 📊 Stocks to Watch")
            stock_cols = st.columns(min(len(analysis['specific_stocks']), 4))
            for idx, stock in enumerate(analysis['specific_stocks'][:8]):
                with stock_cols[idx % 4]:
                    st.success(f"**{stock}**")
        
        # Key Insights
        st.markdown("#### 💡 Key Insights for Investors")
        for idx, insight in enumerate(analysis['key_insights'], 1):
            st.markdown(f"**{idx}.** {insight}")
        
        # Detailed Analysis
        st.markdown("#### 📄 Detailed Market Analysis")
        st.markdown(analysis['detailed_analysis'])
        
        # Sentiment Gauge Visualization
        st.markdown("#### 🎯 Market Sentiment Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=analysis['sentiment_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Market Sentiment", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 3], 'color': "#ffcccc", 'name': 'Bearish'},
                    {'range': [3, 7], 'color': "#ffffcc", 'name': 'Neutral'},
                    {'range': [7, 10], 'color': "#ccffcc", 'name': 'Bullish'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 5
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Download Analysis Report
        st.markdown("---")
        summary_text = f"""# BSE/NSE Market Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Market Impact: {analysis['market_impact']}
## Sentiment Score: {analysis['sentiment_score']}/10

## Executive Summary
{analysis['summary']}

## Affected Sectors
{', '.join(analysis['affected_sectors']) if analysis['affected_sectors'] else 'None identified'}

## Stocks to Watch
{', '.join(analysis['specific_stocks']) if analysis['specific_stocks'] else 'None identified'}

## Key Insights
{chr(10).join([f"{i}. {insight}" for i, insight in enumerate(analysis['key_insights'], 1)])}

## Detailed Analysis
{analysis['detailed_analysis']}

---
Total Articles Analyzed: {len(news)}
High Impact News: {len(categories['high_impact'])}
"""
        st.download_button(
            "📥 Download Full Analysis Report",
            summary_text,
            f"BSE_NSE_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    # ==================== TAB 2: HIGH IMPACT NEWS ====================
    with tab2:
        st.markdown("### ⚠️ High Impact News for BSE/NSE Markets")
        st.info("News items that could significantly affect Indian stock market movements")
        
        high_impact_news = categories['high_impact']
        
        if high_impact_news:
            for idx, news_item in enumerate(high_impact_news, 1):
                st.markdown(f"""
                <div class="impact-high">
                    <h4>{idx}. <a href="{news_item['link']}" target="_blank">{news_item['title']}</a></h4>
                    <p>{news_item['description']}</p>
                    <small><strong>Source:</strong> {news_item['source']} | <strong>Published:</strong> {news_item['published'].strftime('%Y-%m-%d %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No high impact news detected in current batch")
        
        # Company-Specific News Section
        st.markdown("---")
        st.markdown("### 🏢 Company-Specific News")
        
        company_news = categories['company_specific']
        if company_news:
            for news_item in company_news[:10]:
                with st.expander(news_item['title']):
                    st.markdown(f"**Source:** {news_item['source']}")
                    st.markdown(f"**Published:** {news_item['published'].strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Description:** {news_item['description']}")
                    st.markdown(f"[Read Full Article]({news_item['link']})")
        else:
            st.info("No company-specific news found in current batch")
    
    # ==================== TAB 3: BY CATEGORY ====================
    with tab3:
        st.markdown("### 📈 News Categorized by Market Impact")
        
        # Category Distribution Chart
        cat_data = {
            'High Impact': len(categories['high_impact']),
            'Sector Specific': len(categories['sector_specific']),
            'Company Specific': len(categories['company_specific']),
            'General Market': len(categories['general'])
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(cat_data.keys()),
                y=list(cat_data.values()),
                marker_color=['#ffc107', '#007bff', '#28a745', '#6c757d'],
                text=list(cat_data.values()),
                textposition='auto',
            )
        ])
        fig.update_layout(
            title="News Distribution by Impact Category",
            xaxis_title="Category",
            yaxis_title="Number of Articles",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display news by category
        st.markdown("---")
        
        categories_info = {
            'high_impact': {
                'title': '⚠️ High Impact News',
                'desc': 'News affecting overall BSE/NSE market (RBI, SEBI, Government policies, GDP, etc.)',
                'color': 'warning'
            },
            'sector_specific': {
                'title': '🏭 Sector-Specific News',
                'desc': 'News affecting specific sectors (IT, Banking, Pharma, Auto, etc.)',
                'color': 'info'
            },
            'company_specific': {
                'title': '🏢 Company-Specific News',
                'desc': 'News about individual listed companies',
                'color': 'success'
            },
            'general': {
                'title': '📰 General Market News',
                'desc': 'Other market-related news and updates',
                'color': 'secondary'
            }
        }
        
        for cat_key, cat_info in categories_info.items():
            if categories[cat_key]:
                with st.expander(f"{cat_info['title']} ({len(categories[cat_key])} articles)", expanded=(cat_key=='high_impact')):
                    st.caption(cat_info['desc'])
                    for news_item in categories[cat_key]:
                        st.markdown(f"**[{news_item['title']}]({news_item['link']})**")
                        st.caption(f"{news_item['description'][:250]}...")
                        st.caption(f"📰 {news_item['source']} | 🕒 {news_item['published'].strftime('%Y-%m-%d %H:%M')}")
                    st.markdown("---")
        
        # ==================== TAB 4: ALL NEWS ====================
    with tab4:
        st.markdown("### 📰 All News Articles")
        
        # Search and filter controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search news", placeholder="Enter keywords to filter news...")
        
        with col2:
            source_filter = st.selectbox(
                "Filter by source",
                ["All Sources"] + sorted(list(set([n['source'] for n in news])))
            )
        
        # Apply filters
        filtered_news = news
        
        if search_query:
            filtered_news = [
                n for n in filtered_news 
                if search_query.lower() in n['title'].lower() or search_query.lower() in n['description'].lower()
            ]
        
        if source_filter != "All Sources":
            filtered_news = [n for n in filtered_news if n['source'] == source_filter]
        
        # Display count
        st.info(f"📄 Showing {len(filtered_news)} of {len(news)} articles")
        
        # Display all filtered news
        for idx, news_item in enumerate(filtered_news, 1):
            with st.container():
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"**{idx}. [{news_item['title']}]({news_item['link']})**")
                    st.caption(news_item['description'])
                    st.caption(f"📰 {news_item['source']} | 🕒 {news_item['published'].strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    # Category badge
                    if news_item in categories['high_impact']:
                        st.warning("⚠️ High")
                    elif news_item in categories['sector_specific']:
                        st.info("🏭 Sector")
                    elif news_item in categories['company_specific']:
                        st.success("🏢 Stock")
                    else:
                        st.caption("📰 General")
                
                st.markdown("---")
        
        # Export options
        st.markdown("### 📥 Export News Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as CSV
            df = pd.DataFrame(filtered_news)
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📊 Download as CSV",
                data=csv_data,
                file_name=f"BSE_NSE_News_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Export as JSON
            json_data = json.dumps(filtered_news, indent=2, default=str)
            st.download_button(
                label="📋 Download as JSON",
                data=json_data,
                file_name=f"BSE_NSE_News_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )