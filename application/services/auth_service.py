from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from random import randint
import uuid
from fastapi import status
import jwt
from application.configuration.app import AppConfig
from application.configuration.auth_config import AuthConfig
from application.services.encrypt_decrypt import Encryption

from application.utilities.serialization import serialize
from application.utilities.res import APIError, APIResponse
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class AuthService():
    def __init__(self):
        pass
    
    def generate_access_token(self, user_type, user):
        user_dict = serialize(user)
        # txt = "43200"
        txt = "30_days"
        required_fields = {
            'user': ['id', 'name', 'phone','is_active' 'email','role'],
            'admin': ['id', 'name', 'phone','is_active' 'email','role'],
        }
        if user_type == 'admin':
            txt =int(AuthConfig.ADMIN_TOKEN_EXPIRATION_TIME)
        elif user_type =="user":
           txt =int(AuthConfig.USER_TOKEN_EXPIRATION_TIME)
        else:
            txt = 30
        exp= datetime.utcnow()+timedelta(days=txt)

        payload = {
            "user": {field: user_dict[field] for field in required_fields[user_type]},
            "env": AuthConfig.ENVIRONMENT,  # Add environment field (dev, staging, prod)
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4()),
            "exp": exp
        }
        return jwt.encode(payload, AuthConfig.JWT_SECRET_USER[user_type], algorithm="HS256")

        
        # class Hash():
    def verify(self,plain_password,hashes_password):
        return pwd_context.verify(plain_password,hashes_password)



