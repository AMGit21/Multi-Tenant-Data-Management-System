from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO)

# Dictionary to hold session makers for different users
DATABASE_SESSIONS: Dict[str, sessionmaker] = {}

@lru_cache(maxsize=100)  # Cache up to 100 sessions
def get_session(username: str, database_url: str):
    """Retrieve a session maker from the cache, creating it if necessary."""
    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test the connection
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return SessionLocal
    except SQLAlchemyError as e:
        logging.error(f"Failed to create session for user {username} with URL {database_url}: {str(e)}")
        raise

# Assuming DATABASE_POOLS also stores the database URL
DATABASE_POOLS: Dict[str, dict] = {}

def add_database(username: str, database_url: str):
    """Add a new connection pool and session maker to the DATABASE_POOLS dictionary for a given username."""
    try:
        engine = create_engine(database_url, pool_size=10, max_overflow=20)  # Adjust pool_size and max_overflow as needed
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test the connection
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        DATABASE_POOLS[username] = {
            "session_local": SessionLocal,
            "database_url": database_url
        }
        logging.info(f"Database pool added for user {username} with URL: {database_url}")
    except SQLAlchemyError as e:
        logging.error(f"Failed to add database pool for user {username} with URL {database_url}: {str(e)}")
        raise
