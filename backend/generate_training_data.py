import random
import numpy as np
import pandas as pd
from sqlalchemy import text
from database import engine
from calculators import (
    calculate_monthly_mortgage_payment,
    calculate_cap_rate,
    calculate_monthly_cash_flow,
    calculate_roi,
    calculate_break_even_ratio,
)
from risk_scoring import (
    calculate_leverage_risk,
    calculate_cash_flow_risk,
    calculate_composite_risk_score,
)

NUM_SAMPLES = 20000

with engine.connect() as conn:
    result = conn.execute(text("SELECT census_tract, risk_score FROM fema_risk"))
    tracts = result.fetchall()

print(f"Loaded {len(tracts)} real census tracts from fema_risk.")

rows = []
for _ in range(NUM_SAMPLES):
    census_tract, disaster_risk_score = random.choice(tracts)

    purchase_price = float(np.exp(np.random.uniform(np.log(100000), np.log(800000))))
    down_payment_pct = np.random.uniform(0.05, 0.50)
    down_payment = purchase_price * down_payment_pct
    loan_interest_rate = np.random.uniform(4.0, 8.0)
    loan_term_years = random.choices([15, 30], weights = [0.2,0.8])[0]

    rent_to_price_ratio = np.random.uniform(0.006, 0.015)
    monthly_rental_income = purchase_price * rent_to_price_ratio * np.random.uniform(0.9, 1.1)

    expense_ratio = np.random.uniform(0.20, 0.50)
    monthly_expenses = monthly_rental_income * expense_ratio

    mortgage_payment = calculate_monthly_mortgage_payment(
        purchase_price, down_payment, loan_interest_rate, loan_term_years
    )
    cap_rate = calculate_cap_rate(purchase_price, monthly_rental_income, monthly_expenses)
    cash_flow = calculate_monthly_cash_flow(monthly_rental_income, monthly_expenses, mortgage_payment)
    roi = calculate_roi(cash_flow, down_payment)
    break_even_ratio = calculate_break_even_ratio(monthly_expenses, mortgage_payment, monthly_rental_income)

    leverage_risk = calculate_leverage_risk(down_payment, purchase_price)
    cash_flow_risk = calculate_cash_flow_risk(cash_flow, monthly_rental_income)
    risk_label = calculate_composite_risk_score(
        disaster_risk_score, break_even_ratio, leverage_risk, cash_flow_risk
    )

    rows.append({
        "census_tract": census_tract,
        "purchase_price": purchase_price,
        "down_payment": down_payment,
        "loan_interest_rate": loan_interest_rate,
        "loan_term_years": loan_term_years,
        "monthly_rental_income": monthly_rental_income,
        "monthly_expenses": monthly_expenses,
        "disaster_risk_score": disaster_risk_score,
        "monthly_mortgage_payment": mortgage_payment,
        "cap_rate": cap_rate,
        "monthly_cash_flow": cash_flow,
        "roi": roi,
        "break_even_ratio": break_even_ratio,
        "leverage_risk": leverage_risk,
        "cash_flow_risk": cash_flow_risk,
        "risk_label": risk_label,
    })

df = pd.DataFrame(rows)
df.to_csv("data/synthetic_training_data.csv", index=False)
print(f"Generated {len(df)} synthetic training rows -> data/synthetic_training_data.csv")
