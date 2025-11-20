/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef6ed',
          100: '#fce9d1',
          200: '#f9d0a2',
          300: '#f5b06a',
          400: '#f08a3f',
          500: '#e67e22', // Base orange
          600: '#d46a15',
          700: '#b05413',
          800: '#8d4416',
          900: '#723a15',
        },
        secondary: {
          50: '#f4f7f4',
          100: '#e6ede6',
          200: '#cddccd',
          300: '#a9c3a9',
          400: '#8bae66', // Light green accent
          500: '#628141', // Mid green
          600: '#4e6734',
          700: '#3f522b',
          800: '#354325',
          900: '#2d3820',
        },
        accent: {
          50: '#fdf8f3',
          100: '#fbefd9',
          200: '#f7ddb3',
          300: '#f2c782',
          400: '#ecab5d',
          500: '#e5bd5a', // Cream/beige
          600: '#d4a045',
          700: '#b1813a',
          800: '#8e6735',
          900: '#73542d',
        },
        earth: {
          orange: '#E67E22',
          darkgreen: '#628141',
          lightgreen: '#8BAE66',
          cream: '#EBD5AB',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        }
      }
    },
  },
  plugins: [],
}
