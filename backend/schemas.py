from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PropertyCreate(BaseModel):
    address: str
    purchase_price: float
    down_payment: float
    loan_interest_rate: float
    loan_term_years: int
    monthly_rental_income: float
    monthly_expenses: float


class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    purchase_price: Optional[float] = None
    down_payment: Optional[float] = None
    loan_interest_rate: Optional[float] = None
    loan_term_years: Optional[int] = None
    monthly_rental_income: Optional[float] = None
    monthly_expenses: Optional[float] = None


class PropertyOut(BaseModel):
    id: int
    session_id: str
    address: str
    purchase_price: float
    down_payment: float
    loan_interest_rate: float
    loan_term_years: int
    monthly_rental_income: float
    monthly_expenses: float
    created_at: datetime

    class Config:
        from_attributes = True

class PropertyMetrics(BaseModel):
    monthly_mortgage_payment: float
    cap_rate: float
    monthly_cash_flow: float
    roi: float
    break_even_ratio: float


class PropertyWithMetrics(PropertyOut):
    metrics: PropertyMetrics


class ScoreOut(BaseModel):
    id: int
    property_id: int
    disaster_risk_score: Optional[float] = None
    ml_risk_score: Optional[float] = None
    explanation: Optional[str] = None
    computed_at: datetime

    class Config:
        from_attributes = True