''' 
from services.llm_service import analyze_prompt, generate_sql_from_prompt
from tasks.sql_tasks import run_sql_query_async
from utils.helpers import handle_error

async def handle_prompt(prompt: str) -> str:
    """
    Process the user prompt and return a task ID or direct response.
    
    Args:
        prompt (str): The user prompt.
    
    Returns:
        str: Celery task ID if a query is enqueued, or direct LLM response.
    
    Raises:
        Exception: If processing fails.
    """
    try:
        # Analyze the prompt
        analysis_result = analyze_prompt(prompt)

        if analysis_result["requires_db_query"]:
            # Generate SQL query
            sql_query = generate_sql_from_prompt(prompt)
            # Enqueue the SQL query with Celery
            task = run_sql_query_async.delay(sql_query)
            return task.id
        else:
            # Return LLM response directly
            return analysis_result["response"]
    except Exception as e:
        raise Exception(f"Error processing prompt: {e}")

async def get_task_result(task_id: str) -> dict:
    """
    Retrieve the result of a Celery task.
    
    Args:
        task_id (str): The Celery task ID.
    
    Returns:
        dict: Task result or error status.
    """
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return task_result.result
    return {"status": "pending"}
'''

'''

from services.llm_service import analyze_prompt, generate_sql_from_prompt
from tasks.sql_tasks import run_sql_query  # Updated to import synchronous function
from utils.helpers import handle_error, format_response  # Added format_response for consistency

async def handle_prompt(prompt: str) -> dict:
    """
    Process the user prompt and return a response.
    
    Args:
        prompt (str): The user prompt.
    
    Returns:
        dict: Formatted response with LLM result or database query result.
    
    Raises:
        Exception: If processing fails.
    """
    try:
        # Analyze the prompt
        analysis_result = analyze_prompt(prompt)

        if analysis_result["requires_db_query"]:
            # Generate SQL query
            sql_query = generate_sql_from_prompt(prompt)
            # Execute the SQL query synchronously
            query_result = run_sql_query(sql_query)
            return query_result  # Return the query result directly
        else:
            # Return LLM response directly
            return format_response(success=True, data=analysis_result["response"])
    except Exception as e:
        raise Exception(f"Error processing prompt: {e}")
        
'''
import re

from services.llm_service import (
    analyze_prompt, 
    generate_sql_from_prompt,
    send_prompt_to_openai,
    generate_descriptive_response
)

from tasks.sql_tasks import run_sql_query
from utils.helpers import format_response
from services.embedding_service import get_embedding_from_prompt
from services.search_faiss_index import search_top_embedding_with_metadata
from services.prompt_keywords import get_best_matching_schema
from services.plural import singularize_prompt

async def handle_prompt(prompt: str) -> dict:
    try:
        analysis_result = analyze_prompt(prompt)
        if analysis_result["requires_db_query"]:
            
            # Step 1: Generate embedding for the prompt
            # embedding = get_embedding_from_prompt(prompt)

            # # Step 2: Search for top metadata using the embedding
            # metadata_result = search_top_embedding_with_metadata(embedding)
            
            # # Combine the input prompt with the metadata result to create a new prompt
            # prompt = f"{prompt}\n\nContext:\n{metadata_result['context']}"
            
            # # Step 1: Generate SQL query
            # sql_query = generate_sql_from_prompt(prompt)

            # # Step 2: Execute SQL
            # query_result = run_sql_query(sql_query)

            # # Step 3: Send SQL result back to LLM for explanation
            # descriptive_answer = generate_descriptive_response(prompt, query_result["data"])

            
            prompt = singularize_prompt(prompt)
            try:
                context = get_best_matching_schema(prompt)
        # Combine the input prompt with the context to create a new prompt
            except Exception as e:
                raise RuntimeError(f"Error in get_best_matching_schema: {e}")
            
            try:
    # Step 1: Generate embedding for the prompt
                embedding = get_embedding_from_prompt(prompt)
            except Exception as e:
                raise RuntimeError(f"Error in get_embedding_from_prompt: {e}")

            try:
    # Step 2: Search for top metadata using the embedding
                metadata_result = search_top_embedding_with_metadata(embedding)
            except Exception as e:
                raise RuntimeError(f"Error in search_top_embedding_with_metadata: {e}")

            try:
    # Combine the input prompt with the metadata result to create a new prompt
                if isinstance(metadata_result, list):
                    context_text = "\n\n".join(metadata_result)  # Combine all table descriptions
                else:
                    context_text = str(metadata_result)  # Just in case it's not a list

                prompt = f"{prompt}\n\nContext:\n{context_text}"

            except Exception as e:
                raise RuntimeError(f"Error while constructing new prompt with metadata_result: {e}")

            try:
    # Step 3: Generate SQL query
                sql_query = generate_sql_from_prompt(f"Prompt: {prompt}\n\nContext: {context}")
            except Exception as e:
                raise RuntimeError(f"Error in generate_sql_from_prompt: {e}")

            try:
    # Step 4: Execute SQL
                query_result = run_sql_query(sql_query)
            except Exception as e:
                raise RuntimeError(f"Error in run_sql_query: {e}")

            try:
    # Step 5: Generate descriptive response from SQL result
                descriptive_answer = generate_descriptive_response(prompt, query_result["data"])
            except Exception as e:
                raise RuntimeError(f"Error in generate_descriptive_response: {e}")


            return format_response(success=True, data=descriptive_answer)
        else:
            # Step 4: Direct natural language answer
            direct_answer = send_prompt_to_openai(prompt)
            return format_response(success=True, data=direct_answer)
    except Exception as e:
        return format_response(success=False, error_message=str(e))

