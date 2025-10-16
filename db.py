"""Database setup and connection module"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. See .env.example")

# Create SQLAlchemy engine for connecting to PostgreSQL
engine = create_engine(DATABASE_URL, echo=False)

# Session factory for managing DB sessions
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Helper function to get a database session
def get_session():
    return SessionLocal()
