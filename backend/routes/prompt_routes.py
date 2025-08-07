'''
from fastapi import APIRouter, HTTPException
from controllers.prompt_controller import handle_prompt, get_task_result
from models import PromptRequest

router = APIRouter()

@router.post("/prompt")
async def create_prompt(request: PromptRequest):
    """
    Accepts a user prompt and processes it.

    Args:
        request (PromptRequest): The request body containing the prompt.

    Returns:
        dict: Contains task_id if enqueued, or direct response.
    """
    try:
        result = await handle_prompt(request.prompt)
        return {"task_id": result} if isinstance(result, str) else {"response": result}
    except Exception as e:
        import traceback
        print("❌ Error in /prompt:", str(e))
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/result/{task_id}")
async def get_result(task_id: str):
    """
    Retrieves the result of a task by its ID.

    Args:
        task_id (str): The Celery task ID.

    Returns:
        dict: Task result or status.
    """
    try:
        result = await get_task_result(task_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''


from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from controllers.prompt_controller import handle_prompt  # get_task_result removed
from models import PromptRequest

router = APIRouter()

@router.post("/prompt")
async def create_prompt(request: PromptRequest):
    """
    Accepts a user prompt and processes it synchronously.

    Args:
        request (PromptRequest): The request body containing the prompt.

    Returns:
        dict: Contains direct response from the handler.
    """
    try:
        result = await handle_prompt(request.prompt)
        return {"response": result}
    except Exception as e:
        import traceback
        print("❌ Error in /prompt:", str(e))
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
    


'''
@router.get("/result")
async def get_result():
    """
    Returns the result directly without using an ID.
    """
    try:
        result = prompt_store.get_latest()  # Assuming a method to get the latest result
        if result is None:
            raise HTTPException(status_code=404, detail="Result not found")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
'''