import { useState, useEffect, useContext, createContext } from "react";
import * as authService from "../services/authService";

const AuthContext = createContext(null);

/* ---------------- AUTH PROVIDER ---------------- */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // ---------------- INIT AUTH ---------------- //
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await authService.getCurrentUser();

        if (res) {
          setUser({
            email: res.email,
            id: res.id,
          });
          setIsAuthenticated(true);
        }
      } catch (err) {
        console.error("Auth sync failed:", err);
        authService.logout();
        localStorage.removeItem("access_token");
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  // ---------------- LOGIN ---------------- //
  const login = async (data) => {
    try {
      const response = await authService.login(data);

      const token = response.access_token;
      if (token) {
        localStorage.setItem("access_token", token);
      }

      // Fetch user after login
      const res = await authService.getCurrentUser();

      if (res) {
        setUser({
          email: res.email,
          id: res.id,
        });
      }

      setIsAuthenticated(true);
      return response;

    } catch (error) {
      setIsAuthenticated(false);
      throw error;
    }
  };

  // ---------------- REGISTER ---------------- //
  const register = async (data) => {
    try {
      const response = await authService.register(data);
      return response;
    } catch (error) {
      throw error;
    }
  };

  // ---------------- LOGOUT ---------------- //
  const logout = () => {
    authService.logout();
    localStorage.removeItem("access_token");
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/* ---------------- CUSTOM HOOK ---------------- */
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
};