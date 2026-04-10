import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { FiMail, FiLock, FiArrowRight } from "react-icons/fi";

export default function Register() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    passwordConfirm: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // ✅ Validation
    if (!form.email || !form.password || !form.passwordConfirm) {
      setError("Please fill all fields");
      return;
    }

    if (form.password !== form.passwordConfirm) {
      setError("Passwords do not match");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      // ✅ FIXED: send object instead of separate params
      await register({
        email: form.email,
        password: form.password
      });

      // smooth UX
      setTimeout(() => navigate("/login"), 400);

    } catch (err) {
      const message =
        err?.detail ||
        err?.message ||
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Registration failed. Try again.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center px-4">
      <div className="w-full max-w-md">

        {/* Branding */}
        <div className="text-center mb-8">
          <div className="relative inline-flex items-center justify-center mb-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-primary flex items-center justify-center text-white font-bold text-lg shadow-lg">
              TM
            </div>
            <div className="absolute inset-0 rounded-xl bg-primary opacity-20 blur-xl"></div>
          </div>

          <h1 className="text-3xl font-bold text-text-primary mb-2">
            Create Account
          </h1>

          <p className="text-text-muted">
            Start your AI-powered investing journey
          </p>
        </div>

        {/* Card */}
        <div className="bg-dark-card border border-border-color rounded-2xl p-8 shadow-xl">

          {/* Tabs */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => navigate("/login")}
              className="flex-1 py-2 text-center text-text-muted font-semibold border-b-2 border-transparent hover:text-text-secondary transition"
            >
              Sign In
            </button>

            <button className="flex-1 py-2 text-center text-primary font-semibold border-b-2 border-primary">
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

            {/* Email */}
            <div>
              <label className="form-label">Email</label>
              <div className="relative">
                <FiMail className="absolute left-3 top-3 text-text-muted" />
                <input
                  type="email"
                  placeholder="you@example.com"
                  value={form.email}
                  onChange={(e) =>
                    setForm({ ...form, email: e.target.value })
                  }
                  className="form-input pl-10 focus:ring-2 focus:ring-primary transition"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="form-label">Password</label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-text-muted" />
                <input
                  type="password"
                  placeholder="••••••••"
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                  className="form-input pl-10 focus:ring-2 focus:ring-primary transition"
                />
              </div>
              <p className="text-xs text-text-muted mt-1">
                Minimum 6 characters
              </p>
            </div>

            {/* Confirm Password */}
            <div>
              <label className="form-label">Confirm Password</label>
              <div className="relative">
                <FiLock className="absolute left-3 top-3 text-text-muted" />
                <input
                  type="password"
                  placeholder="••••••••"
                  value={form.passwordConfirm}
                  onChange={(e) =>
                    setForm({ ...form, passwordConfirm: e.target.value })
                  }
                  className="form-input pl-10 focus:ring-2 focus:ring-primary transition"
                />
              </div>
            </div>

            {/* Button */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full btn btn-primary flex items-center justify-center gap-2 py-3 mt-6 transition ${
                loading ? "opacity-70 cursor-not-allowed" : "hover:scale-[1.02]"
              }`}
            >
              {loading ? "Creating Account..." : "Create Account"}
              {!loading && <FiArrowRight />}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border-color"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-dark-card text-text-muted">
                Already registered?
              </span>
            </div>
          </div>

          {/* Login */}
          <button
            onClick={() => navigate("/login")}
            className="w-full btn btn-secondary py-3 hover:scale-[1.02] transition"
          >
            Sign In Instead
          </button>
        </div>

        {/* Footer */}
        <p className="text-center text-text-muted text-sm mt-6">
          Secure • AI-powered • Built for smart investors
        </p>
      </div>
    </div>
  );
}