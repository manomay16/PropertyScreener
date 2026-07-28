import { useState, useEffect } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [properties, setProperties] = useState([]);
  const [form, setForm] = useState({
    address: "",
    purchase_price: "",
    down_payment: "",
    loan_interest_rate: "",
    loan_term_years: "",
    monthly_rental_income: "",
    monthly_expenses: "",
  });

  useEffect(() => {
    fetchProperties();
  }, []);

  function fetchProperties() {
    fetch(`${API_URL}/properties`, { credentials: "include" })
      .then((res) => res.json())
      .then((data) => setProperties(data));
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    fetch(`${API_URL}/properties`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        address: form.address,
        purchase_price: parseFloat(form.purchase_price),
        down_payment: parseFloat(form.down_payment),
        loan_interest_rate: parseFloat(form.loan_interest_rate),
        loan_term_years: parseInt(form.loan_term_years),
        monthly_rental_income: parseFloat(form.monthly_rental_income),
        monthly_expenses: parseFloat(form.monthly_expenses),
      }),
    }).then(() => {
      fetchProperties();
      setForm({
        address: "",
        purchase_price: "",
        down_payment: "",
        loan_interest_rate: "",
        loan_term_years: "",
        monthly_rental_income: "",
        monthly_expenses: "",
      });
    });
  }

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Property Screener</h1>

      <form onSubmit={handleSubmit}>
        <input name="address" placeholder="Address" value={form.address} onChange={handleChange} required />
        <input name="purchase_price" placeholder="Purchase Price" value={form.purchase_price} onChange={handleChange} required />
        <input name="down_payment" placeholder="Down Payment" value={form.down_payment} onChange={handleChange} required />
        <input name="loan_interest_rate" placeholder="Interest Rate (%)" value={form.loan_interest_rate} onChange={handleChange} required />
        <input name="loan_term_years" placeholder="Loan Term (years)" value={form.loan_term_years} onChange={handleChange} required />
        <input name="monthly_rental_income" placeholder="Monthly Rental Income" value={form.monthly_rental_income} onChange={handleChange} required />
        <input name="monthly_expenses" placeholder="Monthly Expenses" value={form.monthly_expenses} onChange={handleChange} required />
        <button type="submit">Add Property</button>
      </form>

      <h2>Your Properties</h2>
      <ul>
        {properties.map((p) => (
          <li key={p.id}>
            {p.address} — ${p.purchase_price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;