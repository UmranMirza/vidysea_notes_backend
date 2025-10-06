import logging
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from application.configuration.app import AppConfig, app_config
from fastapi import FastAPI,Request,Depends,status
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from fastapi_mail import ConnectionConfig, FastMail
from fastapi.templating import Jinja2Templates
from application.utilities.res import APIError

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sentry_sdk

from application.configuration.db import ASYNC_DB_URI, DB_URI,activeSession,Base
site = AdminSite(settings=Settings(database_url_async=ASYNC_DB_URI))
scheduler = SchedulerAdmin.bind(site)
templates = Jinja2Templates(directory="application/templates")


def create_app():
    
    if AppConfig.ENVIRONMENT is not None and AppConfig.ENVIRONMENT in ['production','staging'] and AppConfig.SENTRY_DSN is not None and AppConfig.SENTRY_DSN != "":
        print("Initializinng sentry for "+AppConfig.ENVIRONMENT)
        sentry_sdk.init(
            dsn=AppConfig.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            environment=AppConfig.ENVIRONMENT,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )


    app = FastAPI(
        title=app_config.PROJECT_TITLE,
        version=app_config.PROJECT_VERSION,
        description=app_config.DESCRIPTION,
        contact={"name": ""},
        redoc_url=None,
    )
    
    logger = logging.getLogger("api")
    logger.setLevel(logging.DEBUG)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        print(exc.errors())
        error_messages = []

        for e in exc.errors():
            print(e)
            if e['type'] == 'value_error.missing':
                field = e['loc']
                if field[0] == 'body' and len(field) > 1:
                    error_messages.append(field[1].capitalize()+" value is missing")
            elif e['type'] == 'assertion_error':
                error_messages.append(e['msg'])
            else:
                error_messages.append(e['msg'])
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False, 
                "data": {
                    "errors": exc.errors()
                }, 
                "message": error_messages[0] if len(error_messages) > 0 else "Validation"
            }
        )
   
    print("Application title =" + app.title)
    print("Application version =" + app.version)
    print("Application db =" + DB_URI)
    

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # from application.routes import default
    # app.include_router(default.router)
        
    # routes
    from application.routes.app.test import test_router
    app.include_router(test_router, prefix="/app/test",tags=["Test"])

    return app
