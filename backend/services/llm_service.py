import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo

def send_prompt_to_openai(prompt: str) -> str:
    """
    Sends a user prompt to the OpenAI API and returns the response.
    
    Args:
        prompt (str): The user prompt to send to the API.
    
    Returns:
        str: The response from the OpenAI API.
    
    Raises:
        Exception: If the API call fails.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error interacting with OpenAI API: {e}")

def generate_sql_from_prompt(prompt: str) -> str:
    """
    Generates an SQL query from a user prompt using the OpenAI API.
    
    Args:
        prompt (str): The user prompt describing the SQL query.
    
    Returns:
        str: The generated SQL query.
    
    Raises:
        Exception: If SQL generation fails.
    """
    sql_prompt = f"You are a SQL expert. Use the prompt and context defined to generate a relateful SQL query, {prompt}"
    return send_prompt_to_openai(sql_prompt)

def analyze_prompt(prompt: str) -> dict:
    """
    Analyzes a prompt to determine if it requires a database query.
    
    Args:
        prompt (str): The user prompt to analyze.
    
    Returns:
        dict: Contains 'requires_db_query' (bool) and 'response' (str).
    """
    analysis_prompt = (
        f"Determine if this prompt requires a database query: '{prompt}'. "
        "Respond with 'Yes' or 'No' and provide a brief explanation."
    )
    response = send_prompt_to_openai(analysis_prompt)
    requires_db = "Yes" in response
    return {"requires_db_query": requires_db, "response": response}

def generate_descriptive_response(original_prompt: str, data: list) -> str:
    """
    Sends the SQL data and original prompt to LLM for a human-readable answer.

    Args:
        original_prompt (str): The user prompt.
        data (list): SQL query result to describe.

    Returns:
        str: Natural language explanation from LLM.
    """
    data_str = str(data)[:1500]  # Limit data size to avoid token issues
    prompt = (
        f"The user asked: '{original_prompt}'.\n"
        f"The SQL result is: {data_str}.\n"
        "Please provide a human-readable explanation or summary of this data."
    )
    return send_prompt_to_openai(prompt)
