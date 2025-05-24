// tailwind.config.js
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        primary: {
          DEFAULT: "#4f46e5", // Indigo 600
          dark: "#4338ca",
          light: "#6366f1",
        },
        secondary: {
          DEFAULT: "#ec4899", // Pink 500
          dark: "#db2777",
          light: "#f472b6",
        },
        muted: "#6b7280", // gray-500
      },
    },
  },
};
