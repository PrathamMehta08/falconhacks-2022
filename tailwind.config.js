/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.{html,js}", "./templates/**/*.html"],
  theme: {
    extend: {
      backgroundColor: ['even'],
    },
    fontFamily: {
      "sans": ["Work Sans", "ui-sans-serif"]
    }
  },
  plugins: [],
}