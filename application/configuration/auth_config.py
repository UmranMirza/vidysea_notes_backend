import os


class AuthConfig:
    ENVIRONMENT = os.environ.get("ENV")
    JWT_SECRET =  os.environ.get("JWT_SECRET_KEY")
    ENCRYPTION_KEY = JWT_SECRET
    ADMIN_TOKEN_EXPIRATION_TIME = os.environ.get("ADMIN_TOKEN_EXPIRATION_TIME", "30")
    USER_TOKEN_EXPIRATION_TIME = os.environ.get("USER_TOKEN_EXPIRATION_TIME", "30")
    ACEREADYUSER_TOKEN_EXPIRATION_TIME = os.environ.get("USER_TOKEN_ACEREADY_EXPIRATION_TIME", "30")
    JWT_SECRET_USER = {
            'user': JWT_SECRET+"_user",
            'admin': JWT_SECRET+"_admin"
        }

    USER_LOGIN_SECRET = JWT_SECRET+"_user"
    ADMIN_LOGIN_SECRET = JWT_SECRET+"_admin"
    
    
    

