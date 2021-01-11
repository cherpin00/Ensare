from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def getSession():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    return DBSession()


class User(Base):
    __tablename__ = 'tblUsers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self) -> str:
        return f"<User(name={self.name})>"

class Notify(Base):
    __tablename__ = 'tblNotify'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self) -> str:
        return f"<User(name={self.name})>"