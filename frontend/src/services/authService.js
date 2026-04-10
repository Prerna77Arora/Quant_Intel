import API from "./api";

const TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_KEY = "user";

// ---------------------- LOGIN ---------------------- //
export const login = async (data) => {
  try {
    const response = await API.post("/auth/login", data);

    const resData = response.data;

    // Store tokens if present
    if (resData?.access_token) {
      localStorage.setItem(TOKEN_KEY, resData.access_token);

      if (resData.refresh_token) {
        localStorage.setItem(REFRESH_TOKEN_KEY, resData.refresh_token);
      }
    }

    // ✅ Ensure consistent success response
    return {
      success: true,
      ...resData,
    };

  } catch (error) {
    const errorData = error.response?.data;

    if (errorData?.detail) {
      throw { detail: errorData.detail };
    } else if (errorData?.message) {
      throw { detail: errorData.message };
    }

    throw { detail: "Login failed" };
  }
};


// ---------------------- REGISTER ---------------------- //
export const register = async (data) => {
  try {
    const response = await API.post("/auth/register", data);

    const resData = response.data;

    // ✅ Force success flag for frontend consistency
    return {
      success: true,
      ...resData,
    };

  } catch (error) {
    const errorData = error.response?.data;

    if (errorData?.detail) {
      throw { detail: errorData.detail };
    } else if (errorData?.message) {
      throw { detail: errorData.message };
    }

    throw { detail: "Registration failed" };
  }
};


// ---------------------- LOGOUT ---------------------- //
export const logout = async () => {
  try {
    await API.post("/auth/logout");
  } catch (error) {
    // silent fail
  }

  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};


// ---------------------- AUTH HELPERS ---------------------- //
export const isAuthenticated = () => {
  return !!localStorage.getItem(TOKEN_KEY);
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const getUser = () => {
  try {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  } catch {
    return null;
  }
};


// ---------------------- CURRENT USER ---------------------- //
export const getCurrentUser = async () => {
  try {
    const response = await API.get("/auth/me");

    const resData = response.data;

    if (resData?.data) {
      localStorage.setItem(USER_KEY, JSON.stringify(resData.data));
      return resData.data;
    }

    return null;
  } catch (error) {
    return null;
  }
};


// ✅ Alias for compatibility
export const getMe = getCurrentUser;