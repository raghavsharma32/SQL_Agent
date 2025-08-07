import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_response(success: bool, data=None, error_message=None) -> dict:
    """
    Formats a response dictionary for consistency across the application.
    
    Args:
        success (bool): Indicates if the operation was successful.
        data (any, optional): The data to include if successful.
        error_message (str, optional): Error message if the operation failed.
    
    Returns:
        dict: A standardized response dictionary.
    """
    return {
        "success": success,
        "data": data if success else None,
        "error": error_message if not success else None
    }

def handle_error(exception: Exception, custom_message: str = None) -> dict:
    """
    Handles errors by logging them and returning a formatted error response.
    
    Args:
        exception (Exception): The exception to handle.
        custom_message (str, optional): Custom error message to include.
    
    Returns:
        dict: A formatted error response.
    """
    error_message = custom_message or str(exception)
    logger.error(f"Error occurred: {error_message}\n{traceback.format_exc()}")
    return format_response(success=False, error_message=error_message)

def validate_input(data: dict, required_keys: list) -> tuple:
    """
    Validates input data by checking for required keys.
    
    Args:
        data (dict): The input data to validate.
        required_keys (list): List of required keys.
    
    Returns:
        tuple: (bool, str) - Validation success and error message (if any).
    """
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return False, f"Missing required keys: {', '.join(missing_keys)}"
    return True, None