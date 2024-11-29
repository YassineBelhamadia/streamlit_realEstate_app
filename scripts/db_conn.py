# scripts/db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


# Retrieve the environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')  # Default to localhost if not set
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'admin')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')


# Database URL (from .env)
DATABASE_URL = db_url = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create the engine
engine = create_engine(DATABASE_URL)

# Create session maker
Session = sessionmaker(bind=engine)

def get_session():
    """Get a new database session."""
    return Session()

def get_engine():
    return engine