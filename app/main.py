from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine, Base, get_db, ExpenseDB
from app.schemas import RawExpenseInput
from app.ai_agent import parse_expense_text

# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="AI Expense Tracker API")

@app.post("/api/expenses/log")
def log_expense(payload: RawExpenseInput, db: Session = Depends(get_db)):
    """
    Receives raw text input, parses it using the AI agent, 
    and saves the extracted expenses into the database.
    """
    # 1. Pass the raw text to the AI Agent
    extracted_data = parse_expense_text(payload.text)
    
    saved_expenses = []
    
    # 2. For each expense found by the AI, save it to the MySQL database
    for item in extracted_data.expenses:
        db_expense = ExpenseDB(
            amount=item.amount,
            category=item.category,
            date=item.date,
            description=item.description
        )
        db.add(db_expense)
        saved_expenses.append(item.model_dump())
        
    db.commit() # Commit the transaction to save changes to the database
    
    # 3. Return the response to the frontend (e.g., iPhone)
    return {
        "status": "success",
        "message": f"Successfully logged {len(saved_expenses)} expenses.",
        "data": saved_expenses
    }

@app.get("/api/expenses/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Calculates and returns the total expenses grouped by category.
    """
    # Group by category and calculate the sum for each one
    results = db.query(
        ExpenseDB.category, 
        func.sum(ExpenseDB.amount).label("total")
    ).group_by(ExpenseDB.category).all()
    
    # Format the results into a clean dictionary
    summary = {row.category: row.total for row in results}
    return {"summary": summary}
