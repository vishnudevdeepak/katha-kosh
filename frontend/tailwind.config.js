/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#F7F4EE',
        primary: '#6B4F3A',
        secondary: '#8A6A4A',
        accent: '#B9825A',
        sage: '#7D8B68',
        ink: '#2F2B27',
        muted: '#746E67',
        card: '#FFFDF8',
        border: '#E3DDD3',
        cream: '#F0EBE1',
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
