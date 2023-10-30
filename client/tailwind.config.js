/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      transitionProperty: {
        height: "height",
        'max-height': 'max-height',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
  corePlugins: {
    preflight: false
  }
}