export default function Loader({ text = "Analyzing market data...", size = "md" }) {
  const sizeClasses = {
    sm: "w-8 h-8 border-2",
    md: "w-12 h-12 border-4",
    lg: "w-16 h-16 border-4",
  };

  return (
    <div className="relative flex flex-col items-center justify-center h-64 gap-5">

      {/* Animated Glow Background */}
      <div className="absolute w-32 h-32 bg-blue-500/20 blur-3xl rounded-full animate-pulse"></div>

      {/* Spinner System */}
      <div className="relative flex items-center justify-center">

        {/* Outer rotating ring */}
        <div
          className={`${sizeClasses[size]} border-blue-500/30 border-t-blue-500 rounded-full animate-spin`}
        ></div>

        {/* Inner rotating ring */}
        <div
          className={`absolute ${sizeClasses[size]} border-green-400/30 border-b-green-400 rounded-full animate-spin-slow`}
        ></div>

        {/* Center pulse dot */}
        <div className="absolute w-2 h-2 bg-green-400 rounded-full animate-ping"></div>
      </div>

      {/* Text */}
      <div className="flex flex-col items-center">
        <p className="text-gray-300 text-sm font-medium tracking-wide">
          {text}
        </p>
        <span className="text-xs text-gray-500 mt-1 animate-pulse">
          AI processing live market signals...
        </span>
      </div>
    </div>
  );
}