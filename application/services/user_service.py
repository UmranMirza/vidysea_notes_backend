from passlib.context import CryptContext

from application.models.users import User



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class UserService():
    def __init__(self):
        pass
    
    def get_user_by_email(self,db,email):
        user = User.get_by_email(db=db, email=email)
        return user
    
    def get_user_by_id(self,db,id):
        user = User.get_by_id(db=db, id=id)
        return user
    
    
    
    def register_user(self, db, name, email, password, role):
        hashed_password = pwd_context.hash(password)
        user = User(name=name, email=email,role=role, password=hashed_password)
        user.save(db=db)
        return user
    
    
    