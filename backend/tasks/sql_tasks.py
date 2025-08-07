'''
from celery import shared_task
from services.sql_service import execute_query
from utils.helpers import format_response

@shared_task
def run_sql_query_async(query: str) -> dict:
    """
    Celery task to execute SQL queries asynchronously and format the response.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        dict: Formatted response with query results or error.
    """
    try:
        # Execute the SQL query
        raw_result = execute_query(query)
        # Format the response
        return format_response(success=True, data=raw_result)
    except Exception as e:
        return format_response(success=False, error_message=str(e))
'''

from services.sql_service import execute_query
from utils.helpers import format_response

def run_sql_query(query: str) -> dict:
    """
    Executes SQL queries synchronously and formats the response.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        dict: Formatted response with query results or error.
    """
    try:
        # Execute the SQL query
        raw_result = execute_query(query)
        # Format the response
        return format_response(success=True, data=raw_result)
    except Exception as e:
        return format_response(success=False, error_message=str(e))