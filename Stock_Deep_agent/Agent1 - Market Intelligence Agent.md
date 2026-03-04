AGENT 1: MARKET INTELLIGENCE AGENT
A. DATA COLLECTION MODULE (24/7 Operation)
1.1 Real-Time Market Data

DATA_SOURCES = 

{
    "PRIMARY": {
        "NSE": {
            "endpoint": "https://www.nseindia.com/api/equity-stockIndices",
            "type": "REST + WebSocket",
            "frequency": "tick-by-tick",
            "data": [
                "Live prices (LTP, Open, High, Low, Close)",
                "Volume (traded qty, delivery qty)",
                "Bid-Ask spread (top 5 levels)",
                "Market depth",
                "Circuit limits",
                "52-week high/low",
                "VWAP",
                "Total buy/sell quantity"
            ]
        },
        "BSE": {
            "endpoint": "https://api.bseindia.com",
            "type": "REST",
            "frequency": "1 minute",
            "data": ["Similar to NSE"]
        }
    },
    
    "DERIVATIVES": {
        "Futures": {
            "data": [
                "Futures price (all expiries)",
                "Open Interest (OI)",
                "OI change (buildup/unwinding)",
                "Rollover percentage",
                "Basis (Spot - Futures)",
                "Cost of carry",
                "Long/Short buildup indicators"
            ]
        },
        "Options": {
            "data": [
                "Options chain (Calls & Puts - all strikes)",
                "Implied Volatility (IV)",
                "IV Rank & Percentile",
                "PCR (Put-Call Ratio) - OI & Volume based",
                "Max Pain level",
                "Option Greeks (Delta, Gamma, Theta, Vega)",
                "Open Interest distribution",
                "Change in OI (COI)",
                "Options Volume analysis",
                "Large option trades (block)",
                "IV skew analysis"
            ]
        }
    },
    
    "INSTITUTIONAL_ACTIVITY": {
        "FII_DII": {
            "source": "NSE Reports",
            "frequency": "Daily (published EOD)",
            "data": [
                "FII net buying/selling (₹ Crore)",
                "DII net buying/selling",
                "FII futures position",
                "FII options position",
                "Sector-wise FII flow",
                "Stock-wise FII holding changes"
            ]
        },
        "Bulk_Block_Deals": {
            "source": "NSE/BSE announcements",
            "data": [
                "Buyer/Seller name",
                "Quantity traded",
                "Price",
                "Institutional vs Promoter vs Individual"
            ]
        },
        "Mutual_Funds": {
            "source": "SEBI filings + AMFI",
            "frequency": "Monthly",
            "data": [
                "MF holding changes",
                "New positions",
                "Exits",
                "Top holdings per scheme"
            ]
        }
    },
    
    "ORDER_BOOK_MICROSTRUCTURE": {
        "Level_2_Data": {
            "data": [
                "Top 5 bid prices & quantities",
                "Top 5 ask prices & quantities",
                "Order imbalance ratio",
                "Book pressure (buy vs sell)",
                "Large order detection (icebergs)",
                "Order cancellation patterns",
                "Time & sales data"
            ]
        }
    }
}



1.2 Fundamental Data Collection

