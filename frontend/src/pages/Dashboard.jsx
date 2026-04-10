import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getStocks } from "../services/stockService";
import { refreshData } from "../services/pipelineService";
import { useAuth } from "../hooks/useAuth";
import StockCard from "../components/StockCard";
import { FiRefreshCw, FiAlertCircle } from "react-icons/fi";

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();

  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  /* ---------------- PROFILE CHECK ---------------- */
  useEffect(() => {
    if (!authLoading && user) {
      if (!user.profile_complete) {
        const hasSkipped = sessionStorage.getItem("profile_skip_" + user.id);
        if (!hasSkipped) {
          navigate("/profile");
        }
      }
    }
  }, [user, authLoading, navigate]);

  /* ---------------- FETCH STOCKS ---------------- */
  const fetchStocks = async () => {
    try {
      setLoading(true);
      setError(null);

      const res = await getStocks();
      const data = Array.isArray(res.data) ? res.data : [];
      setStocks(data);
    } catch (err) {
      const errorMessage =
        err?.response?.data?.detail || err?.message || "Failed to load stocks";
      setError(errorMessage);
      setStocks([]);
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- INITIAL LOAD ---------------- */
  useEffect(() => {
    fetchStocks();
  }, []);

  /* ---------------- REFRESH PIPELINE ---------------- */
  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      setError(null);

      await refreshData(); // triggers ML/data pipeline
      await fetchStocks();
    } catch (err) {
      const errorMessage =
        err?.response?.data?.detail || err?.message || "Refresh failed";
      setError(errorMessage);
    } finally {
      setRefreshing(false);
    }
  };

  return (
    <div className="p-6 space-y-6">

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-1">Dashboard</h1>
          <p className="text-text-muted">
            Real-time market insights & AI-powered signals
          </p>
        </div>

        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="btn btn-primary flex items-center gap-2 px-6"
        >
          <FiRefreshCw className={refreshing ? "animate-spin" : ""} size={18} />
          {refreshing ? "Running AI Pipeline..." : "Refresh Data"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-900 bg-opacity-30 border border-red-500 rounded-lg p-4 flex items-start gap-3">
          <FiAlertCircle className="text-danger mt-1" size={20} />
          <div>
            <h3 className="text-danger font-semibold">Error</h3>
            <p className="text-text-secondary text-sm">{error}</p>
            <button
              onClick={fetchStocks}
              className="text-primary text-sm mt-2 hover:underline"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-text-muted text-sm">Portfolio Value</p>
          <h2 className="text-3xl font-bold text-text-primary">₹4.8L</h2>
          <span className="badge badge-success">+2.6%</span>
        </div>

        <div className="card">
          <p className="text-text-muted text-sm">Active Positions</p>
          <h2 className="text-3xl font-bold text-text-primary">14</h2>
          <span className="badge badge-warning">2 alerts</span>
        </div>

        <div className="card">
          <p className="text-text-muted text-sm">P&L</p>
          <h2 className="text-3xl font-bold text-success">₹18.4K</h2>
          <span className="badge badge-success">+4.2%</span>
        </div>

        <div className="card">
          <p className="text-text-muted text-sm">AI Signals</p>
          <h2 className="text-3xl font-bold text-primary">7</h2>
          <span className="badge bg-blue-900 bg-opacity-50 text-primary">
            Strong Buy
          </span>
        </div>
      </div>

      {/* Stocks */}
      <div>
        <h2 className="text-2xl font-bold text-text-primary mb-4">
          Top Stocks
        </h2>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="loader-ai"></div>
          </div>
        ) : stocks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stocks.map((stock) => (
              <StockCard key={stock?.id || stock?.symbol} stock={stock} />
            ))}
          </div>
        ) : (
          <div className="card text-center py-12">
            <p className="text-text-muted">
              No stocks available. Try refreshing.
            </p>
            <button onClick={handleRefresh} className="btn btn-primary mt-4">
              Refresh Data
            </button>
          </div>
        )}
      </div>

    </div>
  );
}