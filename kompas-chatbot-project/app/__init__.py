# chatbot_project/app/__init__.py

"""
Initialize the app package for Kompas Chatbot.

This file marks the `app/` folder as a Python package.
It can also expose top-level variables (like the FastAPI app instance)
if you want to import them elsewhere.
"""

from fastapi import FastAPI
from .app import router

# Optionally, create a FastAPI app here for quick import
app = FastAPI(
    title="Kompas Chatbot API",
    description="Hybrid RAG + SQL chatbot for Indonesia Laws and Regulations.",
    version="1.0.0"
)

# Register routes
app.include_router(router, prefix="/api", tags=["Chatbot"])
