from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from tools.tax_analyser import TaxAnalyser

class TaxAdvisor:
    def __init__(self, api_key: str):
        """
        Initializes the TaxAdvisor agent.

        Args:
            api_key (str): OpenAI API key for tax analysis.
        """
        self.tax_analyser = TaxAnalyser(api_key)
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

    def analyse_tax_strategy(self, recommendations: dict, stock_data: dict) -> str:
        """
        Uses the tax_analyser tool to determine a tax-efficient selling strategy.

        Args:
            recommendations (dict): Stock recommendations (buy/hold/sell).
            stock_data (dict): Stock details including buy price & holding period.

        Returns:
            str: Tax-efficient stock selling strategy.
        """
        return self.tax_analyser.analyse_selling_strategy(recommendations, stock_data)

    def ask_tax_question(self, question: str) -> str:
        """
        Allows users to query ChatGPT for tax-related questions.

        Args:
            question (str): User's tax-related query.

        Returns:
            str: ChatGPT's response.
        """
        prompt = f"""
        You are a tax expert with deep knowledge of stock taxation.
        The user has a tax-related question:
        
        {question}

        Provide a clear and accurate answer, following best tax practices.
        """
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)

        return response.content if hasattr(response, "content") else str(response)
