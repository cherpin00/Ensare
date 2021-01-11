from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from sqlalchemy.pool.impl import NullPool
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = 'tblUsers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return f"<User(name={self.name})>"

class Notify(Base):
    __tablename__ = 'tblNotify'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    file = Column(String)
    batchTime = Column(DateTime)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, file={self.file}, batchTime={self.batchTime})>"