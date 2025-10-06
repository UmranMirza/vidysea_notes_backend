import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

print("Application_environment =" + str(os.environ.get("ENV")))
DB_URI= os.environ.get("DB_URI")
ASYNC_DB_URI = os.environ.get("ASYNC_DB_URI")

print(f"Database URI: {DB_URI}")


engine = create_engine(DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)

Base = declarative_base()

def init_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)
    return SessionLocal()


def get_session():
    with SessionLocal() as session:
        try:
            yield session
            print(session)
        except Exception as e:
            print("error")
            # print(e.__traceback__)
            pass


activeSession = Depends(get_session)
