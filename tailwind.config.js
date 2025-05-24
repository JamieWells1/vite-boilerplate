const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/layouts/**/*.{js,ts,jsx,tsx}",
    "./src/pages/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // Enable dark mode (class-based or media-based)
  theme: {
    extend: {
      fontFamily: {
        sans: ["Roboto", ...defaultTheme.fontFamily.sans],
      },
      colors: "<colors>",
    },
  },
  plugins: [
    require("tailwindcss-animate"), // Add ShadCN animations
  ],
};
