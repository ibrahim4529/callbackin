/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  jit: true,
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
}

