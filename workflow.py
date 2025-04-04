from langgraph.graph import StateGraph
from pydantic import BaseModel
from agents.stock_agent import StockAgent

# Define the schema for LangGraph
class StockState(BaseModel):
    question: str
    response: str = None

class StockWorkflow:
    def __init__(self, file_path: str, api_key: str):
        """
        Initializes the LangGraph workflow for stock analysis.

        Args:
            file_path (str): Path to the Excel file.
            api_key (str): OpenAI API key.
        """
        self.agent = StockAgent(file_path, api_key)
        
        # Define the workflow graph with the correct state schema
        self.workflow = StateGraph(StockState)

        self.add_nodes()
        self.define_edges()

        # Compile the graph
        self.executor = self.workflow.compile()

    def fetch_stock_response(self, state: StockState) -> StockState:
        """Delegates user questions to StockAgent."""
        return StockState(
            question=state.question, 
            response=self.agent.ask_question(state.question)
        )

    def add_nodes(self):
        """Define nodes for the LangGraph workflow."""
        self.workflow.add_node("fetch_stock_response", self.fetch_stock_response)

    def define_edges(self):
        """Define edges for workflow transitions."""
        self.workflow.set_entry_point("fetch_stock_response")

    def run(self, user_question: str) -> str:
        """Runs the LangGraph workflow with a user's question."""
        initial_state = StockState(question=user_question)
        
        # Execute the workflow
        result = self.executor.invoke(initial_state)

        # Extract response correctly whether it's an object or dict
        if isinstance(result, StockState):
            return result.response
        elif isinstance(result, dict) and "response" in result:
            return result["response"]
        else:
            return "Error: Could not process the response."
