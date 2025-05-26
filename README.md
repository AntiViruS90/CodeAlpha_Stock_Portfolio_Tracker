# Stock Portfolio Tracker

A RESTful API for tracking a single stock portfolio, allowing users to add, remove, and monitor stock performance in real-time using the Alpha Vantage API. Built with FastAPI, PostgreSQL, and PyJWT for authentication. The interface is provided via Swagger UI.

## Features
- User authentication (register/login) with JWT.
- Manage a single portfolio: add/remove stocks, view real-time performance.
- Real-time stock data via Alpha Vantage API.
- API documentation and interaction via Swagger UI (`/docs`).
- Deployable with Docker.

## Prerequisites
- Docker and Docker Compose
- PostgreSQL 15 (included in Docker Compose)
- Alpha Vantage API key (free tier available at [alphavantage.co](https://www.alphavantage.co))

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AntiViruS90/CodeAlpha_Stock_Portfolio_Tracker.git
cd stock_portfolio_tracker
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory with the following like .env.example

Replace `your_alpha_vantage_api_key` and `your_secret_key` with your values. Generate a secret key

### 3. Run with Docker
Build and start the application:
```bash
1. make build

2. make up
```

Access the API at `http://localhost:8000`. Use Swagger UI at `http://localhost:8000/docs` for interaction.

## Project Structure
```
stock_portfolio_tracker/
├── app/
│   ├── api/endpoints/       # API routes (auth, portfolio, stocks)
│   ├── core/                # Configuration and security utilities
│   ├── db/                  # Database models, schemas, and connection
│   ├── main.py              # Application entry point
├── migrations/              # Alembic migrations (optional)
├── .env                     # Environment variables
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## API Endpoints (via Swagger UI at `/docs`)
- `POST /auth/register`: Register a new user.
- `POST /auth/token`: Log in and get a JWT token.
- `GET /portfolio/`: View portfolio with real-time stock data.
- `POST /stocks/`: Add a stock to the portfolio.
- `DELETE /stocks/{stock_id}`: Remove a stock from the portfolio.

## Notes
- The Alpha Vantage free tier has limits (5 requests/min, 500/day). Consider caching for production.
- Ensure PostgreSQL is accessible via the Docker network (`db:5432`).
- Swagger UI (`/docs`) provides full API interaction and documentation.

## Troubleshooting
- **UnicodeDecodeError**: Ensure `.env` is saved in UTF-8 without BOM.
- **Database connection issues**: Verify PostgreSQL container is running and `DATABASE_URL` is correct.
- **Missing dependencies**: Rebuild the Docker image with `docker-compose up --build`.

P.S. You can view a video tutorial on how to use the app at this [link](https://drive.google.com/file/d/1EwfBDX-O0DkOLQLTTGbGWU4l3-CGZLFs/view?usp=sharing)