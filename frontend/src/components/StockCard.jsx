export default function StockCard({ stock = {} }) {
  const getRiskColor = (risk) => {
    const level = String(risk || "medium").toLowerCase();
    if (level === "low") return "bg-green-500/20 text-green-400 border-green-500/30";
    if (level === "high") return "bg-red-500/20 text-red-400 border-red-500/30";
    return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
  };

  const price = parseFloat(stock.price || 0);
  const change = parseFloat(stock.change || 0);
  const isPositive = change >= 0;

  return (
    <div className="bg-[#0B0F1A] border border-[#1f2937] rounded-xl p-5 shadow-md hover:shadow-[0_0_20px_rgba(59,130,246,0.15)] hover:scale-[1.02] transition-all duration-300">

      {/* Top Section */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="text-lg font-semibold text-white tracking-wide">
            {stock.symbol || "N/A"}
          </div>
          <div className="text-xs text-gray-500">
            {stock.name || stock.sector || "Unknown"}
          </div>
        </div>

        {/* Risk Badge */}
        <span
          className={`text-xs px-2 py-1 rounded-full border ${getRiskColor(
            stock.risk_level
          )}`}
        >
          {stock.risk_level || "MEDIUM"}
        </span>
      </div>

      {/* Price */}
      <div className="text-3xl font-bold text-white mb-1">
        ₹{price.toFixed(2)}
      </div>

      {/* Change */}
      <div
        className={`text-sm font-medium flex items-center gap-1 ${
          isPositive ? "text-green-400" : "text-red-400"
        }`}
      >
        <span className="text-lg">{isPositive ? "▲" : "▼"}</span>
        {Math.abs(change).toFixed(2)}%
      </div>

      {/* Divider */}
      <div className="border-t border-[#1f2937] my-4"></div>

      {/* Meta Info */}
      <div className="flex justify-between text-sm">
        <div>
          <div className="text-white font-semibold">
            {stock.volume || "0"}
          </div>
          <div className="text-gray-500 text-xs">Volume</div>
        </div>

        <div>
          <div className="text-white font-semibold">
            {stock.pe_ratio || "N/A"}
          </div>
          <div className="text-gray-500 text-xs">P/E Ratio</div>
        </div>
      </div>
    </div>
  );
}