FUNDAMENTAL_SOURCES = {
    "QUARTERLY_RESULTS": {
        "sources": [
            "Screener.in (scraping with rotating proxies)",
            "Trendlyne API",
            "BSE/NSE corporate announcements",
            "Company investor presentations"
        ],
        "data": {
            "Income_Statement": [
                "Revenue (Total, Operating)",
                "EBITDA",
                "EBIT",
                "PBT, PAT",
                "EPS (Basic, Diluted)",
                "Margins (Gross, Operating, Net)",
                "Tax rate",
                "Other income",
                "Exceptional items"
            ],
            "Balance_Sheet": [
                "Total Assets",
                "Current Assets (Cash, Inventory, Receivables)",
                "Fixed Assets",
                "Intangible Assets",
                "Total Liabilities",
                "Current Liabilities",
                "Long-term debt",
                "Short-term debt",
                "Shareholder equity",
                "Reserves",
                "Book value per share"
            ],
            "Cash_Flow": [
                "Operating cash flow",
                "Investing cash flow",
                "Financing cash flow",
                "Free cash flow",
                "CAPEX",
                "Cash & equivalents"
            ],
            "Ratios": [
                "P/E (Current, Forward, Trailing)",
                "P/B, P/S, EV/EBITDA",
                "Debt/Equity",
                "Current Ratio",
                "Quick Ratio",
                "Interest Coverage",
                "ROE, ROA, ROCE",
                "Asset Turnover",
                "Inventory Turnover",
                "Receivables Days",
                "Payables Days",
                "Cash Conversion Cycle",
                "Dividend Yield",
                "Payout Ratio"
            ]
        },
        "frequency": "Quarterly + Annual"
    },
    
    "CORPORATE_ACTIONS": {
        "data": [
            "Dividend announcements (interim, final)",
            "Stock splits",
            "Bonus issues",
            "Rights issues",
            "Buyback announcements",
            "Merger & Acquisitions",
            "Demergers",
            "QIP/FPO announcements"
        ]
    },
    
    "MANAGEMENT_QUALITY": {
        "data": [
            "Promoter holding %",
            "Promoter pledging %",
            "Board composition",
            "Management changes",
            "Related party transactions",
            "Corporate governance score",
            "Audit reports (qualified/unqualified)",
            "Whistleblower complaints"
        ]
    },
    
    "INDUSTRY_SECTOR": {
        "data": [
            "Industry growth rate",
            "Market size (TAM)",
            "Company market share",
            "Competitor analysis",
            "Industry regulations",
            "Import/Export data",
            "Capacity utilization",
            "Commodity price impact (if applicable)"
        ]
    }
}



1.3 News & Sentiment Collection
NEWS_SENTIMENT_SOURCES = {
    "NEWS_AGGREGATORS": {
        "Primary": [
            {
                "source": "MoneyControl",
                "endpoint": "https://www.moneycontrol.com/rss/",
                "type": "RSS + Scraping",
                "categories": [
                    "Market news",
                    "Stock-specific news",
                    "Sector news",
                    "Earnings news",
                    "IPO news",
                    "Economy news"
                ]
            },
            {
                "source": "Economic Times",
                "endpoint": "https://economictimes.indiatimes.com/markets/rssfeeds/",
                "type": "RSS + API"
            },
            {
                "source": "Business Standard",
                "type": "RSS + Scraping"
            },
            {
                "source": "Reuters India",
                "type": "API"
            },
            {
                "source": "Bloomberg India",
                "type": "API (paid)"
            }
        ],
        "Real_Time_Alerts": [
            "Google News API (stock name as query)",
            "NSE/BSE announcements feed",
            "SEBI announcements",
            "Corporate announcements (real-time)"
        ]
    },
    
    "SOCIAL_MEDIA": {
        "Twitter_X": {
            "method": "Twitter API v2",
            "tracking": [
                "Hashtags: #NIFTY, #SENSEX, #StockName",
                "Handles: @moneycontrolcom, @economictimes, etc.",
                "Influencers: Finance Twitter accounts (top 100)",
                "Corporate handles (official announcements)"
            ],
            "metrics": [
                "Tweet volume",
                "Sentiment score (NLP)",
                "Engagement (likes, retweets)",
                "Trending topics",
                "Unusual spike detection"
            ]
        },
        "Reddit": {
            "subreddits": [
                "r/IndiaInvestments",
                "r/Indian_StreetBets",
                "r/StockMarket"
            ],
            "data": [
                "Post sentiment",
                "Comment sentiment",
                "Upvote ratio",
                "Discussion volume"
            ]
        },
        "Telegram": {
            "channels": [
                "Stock market channels (top 50)",
                "Analyst channels"
            ],
            "method": "Telegram Bot API"
        },
        "YouTube": {
            "tracking": "Finance channels (video titles, descriptions)","method": "YouTube Data API v3",
            "metrics": [
                "Video sentiment (title/description NLP)",
                "View count trends",
                "Comment sentiment",
                "Channel credibility score"
            ]
        },
        "WhatsApp_Groups": {
            "method": "Manual monitoring + WhatsApp Business API",
            "note": "Limited automation due to privacy"
        }
    },
    
    "EARNINGS_CALLS_TRANSCRIPTS": {
        "sources": [
            "Company investor relations websites",
            "BSE/NSE filings",
            "Third-party transcript providers"
        ],
        "analysis": [
            "Management tone (optimistic/cautious) - NLP",
            "Key phrases extraction",
            "Guidance changes",
            "Question pattern analysis",
            "Management confidence scoring"
        ]
    },
    
    "REGULATORY_FILINGS": {
        "SEBI": [
            "Insider trading disclosures",
            "Shareholding pattern changes",
            "Material events",
            "Related party transactions",
            "Corporate governance reports"
        ],
        "MCA": [
            "Director appointments/resignations",
            "Charge creation (new loans)",
            "Annual filings"
        ]
    }
}

