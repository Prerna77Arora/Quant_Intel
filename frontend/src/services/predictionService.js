import API from "./api";

// ---------------------- GET STOCK PREDICTION ---------------------- //
export const getPrediction = async (symbol) => {
  try {
    const response = await API.get(`/prediction/${symbol}`);

    const resData = response.data;

    return {
      success: true,
      data: resData?.data || resData,
      message: resData?.message || "Prediction fetched successfully",
    };
  } catch (error) {
    console.error("Prediction fetch failed:", error);

    return {
      success: false,
      data: null,
      message:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to fetch prediction",
    };
  }
};