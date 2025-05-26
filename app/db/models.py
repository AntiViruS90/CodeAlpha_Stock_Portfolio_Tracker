from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    portfolio = relationship("Portfolio", back_populates="user", uselist=False)


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, default="My Portfolio")

    user = relationship("User", back_populates="portfolio")
    stocks = relationship("Stock", back_populates="portfolio")


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String, index=True)
    quantity = Column(Float)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="stocks")

