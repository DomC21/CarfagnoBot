"""
This module contains enhanced educational content for investing topics with content
tailored to different user proficiency levels.
"""
from typing import Dict, List, Any

# Enhanced investing topics with content for different proficiency levels
ENHANCED_INVESTING_TOPICS: Dict[str, Dict[str, Any]] = {
    "investing_basics": {
        "id": "investing_basics",
        "title": "Investing Basics",
        "description": "Fundamental concepts for beginners in investing",
        "content": {
            "beginner": """
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
            "intermediate": """
Investing is the process of allocating resources, usually money, with the expectation of generating income or profit over time.

Beyond the basics, intermediate investors should understand:
- Asset Allocation: The strategic distribution of investments across different asset classes based on goals, risk tolerance, and time horizon
- Rebalancing: Periodically adjusting your portfolio to maintain your target asset allocation
- Dollar-Cost Averaging: Investing a fixed amount regularly regardless of market conditions
- Tax-Efficient Investing: Strategies to minimize the tax impact on your investment returns

As you progress, consider exploring:
- Index Investing vs. Active Management: Understanding the differences in approach and performance
- Investment Fees and Expenses: How costs affect long-term returns
- Risk-Adjusted Returns: Evaluating investments based on return relative to risk
- Modern Portfolio Theory: How diversification can optimize returns for a given level of risk
            """,
            "advanced": """
Investing is the process of allocating resources, usually money, with the expectation of generating income or profit over time.

For advanced investors, consider these sophisticated concepts:
- Factor Investing: Targeting specific factors (value, size, momentum, quality) that explain differences in returns
- Efficient Market Hypothesis: Understanding market efficiency and its implications for investment strategies
- Behavioral Finance: How psychological factors influence investor decisions and market outcomes
- Alternative Investments: Incorporating private equity, hedge funds, real estate, and commodities

Advanced portfolio management concepts:
- Strategic vs. Tactical Asset Allocation: Long-term positioning versus short-term adjustments
- Portfolio Optimization: Using mathematical models to maximize returns for a given level of risk
- Correlation and Covariance: Understanding how assets move in relation to each other
- Stress Testing: Analyzing how portfolios might perform under extreme market conditions
- Liability-Driven Investing: Matching investment strategy to future financial obligations
            """
        },
        "subtopics": [
            {"id": "stocks", "title": "Stocks"},
            {"id": "bonds", "title": "Bonds"},
            {"id": "mutual_funds", "title": "Mutual Funds"},
            {"id": "etfs", "title": "ETFs"},
            {"id": "compound_interest", "title": "Compound Interest"},
            {"id": "asset_allocation", "title": "Asset Allocation"}
        ],
        "follow_up_questions": [
            "What's the difference between stocks and bonds?",
            "How does compound interest work?",
            "What is an appropriate asset allocation for a beginner?",
            "How much money do I need to start investing?",
            "What are the tax implications of investing?"
        ],
        "educational_links": [
            {
                "title": "The Power of Compound Interest Calculator",
                "description": "Interactive tool to visualize how compound interest grows over time",
                "url": "https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator"
            },
            {
                "title": "Asset Allocation Basics",
                "description": "Guide to understanding how to distribute investments across asset classes",
                "url": "https://www.investopedia.com/managing-wealth/achieve-optimal-asset-allocation/"
            }
        ]
    },
    "stocks": {
        "id": "stocks",
        "title": "Stocks",
        "description": "Understanding stock investments",
        "content": {
            "beginner": """
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
            "intermediate": """
Stocks represent ownership shares in a company, giving shareholders a claim on the company's assets and earnings.

Intermediate stock investors should understand:
- Fundamental Analysis: Evaluating a company's financial health through metrics like:
  * Earnings Per Share (EPS): A company's profit divided by outstanding shares
  * Return on Equity (ROE): How efficiently a company uses equity to generate profits
  * Debt-to-Equity Ratio: A company's financial leverage
  * Free Cash Flow: Cash generated after accounting for capital expenditures

- Stock Classifications:
  * Large-Cap (>$10B): Generally more stable, lower growth potential
  * Mid-Cap ($2B-$10B): Balance of growth and stability
  * Small-Cap (<$2B): Higher growth potential with higher risk
  * Sector and Industry: How companies are categorized by business activity

- Dividend Investing Strategies:
  * Dividend Yield: Annual dividend divided by share price
  * Dividend Growth: Companies that consistently increase dividends
  * Dividend Payout Ratio: Percentage of earnings paid as dividends
            """,
            "advanced": """
Stocks represent ownership shares in a company, and advanced investors should understand the nuanced approaches to stock analysis and portfolio construction.

Advanced stock investing concepts:
- Quantitative Analysis:
  * Discounted Cash Flow (DCF) Modeling: Valuing a company based on projected future cash flows
  * Multi-Factor Models: Using statistical methods to identify drivers of returns
  * Regression Analysis: Measuring relationships between variables affecting stock performance

- Advanced Trading Strategies:
  * Pairs Trading: Exploiting price relationships between related stocks
  * Statistical Arbitrage: Using mathematical models to identify pricing inefficiencies
  * Event-Driven Strategies: Trading based on corporate events like mergers or earnings

- Corporate Actions and Their Impact:
  * Share Buybacks: When companies repurchase their own shares
  * Stock Splits and Reverse Splits: Changes in share count and price
  * Spinoffs: When a company separates a division into a new independent entity
  * Mergers and Acquisitions: How corporate combinations affect shareholder value

- Global Equity Markets:
  * Cross-Border Investing: Opportunities and challenges in international markets
  * Currency Effects: How exchange rates impact returns
  * Market Structure Differences: Variations in trading mechanisms and regulations
            """
        },
        "subtopics": [
            {"id": "stock_valuation", "title": "Stock Valuation"},
            {"id": "stock_trading", "title": "Stock Trading"},
            {"id": "stock_analysis", "title": "Stock Analysis"},
            {"id": "dividend_investing", "title": "Dividend Investing"},
            {"id": "growth_vs_value", "title": "Growth vs. Value Investing"}
        ],
        "follow_up_questions": [
            "How do I evaluate if a stock is overvalued or undervalued?",
            "What's the difference between technical and fundamental analysis?",
            "How do dividends affect stock returns?",
            "What factors should I consider before buying a stock?",
            "How do economic conditions affect the stock market?"
        ],
        "educational_links": [
            {
                "title": "Financial Statement Analysis Guide",
                "description": "Learn how to read and analyze company financial statements",
                "url": "https://www.investopedia.com/terms/f/financial-statement-analysis.asp"
            },
            {
                "title": "Stock Valuation Methods Comparison",
                "description": "Overview of different approaches to determining a stock's intrinsic value",
                "url": "https://corporatefinanceinstitute.com/resources/valuation/stock-valuation-methods-top-companies-use/"
            }
        ]
    }
}

