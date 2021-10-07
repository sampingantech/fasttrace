from typing import Optional
from sqlalchemy import Column, BigInteger, Text, Integer


from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field, SQLModel

Base = declarative_base()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


class HeroAsync(Base):
    __tablename__ = "hero"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    secret_name = Column(Text)
    age = Column(Integer)
