import { useState, useEffect } from "react";

const API_URL = "http://localhost:8000";

const emptyForm = {
  address: "",
  purchase_price: "",
  down_payment: "",
  loan_interest_rate: "",
  loan_term_years: "",
  monthly_rental_income: "",
  monthly_expenses: "",
};

function App() {
  const [properties, setProperties] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState(emptyForm);

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
    setError("");
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
    }).then((res) => {
      if (!res.ok) {
        setError("Could not add property — check that all fields are filled in correctly.");
        return;
      }
      fetchProperties();
      setForm(emptyForm);
    });
  }

  function startEditing(property) {
    setEditingId(property.id);
    setEditForm({
      address: property.address,
      purchase_price: property.purchase_price,
      down_payment: property.down_payment,
      loan_interest_rate: property.loan_interest_rate,
      loan_term_years: property.loan_term_years,
      monthly_rental_income: property.monthly_rental_income,
      monthly_expenses: property.monthly_expenses,
    });
  }

  function cancelEditing() {
    setEditingId(null);
    setEditForm(emptyForm);
  }

  function handleEditChange(e) {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  }

  function saveEdit(propertyId) {
    setError("");
    fetch(`${API_URL}/properties/${propertyId}`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        address: editForm.address,
        purchase_price: parseFloat(editForm.purchase_price),
        down_payment: parseFloat(editForm.down_payment),
        loan_interest_rate: parseFloat(editForm.loan_interest_rate),
        loan_term_years: parseInt(editForm.loan_term_years),
        monthly_rental_income: parseFloat(editForm.monthly_rental_income),
        monthly_expenses: parseFloat(editForm.monthly_expenses),
      }),
    }).then((res) => {
      if (!res.ok) {
        setError("Could not save changes — check that all fields are filled in correctly.");
        return;
      }
      setEditingId(null);
      fetchProperties();
    });
  }

  function deleteProperty(propertyId) {
    fetch(`${API_URL}/properties/${propertyId}`, {
      method: "DELETE",
      credentials: "include",
    }).then((res) => {
      if (res.ok) fetchProperties();
    });
  }

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
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

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Your Properties</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {properties.map((p) =>
          editingId === p.id ? (
            <li key={p.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
              <input name="address" value={editForm.address} onChange={handleEditChange} />
              <input name="purchase_price" value={editForm.purchase_price} onChange={handleEditChange} />
              <input name="down_payment" value={editForm.down_payment} onChange={handleEditChange} />
              <input name="loan_interest_rate" value={editForm.loan_interest_rate} onChange={handleEditChange} />
              <input name="loan_term_years" value={editForm.loan_term_years} onChange={handleEditChange} />
              <input name="monthly_rental_income" value={editForm.monthly_rental_income} onChange={handleEditChange} />
              <input name="monthly_expenses" value={editForm.monthly_expenses} onChange={handleEditChange} />
              <div>
                <button onClick={() => saveEdit(p.id)}>Save</button>
                <button onClick={cancelEditing}>Cancel</button>
              </div>
            </li>
          ) : (
            <li key={p.id} style={{ border: "1px solid #eee", padding: 10, marginBottom: 10 }}>
              <strong>{p.address}</strong>
              <div>Purchase Price: ${p.purchase_price}</div>
              <div>Down Payment: ${p.down_payment}</div>
              <div>Interest Rate: {p.loan_interest_rate}%</div>
              <div>Loan Term: {p.loan_term_years} years</div>
              <div>Monthly Rent: ${p.monthly_rental_income}</div>
              <div>Monthly Expenses: ${p.monthly_expenses}</div>

              <div style={{ marginTop: 8, paddingTop: 8, borderTop: "1px dashed #ccc" }}>
                <strong>Metrics</strong>
                <div>Monthly Mortgage Payment: ${p.metrics.monthly_mortgage_payment.toFixed(2)}</div>
                <div>Cap Rate: {p.metrics.cap_rate.toFixed(2)}%</div>
                <div>Monthly Cash Flow: ${p.metrics.monthly_cash_flow.toFixed(2)}</div>
                <div>ROI: {p.metrics.roi.toFixed(2)}%</div>
                <div>Break-Even Ratio: {p.metrics.break_even_ratio.toFixed(2)}%</div>
              </div>

              <div>
                <button onClick={() => startEditing(p)}>Edit</button>
                <button onClick={() => deleteProperty(p.id)}>Delete</button>
              </div>
            </li>
          )
        )}
      </ul>
    </div>
  );
}

export default App;