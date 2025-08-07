from config.database import get_database_connection

def execute_query(query: str, params: tuple = None) -> list:
    """
    Executes a SQL query on the Microsoft SQL database and returns the results.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to pass to the query for safety.

    Returns:
        list: Query results as a list of dictionaries.

    Raises:
        Exception: If query execution or database connection fails.
    """
    connection = None
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return results
    except Exception as e:
        raise Exception(f"Error executing query: {e}")
    finally:
        if connection:
            connection.close()