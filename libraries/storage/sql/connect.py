from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from libraries.config import DB_NAME
from .models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

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


# ... (previous code)

def create_database():
    # Connect to the database engine
    engine = connect_sqlalchemy()
    if not engine:
        return

    # Bind the models to the engine
    Base.metadata.bind = engine

    # Create a session to ensure that the engine is bound before creating tables
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the expected table names from the Base
    expected_tables = list(Base.metadata.tables.keys())

    # Use the inspect module to get information about the tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # Check and create tables if they do not exist
    for table_name in expected_tables:
        if table_name not in existing_tables:
            print(f"Table '{table_name}' not found. Creating...")
            Base.metadata.tables[table_name].create(bind=engine)
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists.")

    # Commit the session after creating tables
    session.commit()

    print("Database setup complete.")
