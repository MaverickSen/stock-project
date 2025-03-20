from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from tools.portfolio_calculator import calculate_portfolio_value

class StockAgent:
    def __init__(self, file_path: str, api_key: str):
        """
        Initializes the StockAgent with a file path for stock data and an API key.

        Args:
            file_path (str): Path to the Excel file containing stock data.
            api_key (str): OpenAI API key for LangGraph interaction.
        """
        self.file_path = file_path
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

    def ask_question(self, question: str) -> str:
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

        # Calculate stock prices from total value and quantities
        stock_prices = {ticker: stock_values[ticker] / quantities[ticker] for ticker in stock_values}

        stock_prices_str = "\n".join([f"{ticker}: {round(price, 2)}" for ticker, price in stock_prices.items()])
        stock_values_str = "\n".join([f"{ticker}: {round(value, 2)}" for ticker, value in stock_values.items()])

        prompt_content = (
            f"Here is the stock data:\n\n"
            f"Stock Prices:\n{stock_prices_str}\n\n"
            f"Stock Values:\n{stock_values_str}\n\n"
            f"Total Portfolio Value: {round(total_value, 2)}\n\n"
            f"You can now ask questions about this portfolio."
        )

        # Format input for LLM
        user_prompt = f"{prompt_content}\n\nUser's Question: {question}"
        messages = [HumanMessage(content=user_prompt)]
        response = self.llm.invoke(messages)

        return response.content if hasattr(response, "content") else str(response)
