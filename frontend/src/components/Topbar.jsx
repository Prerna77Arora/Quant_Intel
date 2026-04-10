import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { FiLogOut, FiUser, FiBell, FiSearch } from "react-icons/fi";
import * as authService from "../services/authService";

export default function Topbar() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [showMenu, setShowMenu] = useState(false);
  const [user, setUser] = useState(authService.getUser());

  const handleLogout = async () => {
    await authService.logout();
    setShowMenu(false);
    navigate("/login");
  };

  const handleProfileClick = () => {
    navigate("/profile");
    setShowMenu(false);
  };

  return (
    <div className="bg-[#0B0F1A] border-b border-[#1f2937] px-6 py-4 sticky top-0 z-40 backdrop-blur-md">
      <div className="flex items-center justify-between gap-4">

        {/* Left: Title */}
        <div>
          <h2 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
            Dashboard
          </h2>
        </div>

        {/* Center: Search */}
        <div className="flex-1 max-w-md">
          <div className="relative hidden md:block">
            <FiSearch className="absolute left-3 top-3 text-gray-500" />
            <input
              type="text"
              placeholder="Search stocks (TCS, INFY...)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg bg-[#1A2235] border border-[#2A3441] text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">

          {/* Notification Bell */}
          <button className="relative p-2 rounded-lg bg-[#1A2235] hover:bg-[#243047] transition">
            <FiBell size={18} className="text-gray-300" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-green-400 rounded-full animate-ping"></span>
          </button>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="flex items-center gap-3 px-3 py-2 rounded-lg bg-[#1A2235] hover:bg-[#243047] transition"
            >
              <div className="w-9 h-9 rounded-full bg-gradient-to-r from-blue-500 to-green-400 flex items-center justify-center text-white text-sm font-bold shadow-md">
                {user?.email?.[0]?.toUpperCase() || "U"}
              </div>
              <span className="text-sm text-gray-300 hidden sm:inline">
                {user?.email || "User"}
              </span>
            </button>

            {/* Dropdown */}
            {showMenu && (
              <div className="absolute right-0 mt-3 w-52 bg-[#1A2235] border border-[#2A3441] rounded-xl shadow-xl py-2 z-50">

                <div className="px-4 py-2 border-b border-[#2A3441]">
                  <p className="text-sm text-white">{user?.email || "User"}</p>
                  <p className="text-xs text-gray-500">AI Investor</p>
                </div>

                <button
                  onClick={handleProfileClick}
                  className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#243047] flex items-center gap-2 transition"
                >
                  <FiUser size={16} />
                  Profile
                </button>

                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-red-400 hover:bg-red-500/10 flex items-center gap-2 transition"
                >
                  <FiLogOut size={16} />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}