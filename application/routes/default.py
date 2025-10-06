from fastapi import APIRouter
from fastapi import Request
from application.configuration.app import AppConfig
from application.utilities.res import APIResponse
from application.utilities.serialization import serialize
router = APIRouter(tags=["Default"])
from sqlalchemy.orm import Session
from application import activeSession

@router.get("/", summary="Health Check", response_description="Health Check Response")
async def health_check(request: Request, db: Session = activeSession):
    """
    Health Check Endpoint
    """
    config = AppConfig()
    data = {
        "service": "Notes Service",
        "status": "OK",
        "version": config.APP_VERSION,
        "environment": config.ENVIRONMENT,
    }
    return APIResponse(data=serialize(data), message="Service is healthy").to_json()
