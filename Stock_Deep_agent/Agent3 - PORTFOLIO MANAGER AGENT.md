PORTFOLIO_MANAGEMENT = {
    "POSITION_SIZING": {
        "Kelly_Criterion": {
            "Formula": "f = (bp - q) / b",
            "f": "Fraction of capital to bet",
            "b": "Odds (reward/risk)",
            "p": "Win probability",
            "q": "Loss probability (1-p)",
            "Practical": "Use 25-50% of Kelly (conservative)"
        },
        "2%_Risk_Rule": "Never risk more than 2% per trade",
        "Position_Limits": {
            "Single_Stock": "Max 10% of portfolio",
            "Single_Sector": "Max 30% of portfolio"
        }
    },
    
    "RISK_MANAGEMENT": {
        "Stop_Loss_Types": {
            "Fixed_%": "Entry - 5%",
            "ATR_Based": "Entry - (2 × ATR)",
            "Support_Based": "Below key support level"
        },
        "Trailing_Stop": "Lock profits as stock rises",
        "Portfolio_Stop": "Exit all positions if portfolio down 10%"
    },
    
    "REBALANCING": {
        "Frequency": "Monthly or when allocation drifts >5%",
        "Tax_Optimization": "Avoid selling before 1 year (LTCG benefit)"
    }
}