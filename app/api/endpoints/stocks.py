from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.db.models import Stock, Portfolio, User
from app.db.schemas import StockCreate, Stock as StockSchemas
from app.api.endpoints.portfolio import get_current_user

router = APIRouter()


@router.post("/", response_model=StockSchemas)
async def add_stock(
        stock: StockCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).first()
    if not portfolio:
        raise HTTPException(status_code=401, detail="Portfolio not found")

    db_stock = models.Stock(
        portfolio_id=portfolio.id,
        ticker=stock.ticker.upper(),
        quantity=stock.quantity,
        purchase_price=stock.purchase_price
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)

    return db_stock


@router.delete("/{stock_id}", response_model=StockSchemas)
async def remove_stock(
        stock_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    portfolio = db.query(Portfolio).filter(Portfolio.id == stock.portfolio_id).first()

    if portfolio.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(stock)
    db.commit()
    return stock
