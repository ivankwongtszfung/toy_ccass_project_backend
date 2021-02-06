from datetime import date
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.ccass.services.shareholding_query import (
    ShareHoldingService,
    TransactionService,
)


router = APIRouter()


@router.get("/ccass/top_ten_shareholding")
def update_item(stock_code: str, start_date: date, end_date: date):
    return ShareHoldingService(stock_code, start_date, end_date).execute()


@router.get("/ccass/shareholding_threshold")
def update_item(stock_code: str, start_date: date, end_date: date, threshold: float):
    return TransactionService(stock_code, start_date, end_date, threshold).execute()