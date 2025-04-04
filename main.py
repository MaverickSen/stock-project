import os
from workflow import StockWorkflow

# Configuration
EXCEL_FILE_PATH = "stock_portfolio.xlsx"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this is set in your environment variables

if __name__ == "__main__":
    print("Welcome to the Stock Portfolio Chat Assistant!")
    
    # Initialize workflow
    workflow = StockWorkflow(EXCEL_FILE_PATH, OPENAI_API_KEY)

    while True:
        user_input = input("\nAsk a question about your portfolio (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Send user input to workflow and get response
        response = workflow.run(user_input)
        
        # Display the response in the desired format
        print(f"\nAssistant: {response}")
