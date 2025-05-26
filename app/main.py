from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.endpoints import auth, portfolio, stocks
from app.db.database import engine
from app.db.models import Base

app = FastAPI(title="Stock Portfolio Tracker")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])


@app.get("/")
async def root():
    return {"message": "Welcome to Stock Portfolio Tracker"}
