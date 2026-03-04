AGENT 2: ANALYSIS ENGINE AGENT
A. MULTI-TIMEFRAME TECHNICAL ANALYSIS
2.1 Minute-Level Analysis (Scalping/HFT)


MINUTE_LEVEL_ANALYSIS = {
    "TICK_DATA_ANALYSIS": {
        "Data_Frequency": "Tick-by-tick (every trade)",
        
        "Volume_Analysis": {
            "Volume_Spike_Detection": {
                "threshold": "3x of 5-min average",
                "interpretation": "Institutional activity or news reaction",
                "signal_generation": """
                If Price_Up + Volume_Spike → Strong Buy
                If Price_Down + Volume_Spike → Strong Sell
                """
            },
            "Cumulative_Delta": {
                "calculation": "Σ(Buy_Volume - Sell_Volume)",
                "interpretation": """
                Positive delta = Buying pressure
                Negative delta = Selling pressure
                Divergence with price = reversal signal
                """
            }
        },
        
        "Order_Book_Imbalance": {
            "Calculation": "(Bid_Volume - Ask_Volume) / (Bid_Volume + Ask_Volume)",
            "Threshold": {
                "Strong_Buy": "> +0.6",
                "Moderate_Buy": "+0.3 to +0.6",
                "Neutral": "-0.3 to +0.3",
                "Moderate_Sell": "-0.6 to -0.3",
                "Strong_Sell": "< -0.6"
            },
            "Time_Validity": "1-5 minutes"
        },
        
        "Tape_Reading": {
            "Large_Trade_Detection": {
                "threshold": "> 10x average trade size",
                "analysis": [
                    "Trade at bid = Seller aggressive (bearish)",
                    "Trade at ask = Buyer aggressive (bullish)",
                    "Trade between spread = negotiated (neutral)"
                ]
            },
            "Trade_Clustering": {
                "pattern": "Multiple large trades in short period",
                "interpretation": "Institutional accumulation/distribution"
            }
        },
        
        "Price_Action_Patterns": {
            "Stop_Hunt": {
                "pattern": "Sudden spike → immediate reversal",
                "interpretation": "Stop losses triggered, then reversal",
                "signal": "Counter-trend opportunity"
            },
            "Short_Squeeze": {
                "indicators": [
                    "High short interest in futures",
                    "Sudden upward spike",
                    "Volume expansion"
                ],
                "signal": "Momentum continuation"
            }
        }
    },
    
    "SCALPING_INDICATORS": {
        "1_Minute_Chart": {
            "EMA_5_15": {
                "signal": "5 EMA crosses above 15 EMA = Buy",
                "exit": "5 EMA crosses below 15 EMA"
            },
            "RSI_2": {
                "oversold": "< 10 (extreme)",
                "overbought": "> 90 (extreme)",
                "mean_reversion": "High probability"
            },
            "Stochastic_5_3_3": {
                "signal": "Fast line crosses above slow in oversold"
            }
        }
    },
    
    "NEWS_IMPACT_TRACKER": {
        "Flash_News_Detection": {
            "latency": "< 100ms from news publish",
            "impact_prediction": """
            ML model predicts price movement based on:
            - News headline sentiment
            - News source credibility
            - Historical reaction to similar news
            """,
            "signal_validity": "30 seconds to 2 minutes"
        }
    },
    
    "ALGORITHMIC_PATTERN_DETECTION": {
        "Detection": [
            "VWAP algo (price oscillating around VWAP)",
            "TWAP algo (steady buying/selling)",
            "Implementation Shortfall algo",
            "Market making patterns"
        ],
        "Strategy": "Trade with the algo direction"
    }
}


