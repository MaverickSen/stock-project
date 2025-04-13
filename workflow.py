from langgraph.graph import StateGraph
from pydantic import BaseModel
from agents.stock_advisor import StockAdvisor
from agents.tax_advisor import TaxAdvisor
from openai import OpenAI
from typing import Literal


class PortfolioState(BaseModel):
    stock_question: str = None
    stock_response: str = None
    tax_question: str = None
    tax_response: str = None


class PortfolioWorkflow:
    def __init__(self, file_path: str, api_key: str):
        self.stock_agent = StockAdvisor(file_path, api_key)
        self.tax_agent = TaxAdvisor(api_key)
        self.openai_client = OpenAI(api_key=api_key)

        # Setup stock workflow
        stock_graph = StateGraph(PortfolioState)
        stock_graph.add_node("fetch_stock_response", self.fetch_stock_response)
        stock_graph.set_entry_point("fetch_stock_response")
        self.stock_executor = stock_graph.compile()

        # Setup tax workflow
        tax_graph = StateGraph(PortfolioState)
        tax_graph.add_node("fetch_tax_response", self.fetch_tax_response)
        tax_graph.set_entry_point("fetch_tax_response")
        self.tax_executor = tax_graph.compile()

    def fetch_stock_response(self, state: PortfolioState) -> PortfolioState:
        response = self.stock_agent.ask_stock_question(state.stock_question)
        return PortfolioState(stock_question=state.stock_question, stock_response=response)

    def fetch_tax_response(self, state: PortfolioState) -> PortfolioState:
        response = self.tax_agent.ask_tax_question(state.tax_question)
        return PortfolioState(tax_question=state.tax_question, tax_response=response)

    def classify_query(self, query: str) -> Literal["stock", "tax"]:
        """Uses GPT-4 to classify the query type."""
        system_prompt = (
            "You are a classifier that determines whether a user query is about stocks or taxes. "
            "Only respond with 'stock' or 'tax'."
        )

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=1,
            temperature=0
        )

        result = response.choices[0].message.content.strip().lower()
        return "tax" if "tax" in result else "stock"

    def handle_query(self, question: str) -> str:
        """Routes query to the appropriate agent using GPT classification."""
        query_type = self.classify_query(question)

        if query_type == "tax":
            state = PortfolioState(tax_question=question)
            result = self.tax_executor.invoke(state)
            return result["tax_response"]
        else:
            state = PortfolioState(stock_question=question)
            result = self.stock_executor.invoke(state)
            return result["stock_response"]
