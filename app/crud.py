# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from decimal import Decimal

def get_all_data(db: Session, instrument: str = "HINDALCO"):
    return db.query(models.TickerData).filter(models.TickerData.instrument == instrument).order_by(models.TickerData.datetime).all()

def create_data(db: Session, data: schemas.TickerDataIn):
    db_obj = models.TickerData(
        datetime=data.datetime,
        open=Decimal(str(data.open)),
        high=Decimal(str(data.high)),
        low=Decimal(str(data.low)),
        close=Decimal(str(data.close)),
        volume=int(data.volume),
        instrument=data.instrument
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj