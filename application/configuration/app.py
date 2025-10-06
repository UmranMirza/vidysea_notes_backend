import os
class AppConfig:
    ENVIRONMENT:str = os.environ.get("ENV")
    PROJECT_TITLE:str = "ACEPlus Coupon Service "+str(os.environ.get("ENV"))
    PROJECT_VERSION: str = "0.0.1"
    DESCRIPTION : str = "ACEPlus Coupon Service"
    # REDIS_URL : str = os.environ.get("REDIS_URL")
    # Dev
    SUBSCRIPTION_SERVICE_BASE_URL : str = os.environ.get("SUBSCRIPTION_SERVICE_BASE_URL")
    USER_SERVICE_BASE_URL : str = os.environ.get("USER_SERVICE_BASE_URL")
    ACTIVITY_SERVICE_BASE_URL : str = os.environ.get("ACTIVITY_SERVICE_BASE_URL")
    COUPON_SERVICE_BASE_URL : str = os.environ.get("COUPON_SERVICE_BASE_URL")

    REMOTE_URL_ACTIVITY_SERVICE : str = os.environ.get("REMOTE_URL_ACTIVITY_SERVICE")

    # Staging
    # USER_SERVICE_BASE_URL : str = "http://18.213.241.181:5000"
    POINTS_TO_BUY_TIME = 100
    CURRENT_APP_VERSION : str = os.environ.get("CURRENT_APP_VERSION")
    SENTRY_DSN:str=os.environ.get("COUPON_SENTRY_DSN")


app_config = AppConfig()