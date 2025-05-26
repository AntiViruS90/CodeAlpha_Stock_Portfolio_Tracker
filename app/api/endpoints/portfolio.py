from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Dict, Any, List
import httpx


from app.db.database import get_db
from app.db.models import User, Portfolio as PortfolioModels
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
templates = Jinja2Templates(directory="app/templates")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/", response_model=Dict[str, Any])
async def get_portfolio(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Dict[str, Any]:
    portfolio = db.query(PortfolioModels).filter(PortfolioModels.user_id == user.id).first()
    if not portfolio:
        portfolio = PortfolioModels(user_id=user.id, name="My Portfolio")
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

    stocks = portfolio.stocks
    stock_data: List[Dict[str, Any]] = []

    async with httpx.AsyncClient() as client:
        for stock in stocks:
            response = await client.get(
                f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock.ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
            )
            data = response.json().get("Global Quote", {})
            current_price = float(data.get("05. price", stock.purchase_price))
            stock_data.append({
                "stock_id": stock.id,
                "ticker": stock.ticker,
                "quantity": stock.quantity,
                "purchase_price": stock.purchase_price,
                "current_price": current_price,
                "total_value": round(current_price * stock.quantity, 2),
                "profit_loss": round((current_price - stock.purchase_price) * stock.quantity, 2)
            })
    return {
        "portfolio": {
            "id": portfolio.id,
            "name": portfolio.name,
            "user_id": portfolio.user_id,
        },
        "stocks": stock_data,
        "total_value": sum(stock['total_value'] for stock in stock_data),
        "currency": "USD",
    }
