# scripts/db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Database URL (from .env)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine
engine = create_engine(DATABASE_URL)

# Create session maker
Session = sessionmaker(bind=engine)

def get_session():
    """Get a new database session."""
    return Session()

def get_engine():
    return engine