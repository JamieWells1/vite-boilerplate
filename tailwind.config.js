const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/layouts/**/*.{js,ts,jsx,tsx}",
    "./src/pages/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        //forge-insert:fonts
        sans: ["Roboto", ...defaultTheme.fontFamily.sans],
      },
      //forge-insert:colors
      colors: {
  primary: {
    DEFAULT: "#123456",
    light: "#1f5a95",
    dark: "#040d16",
  },
  secondary: {
    DEFAULT: "#abcdef",
    light: "#ebf3fb",
    dark: "#6aa6e2",
  },
},
    },
  },
  plugins: [
    require("tailwindcss-animate"), // Add ShadCN animations
  ],
};
