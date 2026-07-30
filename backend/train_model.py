import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import joblib

df = pd.read_csv("data/synthetic_training_data.csv")

df["disaster_risk_score"] = df["disaster_risk_score"].fillna(50)

feature_columns = [
    "purchase_price",
    "down_payment",
    "loan_interest_rate",
    "loan_term_years",
    "monthly_rental_income",
    "monthly_expenses",
    "disaster_risk_score",
    "monthly_mortgage_payment",
    "cap_rate",
    "monthly_cash_flow",
    "roi",
    "break_even_ratio",
]

X = df[feature_columns]
y = df["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    random_state=42,
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print(f"Test RMSE: {rmse:.2f}")
print(f"Test R²: {r2:.4f}")

joblib.dump(model, "risk_model.joblib")
joblib.dump(feature_columns, "model_features.joblib")
print("Model saved to risk_model.joblib")
