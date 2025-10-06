import os
class AppConfig:
    ENVIRONMENT:str = os.environ.get("ENV")
    PROJECT_TITLE:str = "Vidysea Notes Service "+str(os.environ.get("ENV"))
    PROJECT_VERSION: str = "0.0.1"
    DESCRIPTION : str = "Vidysea Notes Service"
    CURRENT_APP_VERSION : str = os.environ.get("CURRENT_APP_VERSION")


app_config = AppConfig()