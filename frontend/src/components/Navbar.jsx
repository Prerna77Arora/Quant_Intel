import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const navLinks = [
    { name: "Dashboard", path: "/" },
    { name: "Analysis", path: "/analysis" },
    { name: "AI Advisor", path: "/advisor" },
    { name: "Recommendations", path: "/recommendations" },
  ];

  return (
    <div className="bg-[#0B0F1A] border-b border-[#1f2937] text-white px-6 py-3 flex justify-between items-center shadow-lg">

      {/* Logo */}
      <h1 className="font-bold text-xl tracking-wide bg-gradient-to-r from-blue-500 via-cyan-400 to-green-400 bg-clip-text text-transparent">
        TradeMind AI
      </h1>

      {/* Navigation */}
      <div className="flex gap-8 text-sm">
        {navLinks.map((link) => {
          const isActive = location.pathname === link.path;

          return (
            <Link
              key={link.path}
              to={link.path}
              className={`relative px-2 py-1 transition-all duration-300 ${
                isActive
                  ? "text-blue-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {link.name}

              {/* Active underline glow */}
              {isActive && (
                <span className="absolute left-0 -bottom-1 w-full h-[2px] bg-blue-500 rounded-full shadow-[0_0_8px_#3B82F6]"></span>
              )}
            </Link>
          );
        })}
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">

        {/* Notification Bell */}
        <div className="relative cursor-pointer">
          <div className="w-9 h-9 flex items-center justify-center rounded-full bg-[#1A2235] hover:bg-[#243047] transition">
            🔔
          </div>
          <span className="absolute top-1 right-1 w-2 h-2 bg-green-400 rounded-full animate-ping"></span>
        </div>

        {/* Profile */}
        <div className="flex items-center gap-2 cursor-pointer group">
          <div className="w-9 h-9 rounded-full bg-gradient-to-r from-blue-500 to-green-400 flex items-center justify-center font-semibold shadow-md">
            P
          </div>

          {/* Dropdown */}
          <div className="absolute right-6 top-14 hidden group-hover:block bg-[#1A2235] border border-[#2A3441] rounded-xl p-3 shadow-xl w-40">
            <p className="text-sm text-gray-300">Prerna</p>
            <p className="text-xs text-gray-500 mb-2">Investor</p>
            <div className="border-t border-gray-700 my-2"></div>
            <button className="text-sm text-gray-400 hover:text-white w-full text-left">
              Settings
            </button>
            <button className="text-sm text-red-400 hover:text-red-500 w-full text-left mt-1">
              Logout
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}