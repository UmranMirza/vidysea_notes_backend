from fastapi import APIRouter
from fastapi import Request, status
from application.models.users import User
from application.models.notes import Note
from application.routes import user_login_required, coupon_manager_login_required
from application.schemas.app.user_schemas import UserRegister
from application.services.auth_service import AuthService
from application.services.user_service import UserService
from application.utilities.res import APIError, APIResponse
from sqlalchemy.orm import Session
from application import activeSession
from application.utilities.serialization import serialize



manage_auth = APIRouter()


@manage_auth.post("/register")
def register_user(request:Request, data: UserRegister, db:Session=activeSession):
    User().get_by_id(db=db,id=1)
    Note().get_by_id(db=db,id=1)
    # Check if email already registered
    user_by_email = UserService().get_user_by_email(db=db,email=data.email)
    if user_by_email is not None:
    # user is with same email already registered
        return APIError(message="Email already exist, please choose another email", data={}, status=status.HTTP_406_NOT_ACCEPTABLE).to_json()

    # All good, lets register the user
    user = UserService().register_user(db=db,role=data.role, name=data.name, email=data.email, password=data.password)
    user_serialized = {
          "id": user.id,
          "name": user.name,
          "email": user.email,
          "role": user.role,
          "phone": user.phone,
          "is_active": user.is_active
        }
    if user is None:
        return APIError(message="Unable to process, please try after sometime", data={}, status=status.HTTP_406_NOT_ACCEPTABLE).to_json()

    # Send access token for the Registered user
    token = AuthService().generate_access_token(user_type='user', user=user_serialized)
    if user:
        return APIResponse(message="user Registered", data=serialize({
            "user": user_serialized,
            "access_token": token

        })).to_json()


# @manage_auth.post("/login")
# def login_user(request: Request, data: userlogin, db: Session = activeSession):
#     # Check if email already registered
#     user = user_service.get_user_by_email(db=db, email=data.email)
#     if user is None:
#         # user is with  email not registered
#         return APIError(
#             message="Email Not registered",
#             data={},
#             status=status.HTTP_406_NOT_ACCEPTABLE,
#         ).to_json()
#     role = user.role
#     if role == "skillcoach":
#         role = "user"

#     if not auth_service.verify(data.password, user.password):
#         return APIError(
#             message="Invalid credentials",
#             data={},
#             status=status.HTTP_406_NOT_ACCEPTABLE,
#         ).to_json()
#     user_serialized = {
#         "id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "role": user.role,
#     }
#     token = auth_service.generate_access_token(user_type=role, user=user_serialized)
#     if user:
#         return APIResponse(
#             message="Login successful",
#             data=serialize({"user": user_serialized, "access_token": token}),
#         ).to_json()

