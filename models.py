from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) 

    
    stocks = relationship("Stock", secondary="holdings", back_populates="users")

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)  

    users = relationship("User", secondary="holdings", back_populates="stocks")

class Holdings(Base):
    __tablename__ = 'holdings'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), primary_key=True)
    held = Column(Float, default=0.0)