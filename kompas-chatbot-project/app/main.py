# chatbot_project/app/main.py

"""
Main entry point for Kompas Chatbot API
Run this with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from .app import router

# Initialize the FastAPI app
app = FastAPI(
    title="Kompas Chatbot API",
    description="Hybrid RAG + SQL chatbot for Indonesia Laws and Regulations.",
    version="1.0.0"
)

# Register API routes
app.include_router(router, prefix="/api", tags=["Chatbot"])

# Optional root route
@app.get("/")
async def root():
    return {
        "message": "Welcome to Kompas Chatbot API!",
        "endpoints": {
            "health_check": "/api/health",
            "query": "/api/query"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
