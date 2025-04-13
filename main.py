import os
from workflow import PortfolioWorkflow

EXCEL_FILE_PATH = "stock_portfolio.xlsx"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    print("Welcome to the Stock Portfolio Assistant!")
    print("Ask any stock or tax-related question. Type 'exit' to quit.\n")

    workflow = PortfolioWorkflow(EXCEL_FILE_PATH, OPENAI_API_KEY)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = workflow.handle_query(user_input)
        print(f"\nAssistant: {response}\n")
