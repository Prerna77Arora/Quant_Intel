import axios from "axios";

// Create axios instance with base config
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // useful if cookies/session ever used
});

// Request interceptor → attach JWT token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor → handle global errors (auth, etc.)
API.interceptors.response.use(
  (response) => response,
  (error) => {
    // Auto logout if token expired / unauthorized
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login"; // redirect to login
    }

    return Promise.reject(error);
  }
);

export default API;