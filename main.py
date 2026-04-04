from datetime import timedelta
from database import Base, engine 
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import database
import models
import auth
import services
import schemas

app = FastAPI(title="Stocks API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Watchlist API!"}

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    print(type(user.password), user.password)
    if existing_user:
        return {"error": "Username already exists"}
    
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserResponse)
def read_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/portfolio/stocks", response_model=schemas.AdjustStock)
def adjust_stocks_in_portfolio(stock: schemas.AdjustStock, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    normalized_ticker = stock.ticker.strip().upper()
    existing_stock = db.query(models.Stock).filter(models.Stock.ticker == normalized_ticker).first()
    if not existing_stock:
        existing_stock = models.Stock(ticker=normalized_ticker)
        db.add(existing_stock)
        db.commit()
        db.refresh(existing_stock)

    holding = db.query(models.Holdings).filter(models.Holdings.user_id == current_user.id, models.Holdings.stock_id == existing_stock.id).first()
    if holding:
        holding.held = stock.held
        if stock.held == 0:
            db.delete(holding)
            db.commit()
            db.refresh()
            return {"ticker": normalized_ticker, "held" : stock.held}
    else:
        holding = models.Holdings(user_id=current_user.id, stock_id=existing_stock.id, held=stock.held)
        db.add(holding)
    db.commit()
    db.refresh(holding)

    return {"ticker": existing_stock.ticker, "held": holding.held}

@app.get("/portfolio", response_model=schemas.PortfolioResponse)
def get_portfolio(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    portfolio = services.full_portfolio_response(current_user, db)
    return portfolio

@app.get("/portfolio/value")
def get_portfolio_value(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    total_value = services.total_portfolio_value(current_user, db)
    return {"total_portfolio_value": total_value}

@app.get("/stock/{ticker}/value")
def get_stock_value(ticker: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    stock_value = services.get_stock_price(ticker)
    if stock_value is None:
        raise HTTPException(status_code=404, detail="Stock value not found")
    
    return {"ticker": ticker, "value": stock_value}

@app.delete("/portfolio/stocks/{ticker}")
def delete_stock_from_portfolio(ticker: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    normalized_ticker = ticker.strip().upper()
    stock = db.query(models.Stock).filter(models.Stock.ticker == normalized_ticker).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    holding = db.query(models.Holdings).filter(models.Holdings.user_id == current_user.id, models.Holdings.stock_id == stock.id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Stock not in portfolio")
    
    db.delete(holding)
    db.commit()
    db.refresh()
    
    return {"message": f"Removed {normalized_ticker} from portfolio"}

@app.get("/portfolio_view_holdings")
def get_portfolio_holdings(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return [{**holding.__dict__, "ticker": stock.ticker} for holding, stock in services.get_user_holdings(current_user, db)]

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    if services.test_db_connection(db):
        return {"status": "healthy", "database": "connected"}
    return {"status": "healthy", "database": "error"}