2.2 Hour-Level Analysis (Intraday)
HOUR_LEVEL_ANALYSIS = {
    "INTRADAY_TECHNICAL_INDICATORS": {
        "Moving_Averages": {
            "5_min_chart": ["EMA_9", "EMA_21", "SMA_50"],
            "15_min_chart": ["EMA_20", "EMA_50", "SMA_100"],
            "signals": {
                "Golden_Cross": "Fast MA > Slow MA → Buy",
                "Death_Cross": "Fast MA < Slow MA → Sell",
                "Price_Above_All_MAs": "Strong uptrend",
                "MA_Confluence": "Strong support/resistance"
            }
        },
        
        "VWAP_Strategy": {
            "Calculation": "Σ(Price × Volume) / Σ(Volume)",
            "Bands": "VWAP ± 1 StdDev, ± 2 StdDev",
            "Strategies": {
                "Mean_Reversion": """
                If Price > VWAP+2SD → Short (expect reversion)
                If Price < VWAP-2SD → Long (expect reversion)
                """,
                "Trend_Following": """
                If Price consistently > VWAP → Stay long
                If Price consistently < VWAP → Stay short
                """,
                "Support_Resistance": """
                VWAP acts as dynamic S/R
                Buy at VWAP support, Sell at VWAP resistance
                """
            }
        },
        
        "RSI_MACD_Combo": {
            "RSI_14": {
                "oversold":"oversold": "< 30",
                "overbought": "> 70",
                "divergence_detection": {
                    "Bullish_Divergence": "Price making lower lows, RSI making higher lows → Buy",
                    "Bearish_Divergence": "Price making higher highs, RSI making lower highs → Sell"
                }
            },
            "MACD_12_26_9": {
                "signals": {
                    "Bullish_Crossover": "MACD line crosses above signal line",
                    "Bearish_Crossover": "MACD line crosses below signal line",
                    "Histogram_Expansion": "Increasing momentum",
                    "Zero_Line_Cross": "Trend change confirmation"
                }
            },
            "Combined_Signal": """
            STRONG BUY: RSI oversold + MACD bullish crossover
            STRONG SELL: RSI overbought + MACD bearish crossover
            """
        },
        
        "Bollinger_Bands": {
            "Settings": "20-period SMA, 2 standard deviations",
            "Strategies": {
                "Squeeze": "Bands narrow → Volatility expansion coming",
                "Breakout": "Price breaks above upper band + volume → Continuation",
                "Rejection": "Price touches upper band but closes inside → Reversal",
                "Walking_Bands": "Price riding upper band = strong trend"
            }
        },
        
        "Pivot_Points": {
            "Types": ["Standard", "Fibonacci", "Camarilla"],
            "Calculation": {
                "Pivot": "(High + Low + Close) / 3",
                "R1": "2×Pivot - Low",
                "S1": "2×Pivot - High",
                "R2": "Pivot + (High - Low)",
                "S2": "Pivot - (High - Low)"
            },
            "Usage": "Intraday support/resistance levels"
        },
        
        "ATR_Volatility": {
            "ATR_14": "Average True Range",
            "Uses": {
                "Stop_Loss": "Entry ± (2 × ATR)",
                "Position_Sizing": "Risk amount / ATR = position size",
                "Breakout_Filter": "Valid breakout if move > 0.5 × ATR"
            }
        }
    },
    
    "VOLUME_PROFILE_ANALYSIS": {
        "POC": {
            "metric": "Point of Control (price with highest volume)",
            "interpretation": "Strong support/resistance level"
        },
        "Value_Area": {
            "definition": "Price range where 70% of volume traded",
            "VAH": "Value Area High",
            "VAL": "Value Area Low",
            "strategy": "Buy at VAL, sell at VAH (range trading)"
        },
        "Volume_Nodes": {
            "HVN": "High Volume Node = strong S/R",
            "LVN": "Low Volume Node = quick price movement expected"
        }
    },
    
    "INTRADAY_PATTERNS": {
        "Opening_Range_Breakout": {
            "method": "First 15-30 min range",
            "signal": "Break above/below opening range with volume"
        },
        "Power_Hour": {
            "time": "Last hour of trading (3:00-3:30 PM)",
            "behavior": "Institutional positioning, high volume"
        },
        "Lunch_Hour_Doldrums": {
            "time": "12:30-2:00 PM",
            "behavior": "Low volume, avoid trading"
        }
    },
    
    "SMART_MONEY_TRACKING": {
        "Large_Orders": {
            "detection": "Unusual volume at specific price",
            "interpretation": "Institutional interest level"
        },
        "Absorption": {
            "pattern": "Large selling but price not falling (or vice versa)",
            "interpretation": "Smart money absorbing supply/demand"
        },
        "Sweep_Orders": {
            "pattern": "Multiple orders sweeping through order book",
            "interpretation": "Aggressive institutional positioning"
        }
    }
}

