import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const API_BASE = "http://127.0.0.1:8000";

export default function Chart({ symbol = "TCS" }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchChartData = async () => {
    try {
      setLoading(true);

      // ✅ 1. Fetch stock price data
      const stockRes = await fetch(
        `${API_BASE}/stocks?symbol=${symbol}`
      );
      const stockData = await stockRes.json();

      // ✅ 2. Fetch prediction
      const predRes = await fetch(`${API_BASE}/prediction`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symbol }),
      });

      const predData = await predRes.json();

      // ✅ 3. Merge both datasets
      const merged = stockData.map((item, index) => ({
        ...item,
        prediction: predData?.predictions?.[index] || null,
      }));

      setData(merged);
    } catch (err) {
      console.error("Chart error:", err);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChartData();
  }, [symbol]);

  // 🔥 UI STATES

  if (loading) {
    return (
      <div className="flex items-center justify-center h-72 text-gray-400 animate-pulse">
        Loading market data...
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-72 text-gray-500">
        <p>No market data available</p>
        <button
          onClick={fetchChartData}
          className="mt-3 px-4 py-2 bg-blue-600 rounded-lg text-white"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="w-full h-80 bg-[#0B0F1A] rounded-xl p-4 border border-[#1f2937]">
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="price" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
            </linearGradient>

            <linearGradient id="prediction" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22C55E" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#22C55E" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />

          <XAxis dataKey="date" stroke="#6b7280" />
          <YAxis stroke="#6b7280" />

          <Tooltip
            contentStyle={{
              backgroundColor: "#111827",
              borderRadius: "10px",
              border: "1px solid #1f2937",
            }}
          />

          {/* Actual */}
          <Area
            type="monotone"
            dataKey="close"
            stroke="#3B82F6"
            fill="url(#price)"
            strokeWidth={2}
          />

          {/* Prediction */}
          <Area
            type="monotone"
            dataKey="prediction"
            stroke="#22C55E"
            fill="url(#prediction)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}