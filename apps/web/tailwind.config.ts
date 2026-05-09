import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#00288e",
        "primary-container": "#1e40af",
        secondary: "#006c4a",
        tertiary: "#611e00",
        error: "#ba1a1a",
        surface: "#f8f9ff",
        "on-surface": "#0b1c30",
        "surface-container": "#ffffff",
      },
    },
  },
  plugins: [],
};

export default config;
