import API from "./api";

// ---------------------- GET RECOMMENDATIONS ---------------------- //
export const getRecommendations = async (riskLevel = "medium") => {
  try {
    const response = await API.post("/recommendations/", {
      risk_level: riskLevel,
    });

    const resData = response.data;

    return {
      success: true,
      data: resData?.data || resData || [],
      message: resData?.message || "Recommendations fetched successfully",
    };
  } catch (error) {
    console.error("Recommendation fetch failed:", error);

    return {
      success: false,
      data: [],
      message:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to fetch recommendations",
    };
  }
};