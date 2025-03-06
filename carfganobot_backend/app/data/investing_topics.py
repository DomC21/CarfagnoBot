"""
This module contains the educational content for the investing topics.
"""

INVESTING_TOPICS = {
    "investing_basics": {
        "id": "investing_basics",
        "title": "Investing Basics",
        "description": "Fundamental concepts for beginners in investing",
        "content": """
Investing is the process of allocating resources, usually money, with the expectation of generating income or profit over time. 

Key concepts in investing include:
- Risk and Return: Generally, higher potential returns come with higher risk
- Diversification: Spreading investments across different assets to reduce risk
- Compound Interest: Earning interest on both principal and accumulated interest
- Time Horizon: The length of time you plan to hold an investment

Common investment vehicles for beginners include:
- Stocks: Ownership shares in a company
- Bonds: Loans to companies or governments
- Mutual Funds: Professionally managed investment pools
- ETFs (Exchange-Traded Funds): Baskets of securities that trade like stocks
        """,
        "subtopics": [
            {"id": "stocks", "title": "Stocks"},
            {"id": "bonds", "title": "Bonds"},
            {"id": "mutual_funds", "title": "Mutual Funds"},
            {"id": "etfs", "title": "ETFs"}
        ]
    },
    "stocks": {
        "id": "stocks",
        "title": "Stocks",
        "description": "Understanding stock investments",
        "content": """
Stocks represent ownership shares in a company. When you buy a stock, you become a shareholder and have a claim on part of the company's assets and earnings.

Key concepts about stocks:
- Market Capitalization: The total value of a company's outstanding shares
- Dividends: Payments made by companies to shareholders from profits
- Price-to-Earnings (P/E) Ratio: A valuation metric comparing share price to earnings per share
- Stock Exchanges: Organized markets where stocks are bought and sold

Types of stocks:
- Growth Stocks: Companies expected to grow faster than average
- Value Stocks: Companies that appear undervalued by the market
- Dividend Stocks: Companies that pay regular dividends
- Blue-Chip Stocks: Large, well-established, financially sound companies
        """,
        "subtopics": [
            {"id": "stock_valuation", "title": "Stock Valuation"},
            {"id": "stock_trading", "title": "Stock Trading"},
            {"id": "stock_analysis", "title": "Stock Analysis"}
        ]
    },
    "bonds": {
        "id": "bonds",
        "title": "Bonds",
        "description": "Understanding bond investments",
        "content": """
Bonds are debt securities where investors lend money to an entity (like a corporation or government) for a defined period at a fixed or variable interest rate.

Key concepts about bonds:
- Principal: The amount of money initially invested
- Coupon Rate: The interest rate paid on the bond
- Maturity Date: When the principal amount is returned to the investor
- Yield: The return an investor realizes on a bond

Types of bonds:
- Government Bonds: Issued by national governments
- Municipal Bonds: Issued by states, cities, or counties
- Corporate Bonds: Issued by companies
- Treasury Bills: Short-term government securities
        """,
        "subtopics": [
            {"id": "bond_yields", "title": "Bond Yields"},
            {"id": "bond_risks", "title": "Bond Risks"},
            {"id": "bond_strategies", "title": "Bond Strategies"}
        ]
    },
    "risk_management": {
        "id": "risk_management",
        "title": "Risk Management",
        "description": "Strategies to manage investment risks",
        "content": """
Risk management in investing involves identifying, analyzing, and accepting or mitigating uncertainty in investment decisions.

Key risk management strategies:
- Diversification: Spreading investments across different asset classes
- Asset Allocation: Distributing investments among different asset categories
- Position Sizing: Determining how much to invest in each position
- Stop-Loss Orders: Setting predetermined points to sell and limit losses

Types of investment risks:
- Market Risk: Risk of investments declining due to market factors
- Inflation Risk: Risk of purchasing power declining
- Liquidity Risk: Risk of not being able to sell an investment quickly
- Concentration Risk: Risk of having too much exposure to a single investment
        """,
        "subtopics": [
            {"id": "diversification", "title": "Diversification"},
            {"id": "asset_allocation", "title": "Asset Allocation"},
            {"id": "risk_tolerance", "title": "Risk Tolerance"}
        ]
    },
    "market_analysis": {
        "id": "market_analysis",
        "title": "Market Analysis",
        "description": "Methods to analyze financial markets",
        "content": """
Market analysis involves examining current and historical market data to make informed investment decisions.

Two main approaches to market analysis:
- Fundamental Analysis: Evaluating a security's intrinsic value by examining related economic, financial, and other factors
- Technical Analysis: Analyzing statistical trends gathered from trading activity, such as price movement and volume

Key market indicators:
- Market Indices: Measurements of the value of a section of the stock market
- Economic Indicators: Data points that indicate the health of an economy
- Volatility Indices: Measurements of market's expectation of volatility
- Sector Performance: How different market sectors are performing
        """,
        "subtopics": [
            {"id": "fundamental_analysis", "title": "Fundamental Analysis"},
            {"id": "technical_analysis", "title": "Technical Analysis"},
            {"id": "economic_indicators", "title": "Economic Indicators"}
        ]
    },
    "advanced_concepts": {
        "id": "advanced_concepts",
        "title": "Advanced Concepts",
        "description": "More sophisticated investing strategies and concepts",
        "content": """
Advanced investing concepts build upon basic principles and introduce more sophisticated strategies.

Advanced investing topics:
- Options Trading: Contracts giving the right to buy or sell assets at predetermined prices
- Futures Contracts: Agreements to buy or sell assets at future dates
- Alternative Investments: Non-traditional assets like real estate, commodities, or private equity
- Tax-Efficient Investing: Strategies to minimize tax impact on investments

Advanced portfolio strategies:
- Factor Investing: Targeting specific factors that explain differences in returns
- Tactical Asset Allocation: Actively shifting allocation based on market conditions
- Hedging Strategies: Techniques to offset potential losses in investments
- Sustainable Investing: Considering environmental, social, and governance factors
        """,
        "subtopics": [
            {"id": "options_trading", "title": "Options Trading"},
            {"id": "alternative_investments", "title": "Alternative Investments"},
            {"id": "tax_strategies", "title": "Tax Strategies"}
        ]
    }
}

