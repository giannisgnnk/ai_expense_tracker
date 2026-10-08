
from pydantic import BaseModel, Field
from typing import List
import datetime

# Model representing a single parsed expense item
class ExpenseItem(BaseModel):
    amount: float = Field(description="The exact amount of the expense (e.g., 45.5)")
    category: str = Field(description="The category. Choose ONLY from: Supermarket, Fuel, Food, Entertainment, Bills, Other")
    date: datetime.date = Field(description="The date of the transaction (YYYY-MM-DD).")
    description: str = Field(description="A very short description of the expense (e.g., 'Coffee' or 'Gasoline').")

# Model representing the final output payload from the LLM
class ExpenseExtraction(BaseModel):
    expenses: List[ExpenseItem] = Field(description="A list of expenses found in the text.")

# Model representing the incoming request body from the client (e.g., iPhone/Postman)
class RawExpenseInput(BaseModel):
    text: str