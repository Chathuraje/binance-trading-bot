from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from libraries.config import DB_NAME

def connect_sqlalchemy():
    """
    Connects to the database using SQLAlchemy.

    Returns:
    - engine: The SQLAlchemy engine object.
    """
    
    try:
        engine = create_engine(f'sqlite:///libraries/storage/sql/{DB_NAME}.db', echo=False)
        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        return None
