# ⚡ Trading Strategy Analysis – FastAPI Project

This project is a **FastAPI-based trading analysis platform** designed to analyze stock or crypto data, apply technical strategies such as **Moving Average Crossover**, and evaluate performance metrics.

It supports database storage via **SQLAlchemy ORM**, real-time strategy evaluation, and automated test coverage using **pytest**.

---

## 🚀 Features

✅ Load and parse financial time-series CSV data  
✅ Apply Moving Average Crossover strategy  
✅ Compute performance metrics (returns, signals, etc.)  
✅ Store results in PostgreSQL / SQLite  
✅ RESTful API endpoints built with FastAPI  
✅ Fully tested with `pytest` and `pytest-cov`  

---

## 🧩 Project Structure

## ⚙️ Setup Instructions



```bash
git clone https://github.com/rishee10/-Invsto.git
cd -Invsto

## Create and Activate Virtual Environment
python -m venv venv

## Activate it:
venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

```

## 🗄️ Database Setup

You can run this project using either PostgreSQL or SQLite.

🔹 Option 1: PostgreSQL 

Install PostgreSQL and start the service.

Create a new database:

createdb trading_db


Update the environment variable:

# Windows
set DATABASE_URL=postgresql://postgres:password@localhost/trading_db


Initialize tables:

```bash
>>> from app.db import Base, engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

🔹 Option 2: SQLite (for local development/testing)

No setup needed.
By default, if no DATABASE_URL is found, the app will use:

sqlite:///./trading.db

▶️ Running the FastAPI App

uvicorn app.main:app --reload

🧪 Running Tests
```bash
Run all tests
pytest app/test_main.py -v

Run tests with coverage report
pytest --cov=app --cov-report=term-missing app/test_main.py -v

or
pytest --cov=app --cov-report=term-missing -v

```