2.3 Days-Weeks Analysis (Swing Trading)
SWING_TRADING_ANALYSIS = {
    "CHART_PATTERN_RECOGNITION": {
        "ML_Based_Detection": {
            "Model": "Convolutional Neural Network (CNN)",
            "Training_Data": "10,000+ labeled chart patterns",
            "Patterns_Detected": [
                {
                    "name": "Cup_and_Handle",
                    "success_rate": "68%",
                    "avg_gain": "12%",
                    "holding_period": "15-30 days",
                    "confirmation": [
                        "Volume dries up in cup formation",
                        "Volume expands on handle breakout",
                        "Breakout above cup rim with 1.5x volume"
                    ],
                    "target": "Depth of cup added to breakout point",
                    "stop_loss": "Below handle low"
                },
                {
                    "name": "Head_and_Shoulders",
                    "type": "Reversal (bearish)",
                    "success_rate": "72%",
                    "confirmation": "Break below neckline with volume",
                    "target": "Height of head subtracted from neckline",
                    "stop_loss": "Above right shoulder"
                },
                {
                    "name": "Inverse_Head_and_Shoulders",
                    "type": "Reversal (bullish)",
                    "success_rate": "70%"
                },
                {
                    "name": "Double_Top",
                    "type": "Reversal (bearish)",
                    "confirmation": "Break below support between peaks"
                },
                {
                    "name": "Double_Bottom",
                    "type": "Reversal (bullish)"
                },
                {
                    "name": "Ascending_Triangle",
                    "type": "Continuation (bullish)",
                    "confirmation": "Breakout above horizontal resistance"
                },
                {
                    "name": "Descending_Triangle",
                    "type": "Continuation (bearish)"
                },
                {
                    "name": "Symmetrical_Triangle",
                    "type": "Continuation (direction depends on entry trend)"
                },
                {
                    "name": "Flag_Bull",
                    "type": "Continuation",
                    "characteristic": "Sharp rise → consolidation → breakout",
                    "target": "Flagpole height added to breakout"
                },
                {
                    "name": "Pennant",
                    "similar_to": "Flag but converging trendlines"
                },
                {
                    "name": "Rectangle",
                    "type": "Consolidation",
                    "breakout_direction": "Determines trade direction"
                },
                {
                    "name": "Rounding_Bottom",
                    "type": "Reversal (bullish)",
                    "duration": "Several weeks to months"
                }
            ]
        },
        
        "Traditional_Charting": {
            "Trendlines": {
                "Uptrend_Line": "Connect higher lows",
                "Downtrend_Line": "Connect lower highs",
                "Validation": "Minimum 3 touches",
                "Break_Signal": "Close beyond trendline with volume"
            },
            "Channels": {
                "Parallel_Channel": "Trade between support and resistance",
                "Expanding_Channel": "Increasing volatility",
                "Contracting_Channel": "Decreasing volatility (squeeze)"
            }
        }
    },
    
    "TREND_STRUCTURE_ANALYSIS": {
        "Swing_Points": {
            "Higher_Highs_Higher_Lows": {
                "signal": "UPTREND",
                "strategy": "Buy dips to support",
                "invalidation": "Break of higher low"
            },
            "Lower_Highs_Lower_Lows": {
                "signal": "DOWNTREND",
                "strategy": "Sell rallies to resistance",
                "invalidation": "Break of lower high"
            },
            "Break_of_Structure": {
                "BOS_Bullish": "Price breaks above previous higher high → Strong uptrend",
                "BOS_Bearish": "Price breaks below previous lower low → Strong downtrend"
            }
        },
        
        "Wyckoff_Method": {
            "Accumulation": {
                "phases": [
                    "Phase A: Selling climax (PS, SC, AR)",
                    "Phase B: Building cause (ST)",
                    "Phase C: Spring (false breakdown)",
                    "Phase D: Markup begins (SOS, LPS)",
                    "Phase E: Trend established"
                ],
                "signal": "Buy in Phase C or early Phase D"
            },
            "Distribution": {
                "phases": ["Similar but inverted"],
                "signal": "Sell in Phase C or early Phase D"
            }
        },
        
        "Elliott_Wave": {
            "Impulse_Waves": "5 waves (1,2,3,4,5) in trend direction",
            "Corrective_Waves": "3 waves (A,B,C) against trend",
            "Rules": [
                "Wave 2 cannot retrace > 100% of Wave 1",
                "Wave 3 is never the shortest",
                "Wave 4 cannot overlap Wave 1"
            ],
            "Fibonacci_Targets": {
                "Wave_3": "1.618 × Wave 1",
                "Wave_5": "0.618 × (Wave 1 to 3)"
            }
        }
    },
    
    "VOLUME_ANALYSIS": {
        "On_Balance_Volume": {
            "Calculation": "Cumulative volume (add on up days, subtract on down days)",
            "Divergence": {
                "Bullish": "Price falling but OBV rising → Accumulation",
                "Bearish": "Price rising but OBV falling → Distribution"
            }
        },
        
        "Volume_Price_Analysis": {
            "Breakout_Volume": {
                "Valid_Breakout": "Volume > 1.5x of 20-day average",
                "False_Breakout": "Low volume breakout → likely to fail"
            },
            "Climax_Volume": {
                "Buying_Climax": "Extreme volume + price spike → Top",
                "Selling_Climax": "Extreme volume + price crash → Bottom"
            }
        },
        
        "Delivery_Volume_India_Specific": {
            "Delivery_Percentage": "Delivery qty / Total traded qty",
            "Interpretation": {
                "High_Delivery_65%+": "Genuine buying/selling (positional)",
                "Low_Delivery_<40%": "Speculative/intraday (less reliable)",
                "Increasing_Delivery": "Strong hands accumulating"
            },
            "Combined_Signal": """
            Price Up + High Delivery + Volume Expansion = STRONG BUY
            Price Down + High Delivery + Volume Expansion = STRONG SELL
            """
        }
    },
    
    "MOMENTUM_INDICATORS": {
        "ADX_DMI": {
            "ADX": "Trend strength (0-100)",
            "Interpretation": {
                "ADX_<20": "No trend, range-bound",
                "ADX_20-40": "Developing trend",
                "ADX_>40": "Strong trend"
            },
            "DI_Signals": {
                "+DI_above_-DI": "Bullish trend",
                "-DI_above_+DI": "Bearish trend"
            }
        },
        
        "Supertrend": {
            "Calculation": "ATR-based trailing stop",
            "Signal": {
                "Buy": "Price closes above Supertrend line",
                "Sell": "Price closes below Supertrend line"
            },
            "Advantage": "Clear trend following system"
        },
        
        "Ichimoku_Cloud": {
            "Components": [
                "Tenkan (9-period)",
                "Kijun (26-period)",
                "Senkou Span A & B (cloud)",
                "Chikou Span (lagging)"
            ],
            "Signals": {
                "Bullish": "Price above cloud + Tenkan > Kijun",
                "Bearish": "Price below cloud + Tenkan < Kijun",
                "Strong_Resistance": "Thick cloud",
                "Weak_Resistance": "Thin cloud"
            }
        }
    },
    
    "FIBONACCI_TOOLS": {
        "Retracement_Levels": {
            "levels": ["23.6%", "38.2%", "50%", "61.8%", "78.6%"],
            "usage": "Identify pullback support in uptrend",
            "golden_ratio": "61.8% most important"
        },
        "Extension_Levels": {
            "levels": ["127.2%", "161.8%", "200%", "261.8%"],
            "usage": "Project price targets"
        },
        "Time_Zones": {
            "usage": "Predict reversal timing based on Fib sequence"
        }
    },
    
    "CANDLE_PATTERNS": {
        "Single_Candle": [
            "Doji (indecision)",
            "Hammer (bullish reversal)",
            "Shooting Star (bearish reversal)",
            "Marubozu (strong trend continuation)"
        ],
        "Two_Candle": [
            "Engulfing (bullish/bearish reversal)",
            "Harami (trend pause)",
            "Piercing/Dark Cloud (reversal)"
        ],
        "Three_Candle": [
            "Morning Star (bullish reversal)",
            "Evening Star (bearish reversal)",
            "Three White Soldiers (strong bullish)",
            "Three Black Crows (strong bearish)"
        ],
        "Context_Importance": "Patterns near support/resistance more reliable"
    }
}

