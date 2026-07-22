from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    address = Column(String, nullable=False)
    census_tract = Column(String)
    purchase_price = Column(Float)
    down_payment = Column(Float)
    loan_interest_rate = Column(Float)
    loan_term_years = Column(Integer)
    monthly_rental_income = Column(Float)
    monthly_expenses = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cost_history = relationship("CostHistory", back_populates="property")
    scores = relationship("Score", back_populates="property")


class CostHistory(Base):
    __tablename__ = "cost_history"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime(timezone=True))

    property = relationship("Property", back_populates="cost_history")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    disaster_risk_score = Column(Float)
    ml_risk_score = Column(Float)
    explanation = Column(Text)
    shap_values = Column(JSON)
    computed_at = Column(DateTime(timezone=True), server_default=func.now())

    property = relationship("Property", back_populates="scores")
