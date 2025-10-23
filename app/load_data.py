# app/load_data.py
# import requests
import csv
from io import StringIO
from datetime import datetime
from decimal import Decimal
from urllib import request
from .db import SessionLocal, engine, Base
from .models import TickerData
import os

# Export URL for first sheet as CSV
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL", "https://docs.google.com/spreadsheets/d/1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8/edit?rtpof=true")






def fetch_csv(url=SHEET_CSV_URL):
    r = request.get(url)
    r.raise_for_status()
    return r.text



def parse_and_insert(csv_text):
    f = StringIO(csv_text)
    reader = csv.reader(f)
    # Skip header row(s) — sheet structure has header in row 1: datetime close high low open volume then instrument rows below
    rows = list(reader)
    # Find first row with a date (first entry that parses as datetime)
    data_rows = []
    for row in rows:
        if not row:
            continue
        # Expected pattern: datetime, close, high, low, open, volume, maybe instrument as next row
        try:
            # Try parse first column
            dt = datetime.fromisoformat(row[0])
            # Get other columns with indexes if present
            # Some sheets may have different order; we're mapping columns by detected header positions:
            # But sheet is: datetime, close, high, low, open, volume  (per inspecting sheet)
            close = Decimal(row[1])
            high = Decimal(row[2])
            low = Decimal(row[3])
            openp = Decimal(row[4])
            volume = int(row[5])
            data_rows.append((dt, openp, high, low, close, volume))
        except Exception:
            continue

    db = SessionLocal()
    try:
        for dt, openp, high, low, close, volume in data_rows:
            # Prevent duplicates by unique constraint (we didn't add one programmatically here - ensure unique in DB)
            existing = db.query(TickerData).filter(TickerData.datetime == dt).first()
            if existing:
                continue
            obj = TickerData(
                datetime=dt,
                open=openp,
                high=high,
                low=low,
                close=close,
                volume=volume,
                instrument="HINDALCO"
            )
            db.add(obj)
        db.commit()
    finally:
        db.close()


def load_csv(file_path):
    """Load a CSV file from the given path and return a list of dicts."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


if __name__ == "__main__":
    csv_text = fetch_csv()
    parse_and_insert(csv_text)
    print("Import finished.")