2.4 Months-Level Analysis (Medium-Term)

MEDIUM_TERM_ANALYSIS = {
    "FUNDAMENTAL_SCORING_SYSTEM": {
        "Earnings_Quality_Score": {
            "Revenue_Growth": {
                "Metric": "YoY & QoQ growth %",
                "Scoring": {
                    "Excellent_20_points": "> 20% YoY growth",
                    "Good_15_points": "15-20% growth",
                    "Average_10_points": "10-15% growth",
                    "Below_Average_5_points": "5-10% growth",
                    "Poor_0_points": "< 5% or negative"
                },
                "Consistency_Bonus": "+5 points if growth consistent for 4+ quarters"
            },
            
            "Profit_Margin_Expansion": {
                "Metrics": ["Gross Margin", "EBITDA Margin", "Net Margin"],
                "Scoring": {
                    "Expanding_15_points": "Margin improving QoQ",
                    "Stable_10_points": "Margin flat",
                    "Contracting_0_points": "Margin declining"
                }
            },
            
            "EPS_Growth": {
                "Metric": "YoY EPS growth %",
                "Scoring": "Similar to revenue growth",
                "Red_Flag": "Revenue growing but EPS declining"
            },
            
            "Earnings_Surprise": {
                "Calculation": "(Actual EPS - Estimated EPS) / Estimated EPS",
                "Positive_Surprise_10_points": "> +5%",
                "Inline_5_points": "Within ±5%",
                "Negative_Surprise_0_points": "< -5%"
            },
            
            "Quality_of_Earnings": {
                "Cash_vs_Accrual": {
                    "Metric": "Operating Cash Flow / Net Income",
                    "Excellent_>1.2": "Cash earnings exceed reported earnings",
                    "Good_0.8-1.2": "Cash aligns with earnings",
                    "Poor_<0.8": "Accrual-heavy earnings (red flag)"
                },
                "One_Time_Items": {
                    "Check": "Exceptional income/expenses",
                    "Adjustment": "Remove one-timers for true profitability",
                    "Red_Flag": "Frequent one-time items (earnings manipulation)"
                }
            }
        },
        
        "Financial_Health_Score": {
            "Debt_Analysis": {
                "Debt_to_Equity": {
                    "Excellent_<0.5": "20 points",
                    "Good_0.5-1.0": "15 points",
                    "Average_1.0-2.0": "10 points",
                    "Poor_>2.0": "5 points"
                },
                "Interest_Coverage": {
                    "Metric": "EBIT / Interest Expense",
                    "Safe_>5x": "20 points (can easily service debt)",
                    "Moderate_2-5x": "10 points",
                    "Risky_<2x": "0 points (default risk)"
                },
                "Debt_Trend": {
                    "Bonus_10_points": "Debt reducing YoY",
                    "Neutral": "Debt stable",
                    "Penalty_-10_points": "Debt increasing rapidly"
                }
            },
            
            "Liquidity_Ratios": {
                "Current_Ratio": {
                    "Metric": "Current Assets / Current Liabilities",
                    "Good_>1.5": "Can meet short-term obligations",
                    "Risky_<1.0": "Liquidity crisis potential"
                },
                "Quick_Ratio": {
                    "Metric": "(Current Assets - Inventory) / Current Liabilities",
                    "Ideal_>1.0": "Good liquidity even without selling inventory"
                }
            },
            
            "Working_Capital_Management": {
                "Cash_Conversion_Cycle": {
                    "Formula": "DIO + DSO - DPO",
                    "DIO": "Days Inventory Outstanding",
                    "DSO": "Days Sales Outstanding",
                    "DPO": "Days Payable Outstanding",
                    "Lower_is_Better": "Faster cash conversion",
                    "Excellent_<30_days": "20 points",
                    "Good_30-60_days": "15 points",
                    "Average_60-90_days": "10 points"
                }
            },
            
            "Asset_Quality": {
                "NPA_for_Banks": {
                    "Metric": "Non-Performing Assets %",
                    "Excellent_<2%": "Clean book",
                    "Risky_>5%": "Asset quality concerns"
                },
                "Asset_Turnover": {
                    "Metric": "Revenue / Total Assets",
                    "Higher_is_Better": "Efficient asset utilization"
                }
            }
        },
        
        "Growth_Catalyst_Score": {
            "CAPEX_Plans": {
                "High_CAPEX": "Future growth potential",
                "CAPEX_to_Sales_Ratio": "Indicates growth investment",
                "ROI_on_Past_CAPEX": "Track record of CAPEX efficiency"
            },
            
            "New_Products_Services": {
                "Launch_Pipeline": "Products in development",
                "Market_Size": "TAM for new products",
                "Time_to_Revenue": "When will revenue materialize"
            },
            
            "Market_Share_Gains": {
                "Tracking": "Quarterly market share changes",
                "Source": "Industry reports, company disclosures",
                "Scoring": {
                    "Gaining_Share_20_points": "Taking share from competitors",
                    "Maintaining_10_points": "Holding ground",
                    "Losing_Share_0_points": "Competitive pressure"
                }
            },
            
            "Geographic_Expansion": {
                "Domestic_Expansion": "New states/regions",
                "International_Expansion": "Export growth, foreign plants",
                "Risk_Assessment": "Execution risk in new markets"
            },
            
            "Capacity_Utilization": {
                "Current_Utilization": "% of capacity used",
                "Optimal_80-90%": "Room to grow without CAPEX",
                "Expansion_Plans": "New capacity coming online"
            }
        },
        
        "Management_Quality_Score": {
            "Guidance_Track_Record": {
                "Historical_Accuracy": "Did company meet past guidance?",
                "Scoring": {
                    "Consistently_Meets_20_points": "Trustworthy management",
                    "Sometimes_Meets_10_points": "Average",
                    "Rarely_Meets_0_points": "Credibility issue"
                }
            },
            
            "Capital_Allocation": {
                "ROE_Consistency": "Return on Equity > 15% for 5+ years",
                "ROCE_Consistency": "Return on Capital Employed > 18%",
                "Dividend_Policy": {
                    "Consistent_Dividends": "Shareholder-friendly",
                    "Growing_Dividends": "Bonus points",
                    "Erratic_Dividends": "Red flag"
                },
                "Share_Buybacks": {
                    "Smart_Buybacks": "When stock undervalued",
                    "Dumb_Buybacks": "When stock overvalued (destroys value)"
                }
            },
            
            "Promoter_Behavior": {
                "Promoter_Holding": {
                    "Stable_or_Increasing": "Confidence in business",
                    "Decreasing": "Warning sign (unless for fundraising)",
                    "Ideal_Range": "40-60% (not too low, not too high)"
                },
                "Promoter_Pledging": {
                    "Zero_Pledging": "20 points (best)",
                    "Low_Pledging_<20%": "10 points (acceptable)",
                    "High_Pledging_>50%": "0 points (major red flag)"
                }
            },
            
            "Corporate_Governance": {
                "Board_Independence": "% of independent directors",
                "Audit_Quality": "Big 4 auditor vs local auditor",
                "Related_Party_Transactions": "Low/transparent is good",
                "Past_Controversies": "SEBI cases, fraud allegations"
            }
        },
        
        "Valuation_Score": {
            "PE_Ratio_Analysis": {
                "Current_PE": "Today's P/E",
                "Historical_Average": "5-year median P/E",
                "Sector_Average": "Peer group P/E",
                "Scoring": {
                    "Undervalued_20_points": "Current < Hist avg by 20%+",
                    "Fair_Value_10_points": "Within ±10% of averages",
                    "Overvalued_0_points": "Current > Hist avg by 20%+"
                }
            },
            
            "PEG_Ratio": {
                "Formula": "P/E Ratio / Earnings Growth Rate",
                "Interpretation": {
                    "<1": "Undervalued relative to growth",
                    "1-2": "Fairly valued",
                    ">2": "Overvalued relative to growth"
                }
            },
            
            "Price_to_Book": {
                "Formula": "Market Price / Book Value per Share",
                "For_Asset_Heavy": "More relevant (banks, real estate)",
                "ROE_Consideration": "High ROE justifies higher P/B"
            },
            
            "EV_EBITDA": {
                "Formula": "Enterprise Value / EBITDA",
                "Advantage": "Removes capital structure differences",
                "Comparison": "Better for comparing peers"
            },
            
            "DCF_Model": {
                "Method": "Discounted Cash Flow",
                "Inputs": [
                    "Revenue growth projections (5 years)",
                    "EBITDA margin assumptions",
                    "CAPEX requirements",
                    "Tax rate",
                    "Terminal growth rate (2-3%)",
                    "Discount rate (WACC - 10-12% for India)"
                ],
                "Output": "Intrinsic value per share",
                "Comparison": "Current price vs intrinsic value"
            }
        },
        
        "FINAL_FUNDAMENTAL_SCORE": {
            "Calculation": """
            Total Score = 
                Earnings Quality (30%) +
                Financial Health (25%) +
                Growth Catalysts (20%) +
                Management Quality (15%) +
                Valuation (10%)
            """,
            "Rating": {
                "A_90-100": "STRONG BUY",
                "B_80-89": "BUY",
                "C_70-79": "HOLD",
                "D_60-69": "AVOID",
                "F_<60": "SELL"
            }
        }
    },
    
    "SECTOR_ANALYSIS": {
        "Sector_Rotation_Model": {
            "Economic_Cycle_Stages": {
                "Early_Cycle_Recovery": {
                    "Outperformers": ["Financials", "Real Estate", "Consumer Discretionary"],
                    "Underperformers": ["Utilities", "Consumer Staples"]
                },
                "Mid_Cycle_Expansion": {
                    "Outperformers": ["Technology", "Industrials", "Materials"],
                    "Underperformers": ["Defensives"]
                },
                "Late_Cycle_Peak": {
                    "Outperformers": ["Energy", "Materials"],
                    "Underperformers": ["Financials"]
                },
                "Recession_Contraction": {
                    "Outperformers": ["Consumer Staples", "Healthcare", "Utilities"],
                    "Underperformers": ["Cyclicals"]
                }
            },
            "Current_Cycle_Detection": {
                "Indicators": [
                    "GDP growth trend",
                    "Yield curve shape",
                    "PMI data",
                    "Credit growth",
                    "Corporate earnings momentum"
                ]
            }
        },
        
        "Relative_Strength_Analysis": {
            "Sector_vs_NIFTY": {
                "Calculation": "(Sector Index / NIFTY) × 100",
                "Interpretation": {
                    "Rising_Line": "Sector outperforming (rotate into)",
                    "Falling_Line": "Sector underperforming (rotate out)"
                }
            },
            "Stock_vs_Sector": {
                "Calculation": "(Stock Price / Sector Index) × 100",
                "Use": "Identify sector leaders"
            }
        },
        
        "Sector_Specific_Metrics": {
            "Banking": {
                "Key_Metrics": [
                    "NIM (Net Interest Margin)",
                    "CASA Ratio",
                    "Gross NPA %",
                    "Provision Coverage Ratio",
                    "Loan Growth",
                    "Credit Cost"
                ]
            },
            "IT_Services": {
                "Key_Metrics": [
                    "Revenue growth (CC terms)",
                    "EBIT margin",
                    "Attrition rate",
                    "Deal wins (TCV)",
                    "Employee utilization %",
                    "USD/INR impact"
                ]
            },
            "Pharma": {
                "Key_Metrics": [
                    "US FDA approvals",
                    "ANDA filings",
                    "API vs Formulations mix",
                    "Domestic vs Export ratio",
                    "R&D spend %",
                    "Pipeline products"
                ]
            },
            "Auto": {
                "Key_Metrics": [
                    "Monthly sales volumes",
                    "Market share",
                    "Discounts offered",
                    "Inventory days",
                    "EV transition progress",
                    "Export growth"
                ]
            },
            "Metals": {
                "Key_Metrics": [
                    "LME prices",
                    "Realizations per ton",
                    "Production volumes",
                    "Cost of production",
                    "China demand indicators",
                    "Inventory levels"
                ]
            }
        }
    },
    
    "INSTITUTIONAL_FLOW_ANALYSIS": {
        "FII_DII_Patterns": {
            "3_Month_Trend": {
                "Bullish": "Consistent FII buying for 3+ months",
                "Bearish": "Consistent FII selling",
                "Turning_Point": "FII switching from sell to buy (or vice versa)"
            },
            "Stock_Specific_FII": {
                "Source": "NSE shareholding pattern",
                "Frequency": "Quarterly",
                "Signal": {
                    "FII_Increasing_Holding": "Positive (institutional confidence)",
                    "FII_Decreasing_Holding": "Negative (risk-off)"
                }
            }
        },
        
        "Mutual_Fund_Activity": {
            "New_MF_Entries": "MFs buying stock for first time → Positive",
            "MF_Concentration": "If stock is in top 10 holdings of multiple large funds → Positive",
            "MF_Exits": "Large fund exiting position → Red flag"
        },
        
        "Insider_Trading": {
            "Promoter_Buying": {
                "Signal": "STRONG POSITIVE (skin in the game)",
                "Caveat": "Check if buying in open market or preferential allotment"
            },
            "Promoter_Selling": {
                "Signal": "Negative (unless for diversification/personal needs)",
                "Red_Flag": "Large percentage selling"
            },
            "Management_Buying": {
                "Signal": "Positive (management confidence)"
            }
        }
    },
    
    "EVENT_DRIVEN_ANALYSIS": {
        "Earnings_Announcement": {
            "Pre_Earnings": {
                "Estimate_Consensus": "Analyst EPS estimates",
                "Whisper_Number": "Unofficial estimate (often more accurate)",
                "Options_Positioning": "Implied move from options pricing"
            },
            "Post_Earnings": {
                "Beat_Raise": "Beat estimates + raise guidance → Buy",
                "Beat_Lower": "Beat but lower guidance → Sell",
                "Miss_Maintain": "Miss but maintain guidance → Hold/Monitor",
                "Miss_Lower": "Miss + lower guidance → Strong Sell"
            },
            "Management_Commentary": {
                "NLP_Analysis": "Sentiment from earnings call transcript",
                "Key_Phrases": "Optimistic, challenging, headwinds, tailwinds",
                "Guidance_Changes": "Most important part"
            }
        },
        
        "Corporate_Actions": {
            "Stock_Split": {
                "Impact": "Often bullish (improved liquidity)",
                "Strategy": "Buy before record date"
            },
            "Bonus_Issue": {
                "Impact": "Neutral to positive (shows confidence)",
                "Tax": "No tax implication (unlike dividend)"
            },
            "Dividend": {
                "Ex_Date_Drop": "Price drops by dividend amount",
                "Strategy": "For long-term holders only"
            },
            "Buyback": {
                "Impact": "Bullish (management sees value)",
                "EPS_Accretion": "Reduces shares outstanding"
            },
            "QIP_FPO": {
                "Impact": "Dilutive (share count increases)",
                "Positive_If": "Funds used for growth CAPEX",
                "Negative_If": "Funds used for debt repayment (distress signal)"
            }
        }
    }
}