# Enhanced subtopics content with proficiency levels
ENHANCED_SUBTOPICS_CONTENT = {
    "stock_valuation": {
        "beginner": """
Stock valuation is the process of determining the intrinsic value of a stock. Various methods include:

- Price-to-Earnings (P/E): Compares a company's share price to its earnings per share
- Price-to-Book (P/B): Compares a company's market value to its book value
- Price-to-Sales (P/S): Compares a company's market cap to its revenue
- Dividend Yield: Annual dividends per share divided by share price

No single valuation method is perfect, so investors often use multiple approaches.
        """,
        "intermediate": """
Stock valuation involves determining a stock's intrinsic value using various methodologies.

Intermediate valuation concepts:
- Discounted Cash Flow (DCF): Estimates value based on projected future cash flows
  * Forecasting future earnings and cash flows
  * Determining an appropriate discount rate
  * Calculating terminal value

- Relative Valuation Multiples:
  * Enterprise Value to EBITDA (EV/EBITDA)
  * Price to Earnings Growth (PEG) ratio
  * Free Cash Flow Yield

- Industry-Specific Metrics:
  * REITs: Funds From Operations (FFO)
  * Banks: Price to Book Value, Net Interest Margin
  * Tech: Monthly Active Users, Customer Acquisition Cost
        """,
        "advanced": """
Advanced stock valuation incorporates sophisticated modeling techniques and adjustments to standard methodologies.

Advanced valuation concepts:
- Multi-Stage DCF Models:
  * Variable growth rate assumptions across different periods
  * Scenario analysis with probability-weighted outcomes
  * Monte Carlo simulations for range of possible values

- Adjusted Valuation Metrics:
  * Economic Value Added (EVA)
  * Return on Invested Capital (ROIC) vs. Weighted Average Cost of Capital (WACC)
  * Cyclically Adjusted Price-to-Earnings (CAPE) ratio

- Sum-of-the-Parts Analysis:
  * Valuing different business segments separately
  * Accounting for non-operating assets and liabilities
  * Conglomerate discount considerations

- Real Options Valuation:
  * Applying options pricing models to business opportunities
  * Valuing flexibility in business decisions
  * Incorporating strategic value beyond cash flows
        """
    },
    "diversification": {
        "beginner": """
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
        "intermediate": """
Diversification is a risk management strategy that involves spreading investments across various assets to reduce exposure to any single risk.

Intermediate diversification concepts:
- Correlation Analysis:
  * Understanding correlation coefficients (-1 to +1)
  * Finding assets with low or negative correlations
  * Building a correlation matrix for portfolio components

- International Diversification:
  * Developed vs. Emerging Markets
  * Currency considerations and hedging
  * Single-country vs. regional exposure

- Alternative Asset Diversification:
  * Real Estate Investment Trusts (REITs)
  * Commodities and natural resources
  * Preferred stocks and convertible securities
        """,
        "advanced": """
Advanced diversification goes beyond simple asset allocation to incorporate sophisticated risk management techniques.

Advanced diversification concepts:
- Efficient Frontier Optimization:
  * Mean-variance optimization techniques
  * Constraints and practical implementation challenges
  * Resampling methods to address estimation error

- Factor-Based Diversification:
  * Identifying and targeting specific risk premia
  * Style factors: value, size, momentum, quality, volatility
  * Macroeconomic factors: inflation, interest rates, economic growth

- Tail Risk Diversification:
  * Protecting against extreme market events
  * Asymmetric return profiles using options and other derivatives
  * Crisis alpha strategies and managed futures

- Dynamic Diversification:
  * Regime-based asset allocation
  * Risk parity approaches
  * Adaptive asset allocation based on changing correlations
        """
    }
}

# Main topics list for menu display
ENHANCED_MAIN_TOPICS_LIST = [
    {"id": "investing_basics", "title": "Investing Basics", "difficulty": "beginner"},
    {"id": "stocks", "title": "Stocks", "difficulty": "beginner"},
    {"id": "bonds", "title": "Bonds", "difficulty": "beginner"},
    {"id": "risk_management", "title": "Risk Management", "difficulty": "intermediate"},
    {"id": "market_analysis", "title": "Market Analysis", "difficulty": "intermediate"},
    {"id": "advanced_concepts", "title": "Advanced Concepts", "difficulty": "advanced"}
]

# Educational resources by topic
EDUCATIONAL_RESOURCES = {
    "investing_basics": [
        {
            "title": "The Power of Compound Interest",
            "url": "https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator",
            "description": "Interactive calculator to visualize compound growth",
            "difficulty": "beginner"
        },
        {
            "title": "Asset Allocation Guide",
            "url": "https://www.investopedia.com/managing-wealth/achieve-optimal-asset-allocation/",
            "description": "Comprehensive guide to distributing investments",
            "difficulty": "intermediate"
        },
        {
            "title": "Modern Portfolio Theory Explained",
            "url": "https://www.investopedia.com/terms/m/modernportfoliotheory.asp",
            "description": "Academic framework for portfolio construction",
            "difficulty": "advanced"
        }
    ],
    "stocks": [
        {
            "title": "How to Read a Stock Chart",
            "url": "https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp",
            "description": "Guide to understanding stock price charts",
            "difficulty": "beginner"
        },
        {
            "title": "Financial Statement Analysis",
            "url": "https://www.investopedia.com/terms/f/financial-statement-analysis.asp",
            "description": "How to analyze company financial reports",
            "difficulty": "intermediate"
        },
        {
            "title": "Discounted Cash Flow Modeling",
            "url": "https://corporatefinanceinstitute.com/resources/valuation/dcf-model-training-free-guide/",
            "description": "Advanced stock valuation technique",
            "difficulty": "advanced"
        }
    ]
}

# Disclaimer text
ENHANCED_DISCLAIMER = "Disclaimer: All information provided by CarfganoBot is for educational purposes only and does not constitute financial advice."
