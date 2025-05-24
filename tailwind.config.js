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
        sans: ["<font>", ...defaultTheme.fontFamily.sans],
      },
      //forge-insert:colours
      colors: "<colors>",
    },
  },
  plugins: [
    require("tailwindcss-animate"), // Add ShadCN animations
  ],
};
