import pandas as pd
from tools.stock_fetcher import get_stock_price

def calculate_portfolio_value(file_path: str) -> dict:
    """
    Reads stock tickers and quantities from an Excel file and calculates total portfolio value.

    Args:
        file_path (str): Path to the Excel file containing stock data.

    Returns:
        dict: A dictionary with individual stock values, quantities, and total portfolio value.
    """
    try:
        df = pd.read_excel(file_path)
        total_value = 0
        stock_values = {}
        quantities = {}  # Store quantities

        for _, row in df.iterrows():
            ticker = row["Ticker"]
            quantity = row["Quantity"]
            price = get_stock_price(ticker)

            if price is not None:
                stock_total = price * quantity
                stock_values[ticker] = stock_total
                quantities[ticker] = quantity  # Store quantity
                total_value += stock_total

        return {
            "stocks": stock_values,
            "quantities": quantities,  # Return quantities
            "total_value": round(total_value, 2)
        }

    except Exception as e:
        print(f"Error calculating portfolio value: {e}")
        return None