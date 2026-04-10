import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";
import StockAnalysis from "./pages/StockAnalysis";
import Advisor from "./pages/Advisor";
import Recommendations from "./pages/Recommendations";
import ChatProfile from "./pages/ChatProfile";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { useAuth } from "./hooks/useAuth";
import './App.css';

// ---------------------- PROTECTED ROUTE ---------------------- //
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-card">
        <div className="loader"></div>
        <div className="loading-text">Initializing TradeMind...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// ---------------------- APP LAYOUT ---------------------- //
function AppLayout() {
  const location = useLocation();
  const { isAuthenticated, loading } = useAuth();

  const isAuthPage =
    location.pathname === "/login" || location.pathname === "/register";

  // ---------------------- LOADING STATE ---------------------- //
  if (loading) {
    return (
      <div className="loading-card">
        <div className="loader"></div>
        <div className="loading-text">Initializing TradeMind...</div>
      </div>
    );
  }

  // ---------------------- AUTH PAGES ---------------------- //
  if (isAuthPage) {
    return (
      <Routes>
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/" /> : <Login />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/" /> : <Register />}
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    );
  }

  // ---------------------- MAIN APP ---------------------- //
  return (
    <div className="app">
      <Sidebar />
      <div className="main">
        <Topbar />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/analysis" element={<ProtectedRoute><StockAnalysis /></ProtectedRoute>} />
            <Route path="/advisor" element={<ProtectedRoute><Advisor /></ProtectedRoute>} />
            <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><ChatProfile /></ProtectedRoute>} />

            {/* fallback */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

// ---------------------- ROOT ---------------------- //
function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}

export default App;