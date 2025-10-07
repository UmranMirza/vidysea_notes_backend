from functools import wraps
from fastapi import Request
from fastapi.responses import JSONResponse
from application.services.auth_service import AuthService
from application.utilities.res import APIError

auth_service = AuthService()


def user_login_required(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or args[0]
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                content=APIError(message="Authorization token missing", data={}, status=401).to_dict()
            )
        token = auth_header.split(" ")[1]

        payload = auth_service.decode_access_token(token, user_type="user")
        if not payload:
            return JSONResponse(
                content=APIError(message="Invalid or expired token", data={}, status=401).to_dict()
            )

        request.state.user_id = payload["user"]["id"]
        request.state.role = payload["user"]["role"]
        request.state.user = payload["user"]

        return await func(*args, **kwargs) if callable(getattr(func, "__await__", None)) else func(*args, **kwargs)

    return async_wrapper


def admin_login_required(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or args[0]
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                content=APIError(message="Authorization token missing", data={}, status=401).to_dict()
            )
        token = auth_header.split(" ")[1]

        payload = auth_service.decode_access_token(token, user_type="admin")
        if not payload:
            return JSONResponse(
                content=APIError(message="Invalid or expired token", data={}, status=401).to_dict()
            )

        if payload["user"]["role"] != "admin":
            return JSONResponse(
                content=APIError(message="Admin access required", data={}, status=403).to_dict()
            )

        request.state.user_id = payload["user"]["id"]
        request.state.role = payload["user"]["role"]
        request.state.user = payload["user"]

        return await func(*args, **kwargs) if callable(getattr(func, "__await__", None)) else func(*args, **kwargs)

    return async_wrapper