# SENTIMENT ANALYSIS ENGINE
SENTIMENT_PROCESSING = {
    "NLP_MODELS": {
        "Primary": "FinBERT (Financial domain pre-trained)",
        "Secondary": "Custom LSTM (trained on Indian market news)",
        "Languages": ["English", "Hindi (transliterated)"]
    },
    
    "SENTIMENT_SCORES": {
        "Calculation": """
        1. Text Preprocessing:
           - Remove noise, URLs, special chars
           - Tokenization
           - Stop word removal
           - Lemmatization
        
        2. Entity Recognition:
           - Extract company names, stock symbols
           - Identify financial metrics mentioned
           - Detect events (merger, earnings, etc.)
        
        3. Sentiment Classification:
           - Positive (0.6 to 1.0)
           - Neutral (0.4 to 0.6)
           - Negative (0.0 to 0.4)
        
        4. Weightage Assignment:
           - Source credibility (Reuters: 1.0, Random blog: 0.3)
           - Recency (decay function: 1.0 for <1hr, 0.5 for 24hr)
           - Reach (high traffic sources weighted higher)
        
        5. Aggregation:
           Final_Sentiment = Σ(sentiment_i × weight_i) / Σ(weight_i)
        """
    },
    
    "OUTPUT_METRICS": {
        "Stock_Level": {
            "overall_sentiment": "0-100 scale",
            "news_count_24h": "integer",
            "positive_ratio": "percentage",
            "negative_ratio": "percentage",
            "sentiment_trend": "improving/stable/deteriorating",
            "key_topics": ["list of dominant themes"],
            "major_news_events": ["breaking news list"]
        },
        "Sector_Level": {
            "sector_sentiment": "0-100 scale",
            "trending_sector": "boolean",
            "sector_rotation_signal": "into/outof/neutral"
        },
        "Market_Level": {
            "market_mood": "fear/neutral/greed",
            "fear_greed_index": "0-100",
            "risk_appetite": "low/medium/high"
        }
    }
}

