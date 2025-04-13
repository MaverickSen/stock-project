from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import pandas as pd
from tools.portfolio_calculator import calculate_portfolio_value
from tools.stock_recommender import StockRecommender

class StockAdvisor:
    def __init__(self, file_path: str, api_key: str):
        """
        Initializes the StockAdvisor with stock data and an API key.

        Args:
            file_path (str): Path to the Excel file containing stock data.
            api_key (str): OpenAI API key for LangGraph interaction.
        """
        self.file_path = file_path
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)
        self.recommender = StockRecommender()

        self.recommender.update_excel_with_recommendations(self.file_path)

    def get_stock_recommendations(self):
        """
        Reads recommendations from the updated Excel file.

        Returns:
            dict: A dictionary of recommendations for all stocks.
        """
        try:
            df = pd.read_excel(self.file_path)
            if "Ticker" not in df.columns or "Recommendation" not in df.columns:
                raise ValueError("Excel file must contain 'Ticker' and 'Recommendation' columns.")

            return dict(zip(df["Ticker"], df["Recommendation"]))
        except Exception as e:
            return {"error": f"Failed to read recommendations: {e}"}

    def ask_stock_question(self, question: str) -> str:
        """
        Uses LangChain to generate a response to stock-related questions.

        Args:
            question (str): User's query about the stocks.

        Returns:
            str: The response from ChatGPT.
        """
        portfolio_data = calculate_portfolio_value(self.file_path)

        if not portfolio_data:
            return "Error: Could not retrieve portfolio data."

        stock_values = portfolio_data["stocks"]
        quantities = portfolio_data["quantities"]
        total_value = portfolio_data["total_value"]

        # Calculate stock prices
        stock_prices = {ticker: stock_values[ticker] / quantities[ticker] for ticker in stock_values}

        # Read stock recommendations from Excel
        recommendations = self.get_stock_recommendations()
        recommendation_str = "\n".join([f"{ticker}: {rec}" for ticker, rec in recommendations.items()])

        stock_prices_str = "\n".join([f"{ticker}: {round(price, 2)}" for ticker, price in stock_prices.items()])
        stock_values_str = "\n".join([f"{ticker}: {round(value, 2)}" for ticker, value in stock_values.items()])

        # Prepare context for the prompt
        context = (
            f"Here is the stock data:\n\n"
            f"Stock Prices:\n{stock_prices_str}\n\n"
            f"Stock Values:\n{stock_values_str}\n\n"
            f"Total Portfolio Value: {round(total_value, 2)}\n\n"
            f"Stock Recommendations:\n{recommendation_str}\n\n"
            f"You can now ask questions about this portfolio."
        )

        prompt = (
            f"{context}"
            f"The user has asked the following question about their portfolio:\n"
            f"{question}\n\n"
            f"Please respond clearly and concisely."
        )

        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return response.content if hasattr(response, "content") else str(response)
