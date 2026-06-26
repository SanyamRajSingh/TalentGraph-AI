import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        graphite: "#374151",
        signal: "#2563EB",
        mint: "#0F766E",
        amber: "#B45309"
      }
    }
  },
  plugins: []
};

export default config;
