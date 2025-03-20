import yfinance as yf

def get_stock_price(ticker: str) -> float:
    """
    Fetches the current stock price for a given ticker symbol.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The current stock price.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None
