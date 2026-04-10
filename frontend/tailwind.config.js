/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b7ff5',
        'primary-dark': '#2563eb',
        secondary: '#00d9ff',
        success: '#10d98f',
        danger: '#ff4757',
        warning: '#f5a623',

        'dark-bg': '#0a0e17',
        'dark-surface': '#0f131c',
        'dark-card': '#131823',
        'dark-card-hover': '#16192a',

        'text-primary': '#f5f7fa',
        'text-secondary': '#d4d8e0',
        'text-muted': '#7a8195',

        'border-color': '#1f2639',
      },
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        display: ['Syne', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #3b7ff5, #00d9ff)',
        'gradient-danger': 'linear-gradient(135deg, #ff4757, #ff6b81)',
      },
      boxShadow: {
        card: '0 4px 6px rgba(0, 0, 0, 0.1)',
        'card-hover': '0 12px 24px rgba(0, 0, 0, 0.15)',
      },
    },
  },
  plugins: [],
};