1.4 Global Market & Macro Data
GLOBAL_MACRO_DATA = {
    "GLOBAL_MARKETS": {
        "US_Markets": {
            "indices": ["S&P 500", "NASDAQ", "Dow Jones"],
            "source": "Yahoo Finance API",
            "frequency": "Real-time during US hours",
            "correlation_tracking": "India market correlation coefficient"
        },
        "Asian_Markets": {
            "indices": ["Nikkei", "Hang Seng", "Shanghai", "Singapore"],
            "relevance": "Pre-market sentiment for India"
        },
        "European_Markets": {
            "indices": ["FTSE", "DAX", "CAC"],
            "timing": "Concurrent with Indian market"
        },
        "VIX": {
            "metric": "Volatility Index",
            "use": "Global risk sentiment"
        }
    },
    
    "COMMODITIES": {
        "Crude_Oil": {
            "benchmark": "Brent Crude",
            "impact": "OMC stocks, Inflation",
            "source": "Investing.com API"
        },
        "Gold": {
            "impact": "Jewelry stocks, Safe haven demand"
        },
        "Metals": {
            "types": ["Copper", "Aluminum", "Zinc", "Steel"],
            "impact": "Metal sector stocks"
        },
        "Agricultural": {
            "types": ["Wheat", "Rice", "Cotton", "Sugar"],
            "impact": "FMCG, Agro-based industries"
        }
    },
    
    "CURRENCY": {
        "USD_INR": {
            "source": "RBI reference rate + live forex",
            "impact": "IT exporters, Importers",
            "frequency": "Real-time"
        },
        "Dollar_Index": {
            "impact": "EM flows, FII sentiment"
        }
    },
    
    "INTEREST_RATES": {
        "India": {
            "Repo_Rate": "RBI policy rate",
            "10Y_Gsec": "Bond yield (indicator)",
            "source": "RBI website"
        },
        "US": {
            "Fed_Rate": "US Federal Reserve rate",
            "US_10Y_Treasury": "Global benchmark",
            "impact": "FII flows (interest rate differential)"
        }
    },
    
    "ECONOMIC_INDICATORS": {
        "India": {
            "GDP_Growth": {
                "frequency": "Quarterly",
                "source": "NSO (National Statistical Office)"
            },
            "Inflation": {
                "CPI": "Monthly",
                "WPI": "Monthly",
                "source": "Ministry of Statistics"
            },
            "IIP": {
                "metric": "Industrial production",
                "frequency": "Monthly"
            },
            "PMI": {
                "types": ["Manufacturing PMI", "Services PMI"],
                "frequency": "Monthly",
                "source": "IHS Markit"
            },
            "Trade_Balance": {
                "exports": "Monthly",
                "imports": "Monthly",
                "source": "Commerce Ministry"
            },
            "GST_Collections": {
                "frequency": "Monthly",
                "indicator": "Economic activity"
            },
            "Auto_Sales": {
                "frequency": "Monthly",
                "indicator": "Consumer demand"
            },
            "Bank_Credit_Growth": {
                "frequency": "Fortnightly",
                "source": "RBI"
            },
            "Forex_Reserves": {
                "frequency": "Weekly",
                "source": "RBI"
            }
        },
        "Global": {
            "US_Jobs_Report": "Monthly NFP",
            "US_CPI_PPI": "Inflation data",
            "China_GDP": "Quarterly",
            "Global_PMI": "Monthly"
        }
    },
    
    "POLICY_EVENTS": {
        "RBI_MPC": {
            "frequency": "Bi-monthly",
            "tracking": [
                "Rate decision",
                "Policy stance",
                "Governor commentary",
                "Minutes of meeting"
            ]
        },
        "Union_Budget": {
            "frequency": "Annual (Feb 1)",
            "impact": "Sector-specific allocations"
        },
        "Government_Policies": {
            "tracking": [
                "PLI schemes",
                "Subsidy changes",
                "Tax changes",
                "Regulatory reforms"
            ]
        }
    }
}

# MACRO IMPACT SCORING
MACRO_IMPACT_MODEL = {
    "Event_Impact_Matrix": {
        "RBI_Rate_Hike_50bps": {
            "Banking": "+3 to +5%",
            "Real_Estate": "-5 to -8%",
            "Auto": "-3 to -5%",
            "NBFC": "-2 to -4%"
        },
        "Crude_Oil_+10%": {
            "OMC": "-8 to -12%",
            "Airlines": "-10 to -15%",
            "Paints": "-3 to -5%",
            "Logistics": "-2 to -4%"
        },
        # ... more event-impact mappings
    }
}


1.5 Advanced Microstructure Analytics
MICROSTRUCTURE_ANALYSIS = {
    "ORDER_FLOW_TOXICITY": {
        "VPIN": {
            "metric": "Volume-Synchronized Probability of Informed Trading",
            "calculation": """
            Detects informed trading vs noise trading
            High VPIN = Smart money active
            """,
            "use_case": "Detect institutional accumulation/distribution"
        }
    },
    
    "LIQUIDITY_METRICS": {
        "Bid_Ask_Spread": {
            "absolute": "₹ difference",
            "percentage": "% of price",
            "interpretation": "Narrow = liquid, Wide = illiquid"
        },
        "Market_Depth": {
            "metric": "Total quantity in top 5 bids/asks",
            "imbalance_ratio": "Buy depth / Sell depth"
        },
        "Amihud_Illiquidity": {
            "formula": "abs(return) / volume",
            "use": "Price impact per unit volume"
        }
    },
    
    "SPOOFING_DETECTION": {
        "pattern": "Large orders placed and cancelled quickly",
        "alert": "Potential manipulation",
        "action": "Avoid trading during spoofing periods"
    },
    
    "ICEBERG_ORDER_DETECTION": {
        "pattern": "Multiple small orders at same price",
        "interpretation": "Large institutional order being executed",
        "signal": "Direction of iceberg = likely direction"
    }
}