2.5 Years-Level Analysis (Long-Term)
LONG_TERM_ANALYSIS = {
    "COMPOUNDING_QUALITY": {
        "10_Year_CAGR": {
            "Revenue_CAGR": ">15% = Excellent",
            "Profit_CAGR": ">18% = Excellent",
            "Consistency": "Bonus if growth consistent across years"
        },
        "Return_Ratios": {
            "ROE_>15%_for_10_years": "Wealth creator",
            "ROCE_>18%_for_10_years": "Efficient capital user",
            "ROE_Trend": "Increasing ROE = improving business"
        },
        "Free_Cash_Flow": {
            "FCF_Yield": "FCF / Market Cap > 5% = Good",
            "FCF_Growth": "Growing FCF = sustainable business"
        }
    },
    
    "MOAT_ANALYSIS": {
        "Types": {
            "Brand_Moat": ["Asian Paints", "HDFC Bank", "Titan"],
            "Network_Effects": ["Zomato", "Policy Bazaar"],
            "Cost_Leadership": ["Reliance", "UltraTech Cement"],
            "Switching_Costs": ["SAP", "Oracle"],
            "Regulatory_Moat": ["Utilities", "Licensed sectors"]
        },
        "Durability": "Moat should last 10+ years",
        "Pricing_Power": "Can raise prices without losing customers"
    },
    
    "INDUSTRY_MEGATRENDS": {
        "India_2030_Themes": [
            "Digitalization (Fintech, SaaS)",
            "Manufacturing (PLI schemes, China+1)",
            "EV Revolution",
            "Renewable Energy",
            "Urbanization (Real Estate, Infra)",
            "Premiumization (Consumption upgrade)",
            "Healthcare (Aging population)"
        ]
    }
}