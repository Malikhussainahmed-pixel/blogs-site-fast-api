from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
Database_Url = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_hostport}/{settings.database_name}"

engine = create_engine(Database_Url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
#                                 password="1234", cursor_factory=RealDictCursor)
#         Cursor = conn.cursor()
#         print("connection to database successful")
#         break
#     except Exception as error:
#         print("failed to connect to data base")
#         print(f"error: {error}")
#         time.sleep(2)
