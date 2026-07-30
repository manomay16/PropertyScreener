def calculate_leverage_risk(down_payment, purchase_price):
    if purchase_price == 0:
        return 100
    down_payment_pct = (down_payment / purchase_price) * 100
    leverage_risk = 100 - down_payment_pct
    return max(0, min(100, leverage_risk))


def calculate_cash_flow_risk(monthly_cash_flow, monthly_rental_income):
    if monthly_cash_flow < 0:
        return 100
    if monthly_rental_income == 0:
        return 100
    cash_flow_ratio = (monthly_cash_flow / monthly_rental_income) * 100
    risk = 100 - cash_flow_ratio
    return max(0, min(100, risk))


def calculate_composite_risk_score(disaster_risk_score, break_even_ratio, leverage_risk, cash_flow_risk):
    disaster_risk_score = disaster_risk_score if disaster_risk_score is not None else 50
    break_even_ratio = min(break_even_ratio, 100)

    composite = (
        0.25 * disaster_risk_score
        + 0.35 * break_even_ratio
        + 0.20 * leverage_risk
        + 0.20 * cash_flow_risk
    )
    return round(composite, 2)

