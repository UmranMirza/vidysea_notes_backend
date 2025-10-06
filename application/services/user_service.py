from passlib.context import CryptContext

from application.models.users import User



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


MAX_PASSWORD_LENGTH = 72

def hash_password(password: str) -> str:
        password = password[:MAX_PASSWORD_LENGTH]  # truncate if needed
        return pwd_context.hash(password)
class UserService():
    def __init__(self):
        pass
    
    def get_user_by_email(self,db,email):
        user = User.get_by_email(db=db, email=email)
        return user
    
    def get_user_by_id(self,db,id):
        user = User.get_by_id(db=db, id=id)
        return user
    

    
    
    def register_user(self, db, name, email, password, role, phone):
        hashed_password = hash_password(password)
        user = User(name=name, email=email,role=role, hashed_password=hashed_password,phone=phone)
        user.save(db=db)
        return user
    
    
    