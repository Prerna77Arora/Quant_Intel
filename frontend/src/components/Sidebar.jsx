import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const navItems = [
    { name: "Dashboard", path: "/", icon: "📊" },
    { name: "Analysis", path: "/analysis", icon: "📈" },
    { name: "AI Advisor", path: "/advisor", icon: "🤖" },
    { name: "Recommendations", path: "/recommendations", icon: "⭐", badge: 5 },
  ];

  return (
    <aside className="w-64 h-screen bg-[#0B0F1A] border-r border-[#1f2937] text-white flex flex-col justify-between">

      {/* Logo */}
      <div className="p-6 border-b border-[#1f2937]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-green-400 rounded-lg flex items-center justify-center font-bold text-lg shadow-lg">
            T
          </div>
          <div>
            <div className="font-bold text-lg bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
              TradeMind
            </div>
            <div className="text-xs text-gray-500">AI Engine</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2 px-4 py-6">
        <div className="text-xs text-gray-500 mb-3 tracking-wide">MENU</div>

        {navItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 ${
                isActive
                  ? "bg-gradient-to-r from-blue-600/20 to-green-400/20 text-white border border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.2)]"
                  : "text-gray-400 hover:bg-[#1A2235] hover:text-white"
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-lg">{item.icon}</span>
                <span className="text-sm font-medium">{item.name}</span>
              </div>

              {/* Badge */}
              {item.badge && (
                <span className="bg-blue-500/20 text-blue-400 text-xs px-2 py-0.5 rounded-full border border-blue-500/30">
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-[#1f2937]">
        <div className="flex items-center gap-2 text-sm text-green-400">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-ping"></span>
          <span>Market Live</span>
        </div>

        {/* Extra AI Status */}
        <div className="mt-2 text-xs text-gray-500">
          AI Models Active
        </div>
      </div>
    </aside>
  );
}