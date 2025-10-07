from datetime import datetime, timedelta
import uuid
import jwt
from passlib.context import CryptContext
from application.configuration.auth_config import AuthConfig
from application.utilities.serialization import serialize

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService():
    def __init__(self):
        pass

    def generate_access_token(self, user_type, user):
        user_dict = serialize(user)
        required_fields = {
            'user': ['id', 'name', 'phone','is_active', 'email','role'],
            'admin': ['id', 'name', 'phone','is_active', 'email','role'],
        }
        if user_type == 'admin':
            txt = int(AuthConfig.ADMIN_TOKEN_EXPIRATION_TIME)
        elif user_type == "user":
            txt = int(AuthConfig.USER_TOKEN_EXPIRATION_TIME)
        else:
            txt = 30
        exp = datetime.utcnow() + timedelta(days=txt)

        payload = {
            "user": {field: user_dict[field] for field in required_fields[user_type]},
            "env": AuthConfig.ENVIRONMENT,  # dev, staging, prod
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4()),
            "exp": exp
        }
        return jwt.encode(payload, AuthConfig.JWT_SECRET_USER[user_type], algorithm="HS256")

    def decode_access_token(self, token: str, user_type: str):
        """
        Decode and validate a JWT access token.
        Raises jwt.ExpiredSignatureError if token expired.
        Raises jwt.InvalidTokenError if token is invalid.
        """
        try:
            decoded = jwt.decode(
                token,
                AuthConfig.JWT_SECRET_USER[user_type],
                algorithms=["HS256"]
            )
            return decoded
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def verify(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
