# AI-Powered Financial Assistant for Retirees

This project is an AI-driven financial assistant designed to support **retired individuals** in managing their stock portfolios and making **tax-efficient decisions** related to **IRA withdrawals** and **Required Minimum Distributions (RMDs)**. The assistant uses conversational AI to handle both **stock-related queries** and **tax strategy questions**, all through a streamlined command-line interface.

## Features
* **Dual-Agent Architecture (LangGraph-based)**

  Utilises two specialised agents:

  - stock_advisor.py: Answers portfolio questions, retrieves real-time stock prices, calculates total portfolio value, and provides buy/hold/sell recommendations.

  - tax_advisor.py: Suggests tax-efficient sell strategies based on holding periods and capital gains rules. Can also answer general tax questions.

* **Excel-Based Portfolio Tracking**

  - Users manage their stock data using a simple Excel file stock_portfolio.xlsx with columns: Ticker, Quantity.

  - Automatically fetches and updates current stock prices and total portfolio value.

* **Natural Language Routing (OpenAI GPT-4)**

  - Queries are classified using OpenAI's GPT-4 to route them appropriately to either the stock or tax agent.

  - Built-in LangGraph workflow enables seamless query management and state tracking.

* **Clean CLI Interface**

  - Users interact through a terminal-based interface in main.py.

  - No menu system; users can ask questions freely, e.g., "What is the current value of my portfolio?" or "What is the most tax-efficient way to sell my stocks?"

* **Extensible Architecture**

  - Built with modularity in mind to support future enhancements such as:

    - Document retrieval from a vector database for tax documents

    - Advanced portfolio analytics

    - Web or API deployment

    - Real estate or bond investment analysis

## Tech Stack
* **Core Libraries**: Python, LangChain, LangGraph, OpenAI API (GPT-4), yFinance, Pandas

* **Data Handling**: Excel, Pydantic (for state modeling)

* **Future Integration**: PostgreSQL, Docker, Vector Databases (e.g., FAISS), Unit Testing (Pytest)


## File Structure
<pre>
.
IRARMDWithdrawalPlanner/
│
├── agents/
│   ├── stock_advisor.py
│   └── tax_advisor.py
│
├── tools/
│   ├── stock_fetcher.py
│   ├── portfolio_calculator.py
│   ├── stock_recommender.py
│   └── tax_analyser.py
│
├── stock_portfolio.xlsx
│
├── main.py
├── workflow.py
├── requirements.txt
└── README.md

</pre>

## Getting Started
1. **Install dependencies**

    Create a virtual environment and run:
    
    pip install -r requirements.txt

2. **Set your OpenAI API key**

    Set your environment variable:


    export OPENAI_API_KEY=your_key_here   # for Unix/macOS

    set OPENAI_API_KEY=your_key_here      # for Windows

3. **Prepare your portfolio Excel file**

    Format:


    | Ticker | Quantity |
    |--------|----------|
    | AAPL   | 10       |
    | MSFT   | 5        |

4. **Run the assistant**

   python main.py


## Sample Questions to Ask
* Stock-related:

  - What is the current value of my portfolio?

  - Should I sell TSLA?

  - What is the price of INFY?

* Tax-related:

  - How can I sell stocks with minimum tax impact?

  - What is my capital gains liability if I sell today?

  - How should I withdraw funds from my IRA efficiently?

## Challenges Addressed
  - Routing unstructured natural language queries to specialised agents using GPT-4.

  - Resolving recursive LangGraph flow errors and building robust state transitions.

  - Handling dynamic stock data and computing real-time financial metrics.

  - Designing for a target audience (retired individuals) with simplicity, clarity, and financial accuracy in mind.

## Future Enhancements
  - Integration with a vector database for document-based tax advisory (e.g., IRS forms, state-specific laws).

  - Real estate and bond investment advisory integration.

  - Web dashboard using Flask or FastAPI.

  - CI/CD with GitHub Actions.

  - LoRA fine-tuning for more domain-specific advisory.

