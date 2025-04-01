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
          100: "#fee2e2",
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
        },
        green: {
          100: "#dcfce7" // Добавлен зеленый 100
        }
      }
    }
  },

  plugins: [
    require('flowbite/plugin'),
  ],

  safelist: [
    "bg-red-100", "bg-red-300", "bg-red-400", "bg-red-500", "bg-red-600", 
    "hover:bg-red-400", "hover:bg-red-500", "text-red-500", "hover:text-red-500", 
    "border-red-600", "text-red-600","hover:bg-red-200",
    
    "bg-gray-400",
    
    "bg-blue-300", "bg-blue-400", "bg-blue-500", "bg-blue-600", 
    "hover:bg-blue-400", "hover:bg-blue-500", "text-blue-500", 
    "hover:text-blue-500", "border-blue-600", "text-blue-600", "hover:bg-blue-200",
    
    "bg-lime-300", "bg-lime-400", "bg-lime-500", "bg-lime-600", 
    "hover:bg-lime-400", "hover:bg-lime-500", "text-lime-500", 
    "hover:text-lime-500", "border-lime-600", "text-lime-600", "hover:bg-lime-200",
    
    "bg-yellow-300", "bg-yellow-400", "bg-yellow-500", "bg-yellow-600", 
    "hover:bg-yellow-400", "hover:bg-yellow-500", "text-yellow-500", 
    "hover:text-yellow-500", "border-yellow-600", "text-yellow-600", "hover:bg-yellow-200",
    
    "bg-purple-300", "bg-purple-400", "bg-purple-500", "bg-purple-600", 
    "hover:bg-purple-400", "hover:bg-purple-500", "text-purple-500", 
    "hover:text-purple-500", "border-purple-600", "text-purple-600", "hover:bg-purple-200",

    "bg-green-100",
      "bg-red-200", "hover:bg-red-400",
    "bg-orange-200", "hover:bg-orange-400",
    "bg-amber-200", "hover:bg-amber-400",
    "bg-lime-200", "hover:bg-lime-400",
    "bg-green-200", "hover:bg-green-400",
    "bg-emerald-200", "hover:bg-emerald-400",
    "bg-teal-200", "hover:bg-teal-400",
    "bg-sky-200", "hover:bg-sky-400",
    "bg-blue-200", "hover:bg-blue-400",
    "bg-indigo-200", "hover:bg-indigo-400",
    "bg-violet-200", "hover:bg-violet-400",
    "bg-purple-200", "hover:bg-purple-400",
    "bg-fuchsia-200", "hover:bg-fuchsia-400",
    "bg-pink-200", "hover:bg-pink-400",
    "bg-rose-200", "hover:bg-rose-400",

    "bg-cyan-200",     "hover:bg-cyan-400",
    "bg-slate-200",    "hover:bg-slate-400",
    "bg-stone-200",    "hover:bg-stone-400",
  
    
    ],
}
