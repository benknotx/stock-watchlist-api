from sqlalchemy import text
from sqlalchemy.orm import Session
from models import Stock, User, Holdings
import os
import finnhub
from dotenv import load_dotenv
load_dotenv()

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def get_stock_price(ticker: str) -> float:
    tick = normalize_ticker(ticker)
    try:
        quote = finnhub_client.quote(tick)
        return quote.get("c")
    except Exception as e:
        # would log the error here in a real application
        print(f"Error fetching stock price for {tick}: {e}")
        return None


def total_portfolio_value(user: User, db: Session)-> float:
    holdings = get_user_holdings(user, db)

    total_value = 0.0
    for holding, stock in holdings:
        stock_price = get_stock_price(stock.ticker)
        if stock_price is not None:
            total_value += holding.held * stock_price
    return round(total_value, 2)

def get_user_holdings(user: User, db: Session):
    holdings = (
        db.query(Holdings, Stock)
        .join(Stock, Holdings.stock_id == Stock.id)
        .filter(Holdings.user_id == user.id)
        .all()
        )
    return holdings

def update_holdings_amount(holdings: Holdings, amount: float, db: Session):
    holdings.held = amount
    db.commit()
    db.refresh(holdings)

def full_portfolio_response(user: User, db: Session):
    holdings = get_user_holdings(user, db)
    portfolio = []
    total_value = round(total_portfolio_value(user, db), 2)

    for holding, stock in holdings:
        stock_value = get_stock_price(stock.ticker)
        if stock_value is not None:
            portfolio.append({
                "ticker": stock.ticker,
                "held": holding.held,
                "price": stock_value,
                "total_value": round((holding.held * stock_value), 2),
                "percentage_of_portfolio": round(((holding.held * stock_value)/ total_value) * 100 if total_value > 0 else 0,2)
            })

    return {
        "portfolio": portfolio,
        "total_portfolio_value": total_value
    }

def test_db_connection(db):
    try:
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
    
def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper()

def validate_ticker(ticker: str) -> bool:
    tick = normalize_ticker(ticker)
    attempt = finnhub_client.quote(tick)
    attempt_value = attempt.get("c")
    try:
        if attempt_value != 0:
            return True
    except Exception as e:
        print(f"Error validating ticker {tick}: {e}")
        return False