# Additional subtopics content
SUBTOPICS_CONTENT = {
    "stock_valuation": """
Stock valuation is the process of determining the intrinsic value of a stock. Various methods include:

- Discounted Cash Flow (DCF): Estimates the value based on projected future cash flows
- Price-to-Earnings (P/E): Compares a company's share price to its earnings per share
- Price-to-Book (P/B): Compares a company's market value to its book value
- Price-to-Sales (P/S): Compares a company's market cap to its revenue

No single valuation method is perfect, so investors often use multiple approaches.
    """,
    
    "diversification": """
Diversification is a risk management strategy that mixes a variety of investments within a portfolio.

Benefits of diversification:
- Reduces unsystematic risk (company or industry-specific risk)
- Preserves capital during market downturns
- Provides more stable returns over time

Ways to diversify:
- Across asset classes (stocks, bonds, real estate, etc.)
- Within asset classes (different sectors, industries, company sizes)
- Geographically (domestic and international investments)
- By investment style (growth, value, income)
    """,
    
    "fundamental_analysis": """
Fundamental analysis evaluates a security by measuring its intrinsic value through examining related economic, financial, and other qualitative and quantitative factors.

Key components:
- Economic analysis: Overall economic conditions and trends
- Industry analysis: Industry position, growth potential, and competitive landscape
- Company analysis: Financial statements, management quality, competitive advantages

Common fundamental metrics:
- Earnings per Share (EPS)
- Return on Equity (ROE)
- Debt-to-Equity Ratio
- Free Cash Flow
- Profit Margins
    """
}

# Main topics list for menu display
MAIN_TOPICS_LIST = [
    {"id": "investing_basics", "title": "Investing Basics"},
    {"id": "stocks", "title": "Stocks"},
    {"id": "bonds", "title": "Bonds"},
    {"id": "risk_management", "title": "Risk Management"},
    {"id": "market_analysis", "title": "Market Analysis"},
    {"id": "advanced_concepts", "title": "Advanced Concepts"}
]

# Disclaimer text
DISCLAIMER = "Disclaimer: All information provided by CarfganoBot is for educational purposes only and does not constitute financial advice."
