from fastapi import APIRouter,status
from fastapi import Request
from application.utilities.res import APIError, APIResponse
from sqlalchemy.orm import Session
from application import activeSession
from application.utilities.serialization import serialize


test_router = APIRouter()


@test_router.get("/test")
def test(request:Request, db:Session=activeSession):
    return APIResponse(data="TEST  SERVICE",message="TESTING SERVICE",status=status.HTTP_200_OK).to_json()
