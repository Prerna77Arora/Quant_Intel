import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { FiMail, FiLock, FiArrowRight } from "react-icons/fi";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.email || !form.password) {
      setError("Please fill all fields");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // ✅ FIXED HERE
      await login({
        email: form.email,
        password: form.password
      });

      setTimeout(() => navigate("/"), 500);

    } catch (err) {
      const message =
        err?.detail ||
        err?.message ||
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Invalid email or password";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center px-4">
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="relative inline-flex items-center justify-center mb-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-primary flex items-center justify-center text-white font-bold text-lg shadow-lg">
              TM
            </div>
            <div className="absolute inset-0 rounded-xl bg-primary opacity-20 blur-xl"></div>
          </div>

          <h1 className="text-3xl font-bold text-text-primary mb-2">
            TradeMind
          </h1>

          <p className="text-text-muted">
            AI-powered stock intelligence platform
          </p>
        </div>

        {/* Card */}
        <div className="bg-dark-card border border-border-color rounded-2xl p-8 shadow-xl backdrop-blur">

          {/* Tabs */}
          <div className="flex gap-4 mb-6">
            <button className="flex-1 py-2 text-center text-primary font-semibold border-b-2 border-primary">
              Sign In
            </button>

            <button
              onClick={() => navigate("/register")}
              className="flex-1 py-2 text-center text-text-muted font-semibold border-b-2 border-transparent hover:text-text-secondary transition"
            >
              Sign Up
            </button>
          </div>

          {/* Error */}
          {error && (
            <div className="mb-4 p-3 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg text-danger text-sm animate-pulse">
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">

            <div>
              <label className="form-label">Email</label>
              <div className="relative">
                <FiMail className="absolute left-3 top-3 text-text-muted" />
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) =>
                    setForm({ ...form, email: e.target.value })
                  }
                  className="form-input pl-10"
                />
              </div>
            </div>

            <div>
              <label className="form-label">Password</label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-text-muted" />
                <input
                  type="password"
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                  className="form-input pl-10"
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full btn btn-primary py-3 mt-6">
              {loading ? "Authenticating..." : "Sign In"}
            </button>
          </form>

          <div className="my-6 text-center text-text-muted">
            New to TradeMind?
          </div>

          <button
            onClick={() => navigate("/register")}
            className="w-full btn btn-secondary py-3"
          >
            Create New Account
          </button>
        </div>
      </div>
    </div>
  );
}