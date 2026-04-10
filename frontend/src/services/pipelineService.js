import API from "./api";

// ---------------------- RUN DATA PIPELINE ---------------------- //
export const refreshData = async () => {
  try {
    const response = await API.post("/pipeline/run");

    const resData = response.data;

    // Standardized return structure
    return {
      success: true,
      data: resData?.data || resData,
      message: resData?.message || "Pipeline executed successfully",
    };
  } catch (error) {
    console.error("Pipeline execution failed:", error);

    return {
      success: false,
      data: null,
      message:
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to refresh data pipeline",
    };
  }
};