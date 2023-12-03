import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_USERNAME=os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_NAME=os.getenv('DATABASE_NAME')

connection_string = f'mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
engine = create_engine(connection_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
