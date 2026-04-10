import { useState } from "react";
import { getRecommendations } from "../services/recommendationService";
import { useAuth } from "../hooks/useAuth";

export default function Advisor() {
  const { user } = useAuth();

  const [selectedRisk, setSelectedRisk] = useState("medium");
  const [selectedTime, setSelectedTime] = useState("1month");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateSuggestions = async () => {
    setLoading(true);
    try {
      const res = await getRecommendations({
        risk: selectedRisk,
        time_horizon: selectedTime,
        user_id: user?.id
      });

      setSuggestions(res.data || []);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (action) => {
    const actionLower = String(action || '').toLowerCase();
    if (actionLower.includes('buy')) return 'badge-buy';
    if (actionLower.includes('sell')) return 'badge-sell';
    return 'badge-hold';
  };

  return (
    <div className="advisor-wrap">

      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span className="glow-dot"></span>
          <h1 className="page-h1">AI Advisor</h1>
        </div>
        <p className="page-sub">
          Personalized ML-powered stock recommendations based on your risk profile
        </p>
      </div>

      {/* Risk Selector */}
      <div className="risk-selector-card">
        <h2>Select Risk Profile</h2>
        <p>Choose your investment strategy</p>

        <div className="risk-options">
          <button
            className={`risk-option risk-sel-low ${selectedRisk === 'low' ? 'selected' : ''}`}
            onClick={() => setSelectedRisk('low')}
          >
            <div className="risk-icon">🛡️</div>
            <div className="risk-label">Conservative</div>
            <div className="risk-desc">Low risk, stable returns</div>
          </button>

          <button
            className={`risk-option risk-sel-medium ${selectedRisk === 'medium' ? 'selected' : ''}`}
            onClick={() => setSelectedRisk('medium')}
          >
            <div className="risk-icon">⚖️</div>
            <div className="risk-label">Balanced</div>
            <div className="risk-desc">Moderate growth</div>
          </button>

          <button
            className={`risk-option risk-sel-high ${selectedRisk === 'high' ? 'selected' : ''}`}
            onClick={() => setSelectedRisk('high')}
          >
            <div className="risk-icon">🚀</div>
            <div className="risk-label">Aggressive</div>
            <div className="risk-desc">High returns, high risk</div>
          </button>
        </div>

        {/* Time Horizon */}
        <div className="time-row">
          <span className="time-label">Time Horizon</span>
          {['1week', '1month', '3months', '1year'].map((period) => (
            <button
              key={period}
              className={`time-pill ${selectedTime === period ? 'active' : ''}`}
              onClick={() => setSelectedTime(period)}
            >
              {period === '1week' ? '1W' :
               period === '1month' ? '1M' :
               period === '3months' ? '3M' : '1Y'}
            </button>
          ))}
        </div>

        {/* Generate Button */}
        <button
          className="btn-generate"
          onClick={generateSuggestions}
          disabled={loading}
        >
          {loading ? "Analyzing Market..." : "Generate AI Recommendations"}
        </button>
      </div>

      {/* Results */}
      {suggestions.length > 0 && (
        <div style={{ marginTop: "24px" }}>
          <div className="section-title">AI Recommendations</div>

          <div className="suggestions-grid">
            {suggestions.map((rec, idx) => (
              <div key={idx} className="suggestion-card">

                {/* Top */}
                <div className="sug-top">
                  <div className="sug-symbol">
                    {rec.symbol || `STOCK${idx}`}
                  </div>
                  <span className={`sug-action-badge ${getRiskColor(rec.action)}`}>
                    {rec.action || 'HOLD'}
                  </span>
                </div>

                {/* Reason */}
                <div className="sug-reason">
                  {rec.reason || "AI analysis suggests strong potential based on trends and fundamentals."}
                </div>

                {/* Stats */}
                <div className="sug-stats">

                  <div className="sug-stat">
                    <strong>{Math.round((rec.confidence || 0) * 100)}%</strong>
                    Confidence
                  </div>

                  <div className="sug-stat">
                    <strong>{rec.target_price || 'N/A'}</strong>
                    Target
                  </div>

                  <div className="sug-stat">
                    <strong>{rec.stop_loss || 'N/A'}</strong>
                    Stop Loss
                  </div>

                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && suggestions.length === 0 && (
        <div className="loading-card" style={{ marginTop: "40px" }}>
          <div className="loading-text">
            Generate recommendations to see AI-powered stock insights
          </div>
        </div>
      )}

    </div>
  );
}