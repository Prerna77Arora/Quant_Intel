import API from "./api";

// ---------------------- GET ALL STOCKS ---------------------- //
export const getStocks = async () => {
  try {
    const response = await API.get("/stocks/");

    const resData = response.data;

    return {
      success: true,
      data: resData?.data || resData || [],
      message: resData?.message || "Stocks fetched successfully",
    };
  } catch (error) {
    console.error("Stocks fetch failed:", error);

    return {
      success: false,
      data: [],
      message:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to fetch stocks",
    };
  }
};

// ---------------------- GET STOCK BY SYMBOL ---------------------- //
export const getStockBySymbol = async (symbol) => {
  try {
    const response = await API.get(`/stocks/search/${symbol}`);

    const resData = response.data;

    return {
      success: true,
      data: resData?.data || resData,
      message: resData?.message || "Stock fetched successfully",
    };
  } catch (error) {
    console.error("Stock fetch failed:", error);

    return {
      success: false,
      data: null,
      message:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to fetch stock",
    };
  }
};