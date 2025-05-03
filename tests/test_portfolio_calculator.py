import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Ensure tools/ is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.portfolio_calculator import calculate_portfolio_value


@patch("tools.portfolio_calculator.get_stock_price")
@patch("tools.portfolio_calculator.pd.read_excel")
def test_calculate_portfolio_value_returns_correct_result(mock_read_excel, mock_get_stock_price):
    # Simulate Excel file content
    data = pd.DataFrame({
        "Ticker": ["AAPL", "GOOGL", "MSFT"],
        "Quantity": [10, 5, 8]
    })
    mock_read_excel.return_value = data

    # Mock stock prices
    mock_get_stock_price.side_effect = [150.0, 2800.0, 300.0]  # Prices for AAPL, GOOGL, MSFT

    result = calculate_portfolio_value("fake_path.xlsx")

    assert result is not None
    assert result["quantities"] == {"AAPL": 10, "GOOGL": 5, "MSFT": 8}
    assert result["stocks"] == {
        "AAPL": 150.0 * 10,
        "GOOGL": 2800.0 * 5,
        "MSFT": 300.0 * 8
    }
    expected_total = round(150.0 * 10 + 2800.0 * 5 + 300.0 * 8, 2)
    assert result["total_value"] == expected_total


@patch("tools.portfolio_calculator.pd.read_excel", side_effect=Exception("File error"))
def test_calculate_portfolio_value_file_error_returns_none(mock_read_excel):
    result = calculate_portfolio_value("invalid.xlsx")
    assert result is None
