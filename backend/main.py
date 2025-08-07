from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.prompt_routes import router as prompt_router
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware
origins = [
    "http://localhost:3000",  # Frontend dev origin
    os.getenv("FRONTEND_URL", "https://your-frontend-domain.com")  # Configurable
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Assistant API"}

# Include routes
app.include_router(prompt_router)

if __name__ == "__main__":
    # Run with reload in development mode
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENV", "development") == "development"
    )