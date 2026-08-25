from calculators import (
    calculate_monthly_mortgage_payment,
    calculate_cap_rate,
    calculate_monthly_cash_flow,
    calculate_roi,
    calculate_break_even_ratio,
)


def test_mortgage_payment_known_value():
    # 400k purchase, 80k down, 6.5% over 30 years — hand-verified earlier in the project
    payment = calculate_monthly_mortgage_payment(400000, 80000, 6.5, 30)
    assert abs(payment - 2022.80) < 0.5


def test_mortgage_payment_zero_interest():
    # 0% interest should just be loan amount / number of payments, no compounding
    payment = calculate_monthly_mortgage_payment(120000, 20000, 0, 10)
    assert abs(payment - (100000 / 120)) < 0.01


def test_cap_rate_known_value():
    # 300k purchase, 2500 rent, 500 expenses — hand-verified earlier
    cap_rate = calculate_cap_rate(300000, 2500, 500)
    assert abs(cap_rate - 8.0) < 0.01


def test_cap_rate_zero_purchase_price():
    # Should not raise a divide-by-zero error
    assert calculate_cap_rate(0, 2500, 500) == 0


def test_cash_flnown_value():
    cash_flow = calculate_monthly_cash_flow(2500, 500, 1516.96)
    assert abs(cash_flow - 483.04) < 0.5


def test_roi_known_value():
    roi = calculate_roi(483.04, 60000)
    assert abs(roi - 9.66) < 0.1


def test_roi_zero_down_payment():
    assert calculate_roi(500, 0) == 0


def test_break_even_ratio_known_value():
    ratio = calculate_break_even_ratio(500, 1516.96, 2500)
    assert abs(ratio - 80.68) < 0.1


def test_break_even_ratio_zero_income():
    assert calculate_break_even_ratio(500, 1000, 0) == 0
