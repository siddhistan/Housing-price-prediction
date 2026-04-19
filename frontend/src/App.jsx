import { useState } from "react";

function App() {
  const [formData, setFormData] = useState({
    OverallQual: "",
    GrLivArea: "",
    GarageCars: "",
    TotalBsmtSF: "",
    FullBath: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const backendUrl =
    import.meta.env.VITE_BACKEND_URL ||
    "http://127.0.0.1:8000";

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    // Basic validation
    if (Object.values(formData).some((val) => val === "")) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${backendUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          OverallQual: Number(formData.OverallQual),
          GrLivArea: Number(formData.GrLivArea),
          GarageCars: Number(formData.GarageCars),
          TotalBsmtSF: Number(formData.TotalBsmtSF),
          FullBath: Number(formData.FullBath)
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.predicted_price);
    } catch (error) {
      console.error(error);
      alert("Something went wrong. Check backend or network.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>House Price Predictor</h1>

      <div style={{ display: "inline-block" }}>
        <input name="OverallQual" placeholder="Overall Quality" onChange={handleChange} /><br />
        <input name="GrLivArea" placeholder="Living Area" onChange={handleChange} /><br />
        <input name="GarageCars" placeholder="Garage Cars" onChange={handleChange} /><br />
        <input name="TotalBsmtSF" placeholder="Basement Area" onChange={handleChange} /><br />
        <input name="FullBath" placeholder="Bathrooms" onChange={handleChange} /><br /><br />

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {result && (
        <h2 style={{ marginTop: "20px" }}>
          Price: ${result.toFixed(2)}
        </h2>
      )}
    </div>
  );
}

export default App;