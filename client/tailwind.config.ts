import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        green: "#024f46",
        black: "#1a1a1a",
        offwhite: "#ffffeb",
      },
      fontFamily: {
        mono: ["var(--font-geist-mono)", "Courier New", "Courier", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
