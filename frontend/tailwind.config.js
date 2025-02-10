/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js"
  ],

  theme: {
    extend: {
      colors: {
        red: {
          300: "#fca5a5",
          400: "#f87171",
          500: "#ef4444",
          600: "#dc2626"
        },
        blue: {
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb"
        },
        lime: {
          300: "#bef264",
          400: "#a3e635",
          500: "#84cc16",
          600: "#65a30d"
        },
        yellow: {
          300: "#fde047",
          400: "#facc15",
          500: "#eab308",
          600: "#ca8a04"
        },
        purple: {
          300: "#d8b4fe",
          400: "#c084fc",
          500: "#a855f7",
          600: "#9333ea"
        }
      }
    }
  },

  plugins: [
    require('flowbite/plugin'),
  ],

  safelist: [
    "bg-blue-300", "bg-blue-400", "bg-blue-500", "bg-blue-600", "hover:bg-blue-400", "hover:bg-blue-500", "text-blue-500", "hover:text-blue-500",
    "bg-red-300", "bg-red-400", "bg-red-500", "bg-red-600", "hover:bg-red-400", "hover:bg-red-500", "text-red-500", "hover:text-red-500",
    "bg-lime-300", "bg-lime-400", "bg-lime-500", "bg-lime-600", "hover:bg-lime-400", "hover:bg-lime-500", "text-lime-500", "hover:text-lime-500",
    "bg-yellow-300", "bg-yellow-400", "bg-yellow-500", "bg-yellow-600", "hover:bg-yellow-400", "hover:bg-yellow-500", "text-yellow-500", "hover:text-yellow-500",
    "bg-purple-300", "bg-purple-400", "bg-purple-500", "bg-purple-600", "hover:bg-purple-400", "hover:bg-purple-500", "text-purple-500", "hover:text-purple-500",
  ],
}