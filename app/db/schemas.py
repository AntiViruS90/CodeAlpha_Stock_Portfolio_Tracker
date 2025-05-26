from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PortfolioBase(BaseModel):
    name: Optional[str] = "My Portfolio"


class Portfolio(PortfolioBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class StockBase(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: float
    purchase_price: float
    purchase_date: Optional[datetime] = Field(default_factory=datetime.utcnow)


class StockCreate(StockBase):
    ...


class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True
