def calculate_monthly_mortgage_payment(purchase_price, down_payment, loan_interest_rate, loan_term_years):
    loan_amount = purchase_price - down_payment
    monthly_rate = loan_interest_rate / 100 / 12
    num_payments = loan_term_years * 12

    if num_payments == 0:
        return 0

    if monthly_rate == 0:
        return loan_amount / num_payments

    payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / (
        (1 + monthly_rate) ** num_payments - 1
    )
    return payment


def calculate_cap_rate(purchase_price, monthly_rental_income, monthly_expenses):
    if purchase_price == 0:
        return 0
    annual_noi = (monthly_rental_income - monthly_expenses) * 12
    return (annual_noi / purchase_price) * 100


def calculate_monthly_cash_flow(monthly_rental_income, monthly_expenses, monthly_mortgage_payment):
    return monthly_rental_income - monthly_expenses - monthly_mortgage_payment


def calculate_roi(monthly_cash_flow, down_payment):
    if down_payment == 0:
        return 0
    annual_cash_flow = monthly_cash_flow * 12
    return (annual_cash_flow / down_payment) * 100


def calculate_break_even_ratio(monthly_expenses, monthly_mortgage_payment, monthly_rental_income):
    if monthly_rental_income == 0:
        return 0
    return ((monthly_expenses + monthly_mortgage_payment) / monthly_rental_income) * 100


def calculate_all_metrics(property_data):
    mortgage_payment = calculate_monthly_mortgage_payment(
        property_data.purchase_price,
        property_data.down_payment,
        property_data.loan_interest_rate,
        property_data.loan_term_years,
    )
    cash_flow = calculate_monthly_cash_flow(
        property_data.monthly_rental_income,
        property_data.monthly_expenses,
        mortgage_payment,
    )
    return {
        "monthly_mortgage_payment": mortgage_payment,
        "cap_rate": calculate_cap_rate(
            property_data.purchase_price,
            property_data.monthly_rental_income,
            property_data.monthly_expenses,
        ),
        "monthly_cash_flow": cash_flow,
        "roi": calculate_roi(cash_flow, property_data.down_payment),
        "break_even_ratio": calculate_break_even_ratio(
            property_data.monthly_expenses,
            mortgage_payment,
            property_data.monthly_rental_income,
        ),
    }