from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from dotenv import load_dotenv
from app.settings import get_settings
from functools import lru_cache
import os

load_dotenv()

engine = create_engine(get_settings().database_url, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session

def get_session() -> Generator[scoped_session, None, None]:
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()
