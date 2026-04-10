import { useEffect, useState } from "react";
import { getRecommendations } from "../services/recommendationService";
import { useAuth } from "../hooks/useAuth";
import Loader from "../components/Loader";

export default function Recommendations() {
  const { user } = useAuth();

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState("all");
  const [risk, setRisk] = useState("medium");
  const [time, setTime] = useState("1month");

  /* ---------------- FETCH DATA ---------------- */
  const fetchRecommendations = async () => {
    try {
      setLoading(true);

      const res = await getRecommendations(risk);

      setData(res.data || []);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) fetchRecommendations();
  }, [user, risk, time]);

  /* ---------------- FILTER ---------------- */
  const filteredData =
    activeFilter === "all"
      ? data
      : data.filter((rec) => {
          const action = String(rec.action || "").toLowerCase();
          if (activeFilter === "buy") return action.includes("buy");
          if (activeFilter === "sell") return action.includes("sell");
          return action.includes("hold");
        });

  /* ---------------- UI HELPERS ---------------- */
  const getRecCardClass = (action) => {
    const a = String(action || "").toLowerCase();
    if (a.includes("buy")) return "rec-buy";
    if (a.includes("sell")) return "rec-sell";
    return "rec-hold";
  };

  const getActionBadgeClass = (action) => {
    const a = String(action || "").toLowerCase();
    if (a.includes("buy")) return "rec-action-badge badge-buy";
    if (a.includes("sell")) return "rec-action-badge badge-sell";
    return "rec-action-badge badge-hold";
  };

  return (
    <div>

      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span className="glow-dot"></span>
          <h1 className="page-h1">AI Recommendations</h1>
        </div>
        <p className="page-sub">
          Personalized ML-driven buy/sell signals with risk management
        </p>
      </div>

      {/* Controls */}
      <div className="flex gap-4 flex-wrap mb-4">

        {/* Risk */}
        {["low", "medium", "high"].map((r) => (
          <button
            key={r}
            className={`filter-btn ${risk === r ? "active" : ""}`}
            onClick={() => setRisk(r)}
          >
            {r.toUpperCase()}
          </button>
        ))}

        {/* Time */}
        {["1week", "1month", "3months", "1year"].map((t) => (
          <button
            key={t}
            className={`filter-btn ${time === t ? "active" : ""}`}
            onClick={() => setTime(t)}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Action Filters */}
      <div className="rec-filters">
        {["all", "buy", "sell", "hold"].map((f) => (
          <button
            key={f}
            className={`filter-btn ${activeFilter === f ? "active" : ""}`}
            onClick={() => setActiveFilter(f)}
          >
            {f.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="loading-card">
          <Loader />
          <div className="loading-text">Running AI analysis...</div>
        </div>
      ) : filteredData.length === 0 ? (
        <div className="loading-card">
          <div className="loading-text">
            No recommendations found for selected filters
          </div>
        </div>
      ) : (
        <div className="rec-list">
          {filteredData.map((rec, idx) => (
            <div key={idx} className={`rec-card ${getRecCardClass(rec.action)}`}>

              {/* Top */}
              <div className="rec-top">
                <div>
                  <div className="rec-sym">{rec.symbol}</div>
                  <div className="rec-name">{rec.name || "Stock"}</div>
                </div>

                <span className={getActionBadgeClass(rec.action)}>
                  {rec.action}
                </span>

                <div>
                  <div className="rec-price-val">
                    ₹{parseFloat(rec.current_price || 0).toFixed(2)}
                  </div>
                </div>
              </div>

              {/* Metrics */}
              <div className="rec-details">
                <div>Target: ₹{rec.target_price}</div>
                <div>Stop Loss: ₹{rec.stop_loss}</div>
                <div>Confidence: {Math.round((rec.confidence || 0) * 100)}%</div>
                <div>Risk: {rec.risk_level}</div>
              </div>

              {/* Explanation */}
              <div className="rec-explanation">
                {rec.reason && <p>{rec.reason}</p>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}