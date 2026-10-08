import os
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base


#read the database URL from Render
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./expenses.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#MySQL table for expenses
class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), index=True, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()