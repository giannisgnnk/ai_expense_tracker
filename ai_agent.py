import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.schemas import ExpenseExtraction

# Load environment variables from the .env file (e.g., GEMINI_API_KEY)
load_dotenv()

# Initialize the Gemini LLM (gemini-1.5-flash is extremely fast and free to use)
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

# Bind the LLM to our Pydantic schema to strictly enforce the JSON output structure
structured_llm = llm.with_structured_output(ExpenseExtraction)

def parse_expense_text(user_text: str) -> ExpenseExtraction:
    """
    Takes the raw user input, passes it to the LLM along with the current date,
    and returns a structured list of expenses based on the Pydantic schema.
    """
    
    # Get today's date so the AI can correctly resolve relative dates like "yesterday" or "today"
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Define the system instructions for the LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are an expert financial assistant. Today's date is: {today}. "
                   "The user will dictate their expenses (most likely in Greek). "
                   "Your task is to extract the data accurately. "
                   "If the user mentions relative time like 'yesterday', 'the day before yesterday', "
                   "or specific days of the week, calculate the exact date based on today's date."),
        ("user", "{text}")
    ])
    
    # Create the execution chain: Prompt -> LLM -> Pydantic Schema
    chain = prompt | structured_llm
    
    # Execute the chain with the user's text and return the structured result
    return chain.invoke({"text": user_text})