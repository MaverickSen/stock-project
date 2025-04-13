from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class TaxAnalyser:
    def __init__(self, api_key: str):
        """
        Initializes the TaxAnalyser tool.

        Args:
            api_key (str): OpenAI API key for tax analysis.
        """
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

    def analyse_selling_strategy(self, recommendations: dict, stock_data: dict) -> str:
        """
        Analyzes the most tax-efficient way to sell stocks.

        Args:
            recommendations (dict): Stock recommendations with buy/hold/sell statuses.
            stock_data (dict): Contains stock tickers, purchase prices, and holding periods.

        Returns:
            str: Suggested tax-efficient strategy.
        """
        if not recommendations or not stock_data:
            return "No sufficient data available for tax analysis."

        # Prioritize stocks explicitly marked for selling
        sell_stocks = {
            ticker: stock_data.get(ticker, {})
            for ticker, status in recommendations.items()
            if status == "Sell"
        }

        # If no Sell stocks found, fallback to Hold/Buy stocks
        if sell_stocks:
            stock_details = "\n".join(
                f"{ticker}: Bought at {details.get('buy_price', 'N/A')} | Held for {details.get('holding_period', 'N/A')} months"
                for ticker, details in sell_stocks.items()
            )

            prompt = f"""
            You are a tax consultant specializing in capital gains tax strategies.
            The user has the following stocks recommended for selling:

            {stock_details}

            Suggest the most tax-efficient way to sell these stocks, considering:
            - Long-term vs short-term capital gains taxes
            - FIFO vs LIFO strategies
            - Any potential tax loss harvesting opportunities

            Provide a detailed recommendation.
            """
        else:
            fallback_stocks = {
                ticker: stock_data.get(ticker, {})
                for ticker, status in recommendations.items()
                if status in {"Hold", "Buy"}
            }

            if not fallback_stocks:
                return "No Sell, Hold, or Buy stocks found to evaluate."

            stock_details = "\n".join(
                f"{ticker}: Bought at {details.get('buy_price', 'N/A')} | Held for {details.get('holding_period', 'N/A')} months"
                for ticker, details in fallback_stocks.items()
            )

            prompt = f"""
            No stocks are explicitly marked for selling, but the user may need to liquidate assets.

            The following stocks are marked as Hold/Buy:
            {stock_details}

            Recommend which, if any, could be sold in a tax-efficient manner, considering:
            - Harvesting losses to offset gains
            - Optimizing for long-term capital gains
            - FIFO vs LIFO strategies

            Provide a detailed recommendation.
            """

        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return response.content if hasattr(response, "content") else str(response)
