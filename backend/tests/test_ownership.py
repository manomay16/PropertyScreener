import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

REAL_ADDRESS = "1600 Pennsylvania Avenue NW, Washington, DC 20500"

SAMPLE_PROPERTY = {
    "address": REAL_ADDRESS,
    "purchase_price": 400000,
    "down_payment": 80000,
    "loan_interest_rate": 6.5,
    "loan_term_years": 30,
    "monthly_rental_income": 2800,
    "monthly_expenses": 550,
}


def test_session_cannot_access_another_sessions_property():
    client_a = TestClient(app)
    client_b = TestClient(app)

    created_ids = []
    try:
        create_response = client_a.post("/properties", json=SAMPLE_PROPERTY)
        assert create_response.status_code == 200
        property_id = create_response.json()["id"]
        created_ids.append(property_id)

        get_response = client_b.get(f"/properties/{property_id}")
        assert get_response.status_code == 404

        update_response = client_b.put(f"/properties/{property_id}", json={"monthly_expenses": 999})
        assert update_response.status_code == 404

        delete_response = client_b.delete(f"/properties/{property_id}")
        assert delete_response.status_code == 404

        confirm_response = client_a.get(f"/properties/{property_id}")
        assert confirm_response.status_code == 200

    finally:
        for pid in created_ids:
            client_a.delete(f"/properties/{pid}")


def test_own_session_can_access_own_property():
    client = TestClient(app)
    created_ids = []
    try:
        create_response = client.post("/properties", json=SAMPLE_PROPERTY)
        assert create_response.status_code == 200
        property_id = create_response.json()["id"]
        created_ids.append(property_id)

        get_response = client.get(f"/properties/{property_id}")
        assert get_response.status_code == 200
        assert get_response.json()["address"] == REAL_ADDRESS

    finally:
        for pid in created_ids:
            client.delete(f"/properties/{pid}")
