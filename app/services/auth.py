from fastapi import Request

def is_authenticated(request: Request):
    return request.session.get("user")
