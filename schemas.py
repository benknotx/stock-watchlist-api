from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class AdjustStock(BaseModel):
    ticker: str
    held: float

    class Config:
        from_attributes = True

class StockValueResponse(BaseModel):
    ticker: str
    held: float
    price: float
    total_value: float
    percentage_of_portfolio: float


    class Config:
        from_attributes = True
 
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class PortfolioResponse(BaseModel):
    portfolio: list[StockValueResponse]
    total_portfolio_value: float

    class Config:
        from_attributes = True