import API from "./api";

// ---------------------- START SESSION ---------------------- //
export const startChatbotSession = async () => {
  try {
    const response = await API.post("/chatbot/start");
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: "Failed to start chatbot" };
  }
};

// ---------------------- PROCESS STEP ---------------------- //
export const processChatbotStep = async (sessionId, step, userResponse) => {
  try {
    const payload = {
      step,
      response: userResponse, // renamed for clarity (avoids confusion with API response)
    };

    const res = await API.post(`/chatbot/step/${sessionId}`, payload);
    return res.data;
  } catch (error) {
    throw error.response?.data || { detail: "Failed to process chatbot step" };
  }
};

// ---------------------- GET STATUS ---------------------- //
export const getChatbotStatus = async (sessionId) => {
  try {
    const response = await API.get(`/chatbot/status/${sessionId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: "Failed to get chatbot status" };
  }
};

// ---------------------- OPTIONAL: RESET SESSION ---------------------- //
// (useful for restarting flow without creating new session on frontend)
export const resetChatbotSession = async (sessionId) => {
  try {
    const response = await API.post(`/chatbot/reset/${sessionId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: "Failed to reset chatbot session" };
  }
};