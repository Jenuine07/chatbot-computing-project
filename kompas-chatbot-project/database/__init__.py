# database/__init__.py

"""
Database package for chatbot project.
Handles data access from Excel now, SQL in the future.
"""

from . import excel_loader
from .excel_loader import load_dataset

__all__ = ["excel_loader"]