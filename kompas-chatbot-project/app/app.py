# chatbot_project/app/api.py

"""
API Layer for Kompas Chatbot
Provides REST endpoints for the hybrid chatbot system.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pipeline.hybrid_router import route_query

router = APIRouter()

class QueryRequest(BaseModel):
    prompt: str

@router.get("/health")
async def health_check():
    """Simple endpoint to check if API and pipelines are alive."""
    return {"status": "ok", "message": "Chatbot API running successfully."}

@router.post("/query")
async def handle_query(request: QueryRequest):
    """
    Main endpoint: receives a user query,
    routes it to the correct pipeline (SQL or RAG),
    and returns the chatbot’s natural-language answer.
    """
    try:
        prompt = request.prompt.strip()
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

        response = route_query(prompt)
        return {"answer": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
