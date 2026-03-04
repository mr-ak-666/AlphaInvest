DECISION_ENGINE = {
    "SIGNAL_AGGREGATION": {
        "Timeframe_Weighting": {
            "Intraday_Trader": {
                "Minutes": 60,
                "Hours": 30,
                "Days": 10
            },
            "Swing_Trader": {
                "Days": 50,
                "Weeks": 30,
                "Months": 20
            },
            "Long_Term_Investor": {
                "Years": 70,
                "Months": 25,
                "Weeks": 5
            }
        }
    },
    
    "FINAL_RECOMMENDATION": {
        "Structure": {
            "Action": "BUY/SELL/HOLD",
            "Confidence": "0-100",
            "Entry": "Price range",
            "Targets": "[T1, T2, T3]",
            "Stop_Loss": "Price",
            "Position_Size": "₹ amount",
            "Holding_Period": "Days/Weeks/Months",
            "Risk_Reward": "Ratio",
            "Reasoning": "Detailed explanation"
        }
    }
}