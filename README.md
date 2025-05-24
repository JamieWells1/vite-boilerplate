# Vite + React + TailwindCSS + ShadCN Starter Template

Welcome to the **Vite + React + TailwindCSS + ShadCN Starter Template**! This project is designed to provide a minimal, no-frills starting point for building modern web applications. With **TailwindCSS** and **ShadCN** pre-installed, you can hit the ground running with a fully customizable design system.

---

## Features

- **Barebones Setup**: Stripped down to the essentials—no unnecessary dependencies or boilerplate code.
- **Vite**: Lightning-fast development with hot module replacement (HMR).
- **React**: The latest version of React for building dynamic user interfaces.
- **TailwindCSS**: Utility-first CSS framework pre-configured and ready to use.
- **ShadCN**: Pre-installed components and animations for a modern UI.
- **Custom CLI (`forge`)**: A powerful CLI tool to quickly customize environment variables and Tailwind configurations.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vite-react-tailwind-shadcn-starter.git
cd vite-react-tailwind-shadcn-starter
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start the Development Server

```bash
npm run dev
```

Your app will be available at [http://localhost:5173](http://localhost:5173).

---

## Project Structure

```
vite-react-tailwind-shadcn-starter/
├── forge/ # CLI and configuration utilities
├── src/ # Application source code
│ ├── components/ # UI components
│ ├── lib/ # Utility functions
│ ├── App.tsx # Main application component
│ ├── main.tsx # Entry point
│ └── index.css # TailwindCSS styles
├── tailwind.config.js # TailwindCSS configuration
├── vite.config.ts # Vite configuration
├── package.json # Project metadata and scripts
└── README.md # Project documentation
```

---

## CLI: `forge`

The **`forge` CLI** is a custom tool designed to streamline the customization of your project. It allows you to quickly configure environment variables, fonts, and TailwindCSS settings.

### Commands

#### 1. `forge start`

Launches an interactive interface to customize your project.

```bash
forge start
```

- **Font Configuration**: Choose a font and decide whether to use Google Fonts.
- **Color Configuration**: Define primary and secondary colors in hexadecimal format.
- **Environment Variables**: Set up your domain, API base URL, and API integrations.

#### 2. `forge build`

Syncs your configurations with the project files (e.g., `tailwind.config.js`, `.env`, `index.css`).

```bash
forge build
```

#### 3. `forge list`

Lists all current configurations. If no configurations exist, it prompts you to run `forge start`.

```bash
forge list
```

---

### Using `forge` to Customize Your Project

#### Example: Setting Up Fonts

When you run `forge start`, you'll be prompted to configure fonts:

```bash
Use Google fonts? (y/N): y
-> Font name: Inter
```

This will:

- Add the Google Fonts import to `src/index.css`.
- Update the `tailwind.config.js` file to include the selected font.

#### Example: Setting Up Colors

You'll also be prompted to configure colors:

```bash
Primary colour (hex): #4f46e5
Secondary colour (hex): #ec4899
```

This will:

- Generate light and dark variations for the colors.
- Update the `tailwind.config.js` file with the new color palette.

#### Example: Setting Up Environment Variables

Finally, you'll configure environment variables:

```bash
Domain: https://example.com
Use https://api.example.com as API base URL? (Y/n): y
Add API integration? (y/N): y
Environment variable name: API_KEY
Value for 'API_KEY': 123456
```

This will:

- Write the variables to a `.env` file.
- Update the `forge.config.json` file for future reference.

---

## Scripts

The following scripts are available in `package.json`:

- **`npm run dev`**: Start the development server.
- **`npm run build`**: Build the project for production.
- **`npm run lint`**: Run ESLint to check for code quality issues.
- **`npm run test`**: Run unit tests with Vitest.

---

## Configuration

### TailwindCSS

The `tailwind.config.js` file is pre-configured with placeholders for fonts and colors:

```js
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: ["<font>", ...defaultTheme.fontFamily.sans],
      },
      colors: "<colors>",
    },
  },
  plugins: [require("tailwindcss-animate")],
};
```

Run `forge build` to replace `<font>` and `<colors>` with your custom settings.

### Environment Variables

Environment variables are stored in a `.env` file. Use `forge` to manage these variables.

Example `.env` file:

```
ENV="DEV"
DOMAIN="https://example.com"
API_BASE_URL="https://api.example.com"
API_KEY="123456"
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
