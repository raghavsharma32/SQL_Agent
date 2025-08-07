import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database_connection():
    try:
        # Retrieve connection details from environment variables
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_DATABASE")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if not all([server, database, user, password]):
            raise ValueError("Missing database connection details in environment variables.")

        # Set up the connection string
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}"

        # Establish the connection
        connection = pyodbc.connect(connection_string)
        return connection

    except Exception as e:
        raise print(f"Error connecting to the database: {e}")
       
