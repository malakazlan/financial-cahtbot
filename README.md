# Financial Chatbot

A robust financial chatbot that provides real-time stock information, news, and recommendations using Python, FastAPI, MongoDB, and yfinance.

---

## Features
- Real-time stock price updates (AAPL, TSLA, etc.)
- News scraping and recommendations
- RESTful API endpoints
- NLP for financial queries
- MongoDB for data storage

---

## Project Structure
```
financial cahtbot/
├── app/                # Main application code
│   ├── api/            # API endpoints
│   └── corn/           # Scheduled jobs (e.g., stock updater)
├── data/               # Data files
├── database/           # Database connection and models
├── nlp/                # NLP modules
├── recommendation/     # Recommendation engine
├── tests/              # Unit and integration tests
├── venv/               # Python virtual environment
├── app.py              # Main app entry point
├── run.py              # Alternate app runner
├── requirements.txt    # Python dependencies
├── setup.py            # Packaging
├── install_dependencies.py # Dependency installer
├── news_scraper.py     # News scraping script
├── stocks.db           # SQLite DB (if used)
├── financial_chatbot.db# Main DB file
└── README.md           # This file
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/malakazlan/financial-cahtbot.git
cd financial-cahtbot
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root (if needed) and add your configuration, e.g.:
```
MONGO_URI=mongodb://localhost:27017/financial_chatbot
```

### 5. Initialize the Database
- MongoDB should be running locally or remotely.
- The app will auto-create collections as needed.

### 6. Update Stock Data
Run the stock updater script to fetch and store stock prices:
```bash
python app/corn/update_stock.py
```

### 7. Run the Application
```bash
python app.py
# or
python run.py
```

### 8. API Usage
- The API is served via FastAPI (see `app/api/`).
- Visit `http://localhost:8000/docs` for interactive API docs (if using FastAPI).

### 9. Troubleshooting
- If you see duplicate key errors, ensure no unique index exists on the `ticker` field in MongoDB:
  - Open Mongo shell:
    ```
    mongo
    use financial_chatbot
    db.stocks.dropIndex("ticker_1")
    db.stocks.deleteMany({ticker: null})
    ```
- If `current_price` is null, ensure yfinance is returning valid data and fallback logic is in place in `update_stock.py`.

---

## Contribution
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) 