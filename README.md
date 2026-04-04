# Stock Watchlist API
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![License](https://img.shields.io/badge/License-MIT-blue)

A RESTful API for managing personal stock portfolios with secure authentication and real-time market data integration.

The system allows users to track holdings, calculate portfolio value dynamically, and retrieve live stock prices via the Finnhub API.

## Quick Example

Authenticate and retrieve portfolio value:

### Login
```bash
POST /login
```

```json
{
  "username": "testuser",
  "password": "password123"
}
```

### Response
```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

### Use Token
```bash
GET /portfolio/value
Authorization: Bearer <token>
```

```json
{
  "total_value": 12500.50
}
```

### Get Stock Price
```bash
GET /stock/AAPL/value
Authorization: Bearer <token>
```

```json
{
  "ticker": "AAPL",
  "price": 182.34  
}
```
## 🔄 Typical Workflow

1. Register a new user
2. Login to receive a JWT token
3. Add stocks to your portfolio
4. Retrieve portfolio data with real-time valuations
5. Query individual stock prices as needed

## 🧠 System Design

This API follows a layered architecture:

- **API Layer (FastAPI routes)** – handles HTTP requests
- **Service Layer** – business logic (portfolio calculations, stock handling)
- **Database Layer (SQLAlchemy ORM)** – persistence layer
- **External API Integration** – Finnhub for real-time stock data

Authentication is handled using JWT tokens with hashed passwords stored using bcrypt.

## 📊 Architecture Diagram
```
Client
  ↓
FastAPI Routes
  ↓
Service Layer → Finnhub API
  ↓
Database (SQLite)
```

## 🚀 Features

- **User Authentication**: Secure JWT-based login and registration system
- **Portfolio Management**: Add, update, and remove stocks from user portfolios
- **Real-time Stock Data**: Fetch live prices using the Finnhub API
- **Portfolio Valuation**: Calculate total portfolio value and individual stock contributions
- **Health Checks**: Database connectivity monitoring
- **Auto-generated API Documentation**: Interactive docs via FastAPI's built-in Swagger UI

## 🛠 Tech Stack

- **Framework**: FastAPI (Python web framework for building APIs)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **External API**: Finnhub for stock market data
- **Environment Management**: python-dotenv
- **ASGI Server**: Uvicorn

## 📋 Prerequisites

- Python 3.8+
- Finnhub API key (free tier available at [finnhub.io](https://finnhub.io))

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/benknotx/stock-watchlist-api.git
   cd stock-watchlist-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   FINNHUB_API_KEY=your-finnhub-api-key
   ```

## ▶️ Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📖 Interactive API Docs

Once running, visit `http://127.0.0.1:8000/docs` for interactive API documentation powered by Swagger UI.

## 🔐 Authentication

All protected endpoints require a Bearer token obtained from the `/login` endpoint.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | User registration |
| POST | `/login` | User login (returns JWT token) |
| GET | `/me` | Get current user info |
| POST | `/portfolio/stocks` | Add/update stocks in portfolio |
| GET | `/portfolio` | Get full portfolio with valuations |
| GET | `/portfolio/value` | Get total portfolio value |
| GET | `/stock/{ticker}/value` | Get individual stock price |
| DELETE | `/portfolio/stocks/{ticker}` | Remove stock from portfolio |
| GET | `/health` | Health check |

## 🗄 Database Schema

The application uses SQLite with the following main models:
- **User**: Stores user credentials and info
- **Stock**: Represents individual stocks by ticker
- **Holdings**: Links users to stocks with quantity held

## ⚙️ Key Design Decisions

- Portfolio values are calculated in real-time instead of stored in the database to avoid stale data
- Stock tickers are normalized and validated before database insertion
- Stateless authentication is used via JWT instead of server-side sessions
- External API calls are made on-demand (no caching layer in current version)

## 🧪 Testing

The API was validated using:

- FastAPI Swagger UI (`/docs`) for endpoint testing
- Manual integration testing via curl requests
- Authentication flow testing (register → login → token validation)
- Edge case testing (invalid tickers, zero holdings, unauthorized access)

Future improvements:
- Automated unit and integration testing with Pytest
- Continuous integration (CI) pipeline for test automation


## 🚧 Future Improvements

- Add caching layer for external API responses
- Implement automated testing with Pytest
- Add portfolio performance tracking over time
- Introduce refresh token authentication flow
- Add pagination for large portfolios

## 📌 What This Project Demonstrates

- RESTful API design with FastAPI
- JWT-based authentication and authorization
- Integration with external financial APIs (Finnhub)
- Database modeling with SQLAlchemy ORM
- Service-layer architecture separation
- Real-time data aggregation and computation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Benjamin Williams** 
Email: Benknotx@gmail.com
Github: https://github.com/Benknotx

Project Link: [https://github.com/Benknotx/stock-watchlist-api](https://github.com/Benknotx/stock-watchlist-api)

---

Built as a backend portfolio project to demonstrate authentication, external API integration, and RESTful API design using FastAPI.
