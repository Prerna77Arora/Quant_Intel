import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { startChatbotSession, processChatbotStep } from "../services/chatbotService";
import { useAuth } from "../hooks/useAuth";
import { FiSend, FiArrowRight, FiCheck } from "react-icons/fi";

export default function ChatProfile() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [response, setResponse] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (user) initializeChat();
  }, [user]);

  const initializeChat = async () => {
    try {
      setLoading(true);

      const result = await startChatbotSession();

      if (result.completed) {
        setCompleted(true);
        setSession(result.data);
      } else {
        setSession(result.data);
      }

      setError("");
    } catch (err) {
      setError("Failed to start chatbot session");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!response.trim()) return;

    try {
      setSubmitting(true);
      setError("");

      const result = await processChatbotStep(
        session.session_id,
        session.current_step,
        response
      );

      if (result.success) {
        setResponse("");

        if (result.completed) {
          setCompleted(true);
        } else if (result.next_question) {
          setSession((prev) => ({
            ...prev,
            current_step: result.current_step,
            question: result.next_question.question,
            options: result.next_question.options
          }));
        }
      } else {
        setError(result.message || "Failed to process response");
      }
    } catch (err) {
      setError("Error processing your response");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  /* ---------------- LOADING ---------------- */
  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <div className="loader-ai mb-4"></div>
          <p className="text-text-primary">Initializing AI Advisor...</p>
        </div>
      </div>
    );
  }

  /* ---------------- ERROR STATE ---------------- */
  if (!session) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <p className="text-danger mb-4">Failed to load chat session</p>
          <button onClick={initializeChat} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg flex flex-col items-center justify-center px-4 py-8">

      <div className="w-full max-w-2xl">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            AI Investment Profiling
          </h1>
          <p className="text-text-muted">
            Personalized onboarding powered by AI
            {session.total_steps && ` (${session.current_step + 1}/${session.total_steps})`}
          </p>
        </div>

        {/* Chat Box */}
        <div className="bg-dark-card border border-border-color rounded-2xl p-6 shadow-lg">

          {/* Chat Area */}
          <div className="min-h-96 max-h-96 overflow-y-auto mb-6 space-y-4">

            {/* Bot Message */}
            <div className="flex justify-start">
              <div className="max-w-xs bg-dark-surface border border-border-color rounded-lg px-4 py-3 text-text-primary">
                {session.question}
              </div>
            </div>

            {/* Options */}
            {session.options && (
              <div className="flex flex-col gap-2 mt-4">
                <p className="text-xs text-text-muted uppercase">Options</p>

                {session.options.map((option, idx) => (
                  <button
                    key={idx}
                    onClick={() => setResponse(option)}
                    className={`text-left px-4 py-3 rounded-lg border transition-all ${
                      response === option
                        ? "bg-primary border-primary text-white"
                        : "bg-dark-card border-border-color text-text-primary hover:border-primary"
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Error */}
          {error && (
            <div className="mb-4 p-3 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg text-danger text-sm">
              {error}
            </div>
          )}

          {/* Input */}
          {!completed ? (
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                placeholder="Type or select your answer..."
                className="flex-1 form-input"
                disabled={submitting}
              />

              <button
                type="submit"
                disabled={submitting || !response.trim()}
                className="btn btn-primary px-6 flex items-center gap-2"
              >
                {submitting ? "..." : <FiSend size={18} />}
              </button>
            </form>
          ) : (
            <div className="text-center py-8">

              <div className="success-glow mb-4">
                <FiCheck size={32} />
              </div>

              <p className="text-text-primary font-semibold mb-2">
                Profile Completed
              </p>

              <p className="text-text-muted mb-6">
                AI has built your investment profile. You’ll now receive smarter recommendations.
              </p>

              <button
                onClick={() => navigate("/")}
                className="btn btn-primary flex items-center justify-center gap-2 mx-auto"
              >
                Go to Dashboard
                <FiArrowRight />
              </button>
            </div>
          )}
        </div>

        {/* Progress */}
        {!completed && session.total_steps && (
          <div className="mt-6">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-text-muted">Progress</span>
              <span className="text-text-primary font-semibold">
                {Math.round((session.current_step / session.total_steps) * 100)}%
              </span>
            </div>

            <div className="w-full bg-dark-surface rounded-full h-2">
              <div
                className="bg-gradient-primary h-2 rounded-full transition-all"
                style={{
                  width: `${(session.current_step / session.total_steps) * 100}%`
                }}
              />
            </div>
          </div>
        )}

      </div>
    </div>
  );
}