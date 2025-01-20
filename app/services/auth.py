"""
Authentication utility module.

Provides a function to check if a user is authenticated based on the session.
"""

from fastapi import Request

def is_authenticated(request: Request) -> bool:
    """
    Checks if the user is authenticated by verifying the session.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    return bool(request.session.get("user"))
