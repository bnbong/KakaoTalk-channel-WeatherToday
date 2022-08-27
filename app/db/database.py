from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = 'postgresql://' + \
    os.getenv('PG_USER') + ':' + os.getenv('PG_PASSWORD') +\
        '@' + os.getenv('PG_HOSTNAME') + ':' + os.getenv('PG_PORT') + '/' + os.getenv('PG_DBNAME')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
