
import streamlit as st
import yfinance as yf
import pandas as pd
import json
from datetime import datetime

# Page Config
st.set_page_config(page_title="Complete Stock Data Viewer", page_icon="📊", layout="wide")

# CSS
st.markdown("""
    <style>
    .stApp {background-color: #f5f5f5;}
    .data-section {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Complete Stock Data Viewer")
st.markdown("*Fetch and display ALL available data from yfinance*")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Settings")

stocks = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "SBIN": "SBIN.NS",
    "WIPRO": "WIPRO.NS",
    "ITC": "ITC.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "ADANIENT": "ADANIENT.NS"
}

stock_name = st.sidebar.selectbox("🎯 Select Stock", list(stocks.keys()))
stock_symbol = stocks[stock_name]

# Fetch options
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Data to Fetch")

fetch_basic = st.sidebar.checkbox("Basic Info", value=True)
fetch_price = st.sidebar.checkbox("Price Data", value=True)
fetch_financial = st.sidebar.checkbox("Financial Data", value=True)
fetch_statements = st.sidebar.checkbox("Financial Statements", value=False)
fetch_holders = st.sidebar.checkbox("Shareholders", value=False)
fetch_dividends = st.sidebar.checkbox("Dividends & Splits", value=False)
fetch_recommendations = st.sidebar.checkbox("Analyst Recommendations", value=False)
fetch_calendar = st.sidebar.checkbox("Earnings Calendar", value=False)
fetch_options = st.sidebar.checkbox("Options Data", value=False)
fetch_news = st.sidebar.checkbox("Latest News", value=False)

# Download option
download_json = st.sidebar.checkbox("📄 Enable JSON Download", value=False)

# Fetch button
if st.sidebar.button("🔄 Fetch All Data", type="primary"):
    
    with st.spinner(f"Fetching complete data for {stock_name}..."):
        try:
            # Initialize stock
            stock = yf.Ticker(stock_symbol)
            
            # Master data dictionary
            all_data = {
                "symbol": stock_symbol,
                "company_name": stock_name,
                "fetch_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": {}
            }
            
            # =========================
            # 1. BASIC INFORMATION
            # =========================
            if fetch_basic:
                st.markdown("## 🏢 Basic Company Information")
                
                info = stock.info
                
                basic_data = {
                    "Company Name": info.get('longName', 'N/A'),
                    "Symbol": info.get('symbol', 'N/A'),
                    "Sector": info.get('sector', 'N/A'),
                    "Industry": info.get('industry', 'N/A'),
                    "Website": info.get('website', 'N/A'),
                    "Country": info.get('country', 'N/A'),
                    "City": info.get('city', 'N/A'),
                    "Phone": info.get('phone', 'N/A'),
                    "Full Time Employees": info.get('fullTimeEmployees', 'N/A'),
                    "Exchange": info.get('exchange', 'N/A'),
                    "Currency": info.get('currency', 'N/A'),
                    "Timezone": info.get('timeZoneFullName', 'N/A'),
                    "ISIN": info.get('isin', 'N/A')
                }
                
                col1, col2 = st.columns(2)
                with col1:
                    for key, value in list(basic_data.items())[:7]:
                        st.write(f"**{key}:** {value}")
                with col2:
                    for key, value in list(basic_data.items())[7:]:
                        st.write(f"**{key}:** {value}")
                
                # Business Summary
                st.markdown("### 📝 Business Summary")
                st.write(info.get('longBusinessSummary', 'N/A'))
                
                all_data["data"]["basic_info"] = basic_data
                all_data["data"]["business_summary"] = info.get('longBusinessSummary', 'N/A')
                
                st.markdown("---")
            
            # =========================
            # 2. PRICE DATA
            # =========================
            if fetch_price:
                st.markdown("## 💰 Price & Market Data")
                
                info = stock.info
                
                price_data = {
                    "Current Price": f"₹{info.get('currentPrice', 'N/A')}",
                    "Previous Close": f"₹{info.get('previousClose', 'N/A')}",
                    "Open": f"₹{info.get('open', 'N/A')}",
                    "Day Low": f"₹{info.get('dayLow', 'N/A')}",
                    "Day High": f"₹{info.get('dayHigh', 'N/A')}",
                    "52 Week Low": f"₹{info.get('fiftyTwoWeekLow', 'N/A')}",
                    "52 Week High": f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}",
                    "50 Day Average": f"₹{info.get('fiftyDayAverage', 'N/A')}",
                    "200 Day Average": f"₹{info.get('twoHundredDayAverage', 'N/A')}",
                    "Volume": info.get('volume', 'N/A'),
                    "Average Volume": info.get('averageVolume', 'N/A'),
                    "Market Cap": f"₹{info.get('marketCap', 0)/10000000:.2f} Cr" if info.get('marketCap') else 'N/A',
                    "Bid": f"₹{info.get('bid', 'N/A')}",
                    "Ask": f"₹{info.get('ask', 'N/A')}",
                    "Bid Size": info.get('bidSize', 'N/A'),
                    "Ask Size": info.get('askSize', 'N/A')
                }
                
                col1, col2, col3, col4 = st.columns(4)
                items = list(price_data.items())
                chunk_size = len(items) // 4 + 1
                
                with col1:
                    for key, value in items[:chunk_size]:
                        st.metric(key, value)
                with col2:
                    for key, value in items[chunk_size:chunk_size*2]:
                        st.metric(key, value)
                with col3:
                    for key, value in items[chunk_size*2:chunk_size*3]:
                        st.metric(key, value)
                with col4:
                    for key, value in items[chunk_size*3:]:
                        st.metric(key, value)
                
                all_data["data"]["price_data"] = price_data
                
                st.markdown("---")
            
            # =========================
            # 3. FINANCIAL DATA
            # =========================
            if fetch_financial:
                st.markdown("## 📊 Financial Ratios & Metrics")
                
                info = stock.info
                
                financial_data = {
                    "P/E Ratio (Trailing)": info.get('trailingPE', 'N/A'),
                    "P/E Ratio (Forward)": info.get('forwardPE', 'N/A'),
                    "PEG Ratio": info.get('pegRatio', 'N/A'),
                    "Price to Book": info.get('priceToBook', 'N/A'),
                    "Price to Sales": info.get('priceToSalesTrailing12Months', 'N/A'),
                    "EV to Revenue": info.get('enterpriseToRevenue', 'N/A'),
                    "EV to EBITDA": info.get('enterpriseToEbitda', 'N/A'),
                    "Enterprise Value": f"₹{info.get('enterpriseValue', 0)/10000000:.2f} Cr" if info.get('enterpriseValue') else 'N/A',
                    "Profit Margin": f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else 'N/A',
                    "Operating Margin": f"{info.get('operatingMargins', 0)*100:.2f}%" if info.get('operatingMargins') else 'N/A',
                    "Gross Margin": f"{info.get('grossMargins', 0)*100:.2f}%" if info.get('grossMargins') else 'N/A',
                    "ROA (Return on Assets)": f"{info.get('returnOnAssets', 0)*100:.2f}%" if info.get('returnOnAssets') else 'N/A',
                    "ROE (Return on Equity)": f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else 'N/A',
                    "Revenue": f"₹{info.get('totalRevenue', 0)/10000000:.2f} Cr" if info.get('totalRevenue') else 'N/A',
                    "Revenue Per Share": info.get('revenuePerShare', 'N/A'),
                    "EBITDA": f"₹{info.get('ebitda', 0)/10000000:.2f} Cr" if info.get('ebitda') else 'N/A',
                    "Debt to Equity": info.get('debtToEquity', 'N/A'),
                    "Current Ratio": info.get('currentRatio', 'N/A'),
                    "Quick Ratio": info.get('quickRatio', 'N/A'),
                    "Book Value": info.get('bookValue', 'N/A'),
                    "EPS (Trailing)": info.get('trailingEps', 'N/A'),
                    "EPS (Forward)": info.get('forwardEps', 'N/A'),
                    "Total Cash": f"₹{info.get('totalCash', 0)/10000000:.2f} Cr" if info.get('totalCash') else 'N/A',
                    "Total Debt": f"₹{info.get('totalDebt', 0)/10000000:.2f} Cr" if info.get('totalDebt') else 'N/A',
                    "Beta": info.get('beta', 'N/A'),
                    "Shares Outstanding": info.get('sharesOutstanding', 'N/A'),
                }
                
                # Display in tabs
                tab1, tab2, tab3 = st.tabs(["📈 Valuation", "💹 Profitability", "⚖️ Financial Health"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    valuation_metrics = ["P/E Ratio (Trailing)", "P/E Ratio (Forward)", "PEG Ratio", 
                                        "Price to Book", "Price to Sales", "EV to Revenue", "EV to EBITDA", "Enterprise Value"]
                    with col1:
                        for key in valuation_metrics[:4]:
                            st.write(f"**{key}:** {financial_data[key]}")
                    with col2:
                        for key in valuation_metrics[4:]:
                            st.write(f"**{key}:** {financial_data[key]}")
                
                with tab2:
                    col1, col2 = st.columns(2)
                    profit_metrics = ["Profit Margin", "Operating Margin", "Gross Margin", 
                                     "ROA (Return on Assets)", "ROE (Return on Equity)", 
                                     "Revenue", "Revenue Per Share", "EBITDA", "EPS (Trailing)", "EPS (Forward)"]
                    with col1:
                        for key in profit_metrics[:5]:
                            st.write(f"**{key}:** {financial_data[key]}")
                    with col2:
                        for key in profit_metrics[5:]:
                            st.write(f"**{key}:** {financial_data[key]}")
                
                with tab3:
                    col1, col2 = st.columns(2)
                    health_metrics = ["Debt to Equity", "Current Ratio", "Quick Ratio", 
                                     "Total Cash", "Total Debt", "Book Value", "Beta", "Shares Outstanding"]
                    with col1:
                        for key in health_metrics[:4]:
                            st.write(f"**{key}:** {financial_data[key]}")
                    with col2:
                        for key in health_metrics[4:]:
                            st.write(f"**{key}:** {financial_data[key]}")
                
                all_data["data"]["financial_metrics"] = financial_data
                
                st.markdown("---")
            
            # =========================
            # 4. FINANCIAL STATEMENTS
            # =========================
            if fetch_statements:
                st.markdown("## 📋 Financial Statements")
                
                tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
                
                with tab1:
                    st.markdown("### Annual Income Statement")
                    try:
                        financials = stock.financials
                        if financials is not None and not financials.empty:
                            st.dataframe(financials, use_container_width=True)
                            all_data["data"]["income_statement_annual"] = financials.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching income statement")
                    
                    st.markdown("### Quarterly Income Statement")
                    try:
                        quarterly_financials = stock.quarterly_financials
                        if quarterly_financials is not None and not quarterly_financials.empty:
                            st.dataframe(quarterly_financials, use_container_width=True)
                            all_data["data"]["income_statement_quarterly"] = quarterly_financials.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching quarterly income statement")
                
                with tab2:
                    st.markdown("### Annual Balance Sheet")
                    try:
                        balance_sheet = stock.balance_sheet
                        if balance_sheet is not None and not balance_sheet.empty:
                            st.dataframe(balance_sheet, use_container_width=True)
                            all_data["data"]["balance_sheet_annual"] = balance_sheet.to_dict()
                        else:
                            st.info("No data available")
                
                    except:
                        st.error("Error fetching balance sheet")
                    
                    st.markdown("### Quarterly Balance Sheet")
                    try:
                        quarterly_balance = stock.quarterly_balance_sheet
                        if quarterly_balance is not None and not quarterly_balance.empty:
                            st.dataframe(quarterly_balance, use_container_width=True)
                            all_data["data"]["balance_sheet_quarterly"] = quarterly_balance.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching quarterly balance sheet")
                
                with tab3:
                    st.markdown("### Annual Cash Flow")
                    try:
                        cashflow = stock.cashflow
                        if cashflow is not None and not cashflow.empty:
                            st.dataframe(cashflow, use_container_width=True)
                            all_data["data"]["cashflow_annual"] = cashflow.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching cash flow")
                    
                    st.markdown("### Quarterly Cash Flow")
                    try:
                        quarterly_cashflow = stock.quarterly_cashflow
                        if quarterly_cashflow is not None and not quarterly_cashflow.empty:
                            st.dataframe(quarterly_cashflow, use_container_width=True)
                            all_data["data"]["cashflow_quarterly"] = quarterly_cashflow.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching quarterly cash flow")
                
                st.markdown("---")
            
            # =========================
            # 5. SHAREHOLDERS DATA
            # =========================
            if fetch_holders:
                st.markdown("## 👥 Shareholders & Ownership")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Major Holders")
                    try:
                        major_holders = stock.major_holders
                        if major_holders is not None and not major_holders.empty:
                            st.dataframe(major_holders, use_container_width=True)
                            all_data["data"]["major_holders"] = major_holders.to_dict()
                        else:
                            st.info("No data available")
                    except:
                        st.error("Error fetching major holders")
                
                with col2:
                    info = stock.info
                    st.markdown("### Ownership Details")
                    st.write(f"**% Held by Insiders:** {info.get('heldPercentInsiders', 'N/A')}")
                    st.write(f"**% Held by Institutions:** {info.get('heldPercentInstitutions', 'N/A')}")
                    st.write(f"**Float Shares:** {info.get('floatShares', 'N/A')}")
                    st.write(f"**Shares Outstanding:** {info.get('sharesOutstanding', 'N/A')}")
                
                st.markdown("### Institutional Holders")
                try:
                    institutional = stock.institutional_holders
                    if institutional is not None and not institutional.empty:
                        st.dataframe(institutional, use_container_width=True)
                        all_data["data"]["institutional_holders"] = institutional.to_dict()
                    else:
                        st.info("No data available")
                except:
                    st.error("Error fetching institutional holders")
                
                st.markdown("### Mutual Fund Holders")
                try:
                    mutualfund = stock.mutualfund_holders
                    if mutualfund is not None and not mutualfund.empty:
                        st.dataframe(mutualfund, use_container_width=True)
                        all_data["data"]["mutualfund_holders"] = mutualfund.to_dict()
                    else:
                        st.info("No data available")
                except:
                    st.error("Error fetching mutual fund holders")
                
                st.markdown("---")
            
            # =========================
            # 6. DIVIDENDS & SPLITS
            # =========================
            if fetch_dividends:
                st.markdown("## 💵 Dividends & Stock Splits")
                
                info = stock.info
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Dividend Information")
                    dividend_info = {
                        "Dividend Rate": info.get('dividendRate', 'N/A'),
                        "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A',
                        "Payout Ratio": f"{info.get('payoutRatio', 0)*100:.2f}%" if info.get('payoutRatio') else 'N/A',
                        "5 Year Avg Dividend Yield": info.get('fiveYearAvgDividendYield', 'N/A'),
                        "Ex-Dividend Date": info.get('exDividendDate', 'N/A'),
                        "Last Dividend Value": info.get('lastDividendValue', 'N/A'),
                    }
                    for key, value in dividend_info.items():
                        st.write(f"**{key}:** {value}")
                    
                    all_data["data"]["dividend_info"] = dividend_info
                
                with col2:
                    st.markdown("### Dividend History")
                    try:
                        dividends = stock.dividends
                        if dividends is not None and not dividends.empty:
                            st.dataframe(dividends.tail(10), use_container_width=True)
                            all_data["data"]["dividend_history"] = dividends.to_dict()
                        else:
                            st.info("No dividend history available")
                    except:
                        st.error("Error fetching dividend history")
                
                st.markdown("### Stock Split History")
                try:
                    splits = stock.splits
                    if splits is not None and not splits.empty:
                        st.dataframe(splits, use_container_width=True)
                        all_data["data"]["split_history"] = splits.to_dict()
                    else:
                        st.info("No stock split history")
                except:
                    st.error("Error fetching split history")
                
                st.markdown("### All Actions (Dividends + Splits)")
                try:
                    actions = stock.actions
                    if actions is not None and not actions.empty:
                        st.dataframe(actions.tail(20), use_container_width=True)
                        all_data["data"]["actions"] = actions.to_dict()
                    else:
                        st.info("No actions available")
                except:
                    st.error("Error fetching actions")
                
                st.markdown("---")
            
            # =========================
            # 7. ANALYST RECOMMENDATIONS
            # =========================
            if fetch_recommendations:
                st.markdown("## 📊 Analyst Recommendations")
                
                info = stock.info
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Target High Price", f"₹{info.get('targetHighPrice', 'N/A')}")
                    st.metric("Target Mean Price", f"₹{info.get('targetMeanPrice', 'N/A')}")
                
                with col2:
                    st.metric("Target Low Price", f"₹{info.get('targetLowPrice', 'N/A')}")
                    st.metric("Target Median Price", f"₹{info.get('targetMedianPrice', 'N/A')}")
                
                with col3:
                    st.metric("Number of Analysts", info.get('numberOfAnalystOpinions', 'N/A'))
                    recommendation = info.get('recommendationKey', 'N/A')
                    st.metric("Recommendation", recommendation.upper() if recommendation != 'N/A' else 'N/A')
                
                st.markdown("### Recommendation History")
                try:
                    recommendations = stock.recommendations
                    if recommendations is not None and not recommendations.empty:
                        st.dataframe(recommendations.tail(20), use_container_width=True)
                        all_data["data"]["recommendations"] = recommendations.to_dict()
                    else:
                        st.info("No recommendations available")
                except:
                    st.error("Error fetching recommendations")
                
                st.markdown("### Upgrades & Downgrades")
                try:
                    upgrades = stock.upgrades_downgrades
                    if upgrades is not None and not upgrades.empty:
                        st.dataframe(upgrades.tail(20), use_container_width=True)
                        all_data["data"]["upgrades_downgrades"] = upgrades.to_dict()
                    else:
                        st.info("No upgrades/downgrades data")
                except:
                    st.error("Error fetching upgrades/downgrades")
                
                st.markdown("---")
            
            # =========================
            # 8. EARNINGS CALENDAR
            # =========================
            if fetch_calendar:
                st.markdown("## 📅 Earnings & Calendar")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Earnings Calendar")
                    try:
                        calendar = stock.calendar
                        if calendar is not None and not calendar.empty:
                            st.dataframe(calendar, use_container_width=True)
                            all_data["data"]["calendar"] = calendar.to_dict()
                        else:
                            st.info("No calendar data")
                    except:
                        st.error("Error fetching calendar")
                
                with col2:
                    info = stock.info
                    st.markdown("### Key Dates")
                    st.write(f"**Last Fiscal Year End:** {info.get('lastFiscalYearEnd', 'N/A')}")
                    st.write(f"**Next Fiscal Year End:** {info.get('nextFiscalYearEnd', 'N/A')}")
                    st.write(f"**Most Recent Quarter:** {info.get('mostRecentQuarter', 'N/A')}")
                
                st.markdown("### Earnings History")
                try:
                    earnings = stock.earnings
                    if earnings is not None and not earnings.empty:
                        st.dataframe(earnings, use_container_width=True)
                        all_data["data"]["earnings"] = earnings.to_dict()
                    else:
                        st.info("No earnings data")
                except:
                    st.error("Error fetching earnings")
                
                st.markdown("### Quarterly Earnings")
                try:
                    quarterly_earnings = stock.quarterly_earnings
                    if quarterly_earnings is not None and not quarterly_earnings.empty:
                        st.dataframe(quarterly_earnings, use_container_width=True)
                        all_data["data"]["quarterly_earnings"] = quarterly_earnings.to_dict()
                    else:
                        st.info("No quarterly earnings data")
                except:
                    st.error("Error fetching quarterly earnings")
                
                st.markdown("---")
            
            # =========================
            # 9. OPTIONS DATA
            # =========================
            if fetch_options:
                st.markdown("## 📈 Options Data")
                
                try:
                    options_dates = stock.options
                    if options_dates and len(options_dates) > 0:
                        st.markdown("### Available Expiration Dates")
                        st.write(options_dates)
                        
                        selected_date = st.selectbox("Select Expiration Date", options_dates)
                        
                        if selected_date:
                            option_chain = stock.option_chain(selected_date)
                            
                            tab1, tab2 = st.tabs(["📞 Calls", "📉 Puts"])
                            
                            with tab1:
                                st.markdown("### Call Options")
                                if option_chain.calls is not None and not option_chain.calls.empty:
                                    st.dataframe(option_chain.calls, use_container_width=True)
                                    all_data["data"]["options_calls"] = option_chain.calls.to_dict()
                            
                            with tab2:
                                st.markdown("### Put Options")
                                if option_chain.puts is not None and not option_chain.puts.empty:
                                    st.dataframe(option_chain.puts, use_container_width=True)
                                    all_data["data"]["options_puts"] = option_chain.puts.to_dict()
                    else:
                        st.info("No options data available for this stock")
                except:
                    st.error("Error fetching options data")
                
                st.markdown("---")
            
            # =========================
            # 10. NEWS
            # =========================
            if fetch_news:
                st.markdown("## 📰 Latest News")
                
                try:
                    news = stock.news
                    if news and len(news) > 0:
                        all_data["data"]["news"] = news
                        
                        for idx, article in enumerate(news[:10]):  # Show top 10
                            with st.expander(f"📄 {article.get('title', 'No Title')}"):
                                st.write(f"**Publisher:** {article.get('publisher', 'Unknown')}")
                                st.write(f"**Published:** {datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
                                st.write(f"**Link:** [Read More]({article.get('link', '#')})")
                                if article.get('thumbnail'):
                                    st.image(article['thumbnail'].get('resolutions', [{}])[0].get('url', ''), width=200)
                    else:
                        st.info("No news available")
                except Exception as e:
                    st.error(f"Error fetching news: {e}")
                
                st.markdown("---")
            
            # =========================
            # 11. RAW INFO (Everything)
            # =========================
            st.markdown("## 🗂️ Complete Raw Data")
            
            with st.expander("📊 Click to view ALL raw data from yfinance"):
                info = stock.info
                
                # Convert to JSON for better display
                json_data = json.dumps(info, indent=2, default=str)
                st.code(json_data, language='json')
                
                all_data["data"]["raw_info"] = info
            
            # =========================
            # DOWNLOAD JSON
            # =========================
            if download_json:
                st.markdown("---")
                st.markdown("## 📥 Download Data")
                
                # Convert all data to JSON
                json_str = json.dumps(all_data, indent=2, default=str)
                
                st.download_button(
                    label="💾 Download Complete Data as JSON",
                    data=json_str,
                    file_name=f"{stock_symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                st.success(f"✅ Data ready for download! Total size: {len(json_str)} bytes")
            
            # Success message
            st.sidebar.success(f"✅ Data fetched successfully!")
            st.sidebar.info(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

else:
    # Initial state
    st.info("👈 Configure settings in the sidebar and click 'Fetch All Data' to begin")
    
    st.markdown("---")
    st.markdown("### 📋 Available Data Sections:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - ✅ **Basic Info**: Company details, sector, industry
        - ✅ **Price Data**: Current price, 52-week range, volume
        - ✅ **Financial Data**: P/E, ROE, margins, ratios
        - ✅ **Financial Statements**: Income, balance sheet, cash flow
        - ✅ **Shareholders**: Major holders, institutional investors
        """)
    
    with col2:
        st.markdown("""
        - ✅ **Dividends & Splits**: Dividend history, stock splits
        - ✅ **Analyst Recommendations**: Target prices, ratings
        - ✅ **Earnings Calendar**: Earnings dates, quarterly results
        - ✅ **Options Data**: Call/Put options chain
        - ✅ **Latest News**: Recent news articles
        """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Tips:")
    st.markdown("""
    1. **Select a stock** from the dropdown
    2. **Choose data sections** you want to fetch (checking all may take longer)
    3. **Click 'Fetch All Data'** button
    4. **Enable JSON Download** to save data for later use
    5. Data is cached for 5 minutes to improve performance
    """)
    
    st.markdown("---")
    
    # Sample data preview
    st.markdown("### 📊 Sample Data Structure:")
    
    sample_json = {
        "symbol": "RELIANCE.NS",
        "company_name": "RELIANCE",
        "fetch_timestamp": "2024-01-15 10:30:00",
        "data": {
            "basic_info": {
                "Company Name": "Reliance Industries Limited",
                "Sector": "Energy",
                "Industry": "Oil & Gas Refining & Marketing"
            },
            "price_data": {
                "Current Price": "₹2450.50",
                "Market Cap": "₹16,58,234 Cr"
            },
            "financial_metrics": {
                "P/E Ratio": "24.5",
                "ROE": "12.3%"
            }
        }
    }
    
    st.json(sample_json)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>📊 <b>Complete Stock Data Viewer</b></p>
        <p>Data provided by Yahoo Finance via yfinance library</p>
        <p>Updates every 5 minutes | Free & Open Source</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info("""
**Features:**
- Fetch ALL available yfinance data
- Clean organized display
- Download as JSON
- Real-time updates
- No API key required

**Note:** Some data may not be available for all stocks.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")