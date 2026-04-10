import { useState, useEffect } from "react";
import { getPrediction } from "../services/predictionService";
import Loader from "../components/Loader";

export default function StockAnalysis() {
  const [selectedStock, setSelectedStock] = useState("TCS");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeChart, setActiveChart] = useState("1D");
  const [error, setError] = useState("");

  const stocks = ["RELIANCE", "TCS", "HDFC BANK", "ZOMATO", "INFY", "BAJAJ"];

  /* ---------------- FETCH PREDICTION ---------------- */
  const fetchPrediction = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await getPrediction(selectedStock);

      setResult(res.data || {});
    } catch (err) {
      console.error("Prediction error:", err);
      setError("Failed to fetch prediction");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  /* Auto-refresh when stock/time changes */
  useEffect(() => {
    fetchPrediction();
  }, [selectedStock, activeChart]);

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
    setResult(null);
  };

  /* ---------------- SIGNAL LOGIC ---------------- */
  const getSignal = () => {
    if (!result) return "HOLD";
    if (result.predicted_price > result.current_price) return "BUY";
    if (result.predicted_price < result.current_price) return "SELL";
    return "HOLD";
  };

  return (
    <div>

      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span className="glow-dot"></span>
          <h1 className="page-h1">AI Stock Analysis</h1>
        </div>
        <p className="page-sub">
          Real-time ML predictions with technical insights
        </p>
      </div>

      {/* Stock Selector */}
      <div style={{ marginBottom: "24px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {stocks.map((stock) => (
          <button
            key={stock}
            className={selectedStock === stock ? "ticker-chip active" : "ticker-chip"}
            onClick={() => handleStockSelect(stock)}
          >
            {stock}
          </button>
        ))}
      </div>

      {/* Top Section */}
      <div className="analysis-top">

        {/* Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <div className="chart-title">{selectedStock} Price Chart</div>

            <div className="chart-tabs">
              {["1D", "1W", "1M", "3M", "1Y"].map((period) => (
                <button
                  key={period}
                  className={activeChart === period ? "chart-tab active" : "chart-tab"}
                  onClick={() => setActiveChart(period)}
                >
                  {period}
                </button>
              ))}
            </div>
          </div>

          <div className="chart-placeholder">
            {/* You can plug your Chart component here */}
            Live chart coming soon...
          </div>
        </div>

        {/* AI Prediction */}
        <div className="ai-prediction-card">

          <div className="ai-badge">AI Prediction</div>

          {loading ? (
            <Loader />
          ) : error ? (
            <div className="loading-text">{error}</div>
          ) : result ? (
            <>
              <div className="prediction-value">
                ₹{parseFloat(result.predicted_price || 0).toFixed(2)}
              </div>

              <div className="prediction-label">
                Predicted Price ({activeChart})
              </div>

              {/* Confidence */}
              <div className="confidence-bar">
                <div className="conf-label">
                  <span>Confidence</span>
                  <span>{Math.round((result.confidence || 0) * 100)}%</span>
                </div>

                <div className="conf-track">
                  <div
                    className="conf-fill"
                    style={{ width: `${(result.confidence || 0) * 100}%` }}
                  />
                </div>
              </div>

              {/* Signal */}
              <div className="signal-row">
                <span
                  className={`signal-pill ${
                    getSignal() === "BUY"
                      ? "signal-buy"
                      : getSignal() === "SELL"
                      ? "signal-sell"
                      : "signal-neutral"
                  }`}
                >
                  {getSignal()}
                </span>
              </div>
            </>
          ) : null}

        </div>
      </div>

      {/* Metrics */}
      <div style={{ marginTop: "24px" }}>
        <div className="section-title">Market Metrics</div>

        <div className="analysis-metrics">
          <div className="metric-item">
            <div className="metric-label">Current Price</div>
            <div className="metric-val">
              ₹{parseFloat(result?.current_price || 0).toFixed(2)}
            </div>
          </div>

          <div className="metric-item">
            <div className="metric-label">Predicted Change</div>
            <div className="metric-val">
              {result?.predicted_price && result?.current_price
                ? `${(
                    ((result.predicted_price - result.current_price) /
                      result.current_price) *
                    100
                  ).toFixed(2)}%`
                : "N/A"}
            </div>
          </div>

          <div className="metric-item">
            <div className="metric-label">Confidence</div>
            <div className="metric-val">
              {Math.round((result?.confidence || 0) * 100)}%
            </div>
          </div>

          <div className="metric-item">
            <div className="metric-label">Signal</div>
            <div className="metric-val">{getSignal()}</div>
          </div>
        </div>
      </div>
    </div>
  );
}