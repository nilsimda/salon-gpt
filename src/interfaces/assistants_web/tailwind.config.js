const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['src/**/*.{js,jsx,ts,tsx}'],
  plugins: [require('@tailwindcss/typography')],
  darkMode: 'class',
  safelist: [
    {
      pattern:
        /(bg|text|border|fill)-(blue|evolved-blue|coral|green|evolved-green|quartz|evolved-quartz|mushroom|evolved-mushroom|marble|volcanic|danger)-\S+/,
      variants: ['hover', 'dark', 'dark:hover'],
    },
  ],
  theme: {
    extend: {
      colors: {
        black: '#212121',
        white: '#FAFAFA',
        // Simulated Coral
        coral: {
          950: '#f2fda6',
          900: '#edfd82',
          800: '#e8fc5e',
          700: '#e2fb3a',
          600: '#ddfb16',
          500: '#C0DC04',
          400: '#c5e104',
          300: '#99af03',
          200: '#6d7d02',
          150: '#424b01',

          //950: '#FFEAE5',
          //900: '#FFD5CC',
          //800: '#FFAC99',
          //700: '#FF8266',
          //600: '#FF5833',
          //500: '#FF2F00',
          //400: '#CC2500',
          //300: '#991C00',
          //200: '#661300',
          //150: '#330900',
        },
        // Mushroom Grey
        mushroom: {
          950: '#F4F3F0',
          900: '#E9E7E2',
          800: '#D2CDC4',
          700: '#BDB6A8',
          600: '#A79E8B',
          500: '#91856E',
          400: '#70695C',
          300: '#575042',
          200: '#3A352C',
          150: '#2C2821',
        },
        // Evolved Mushroom Grey
        'evolved-mushroom': {
          500: '#FFAA00',
          600: '#FFBB33',
          800: '#FFDC97',
        },
        // Marble White
        marble: {
          1000: '#FFFFFF',
          980: '#F9F9FB',
          950: '#EFEFF5',
          900: '#DFDFEC',
          850: '#D0D0E2',
          800: '#C4C4C4',
        },
        // Volcanic Black
        volcanic: {
          950: '#F2F2F2',
          900: '#E6E6E6',
          800: '#CBCBCB',
          700: '#B3B3B3',
          600: '#999999',
          500: '#808080',
          400: '#666666',
          300: '#4D4D4D',
          200: '#333333',
          150: '#262626',
          100: '#1A1A1A',
          60: '#0F0F0F',
        },
        // Coniferous Green
        green: {
          950: '#f2fda6',
          900: '#edfd82',
          800: '#e8fc5e',
          700: '#e2fb3a',
          600: '#ddfb16',
          500: '#C0DC04',
          400: '#c5e104',
          300: '#99af03',
          200: '#6d7d02',
          150: '#424b01',
          //950: '#F0F5F3',
          //900: '#E0EBE7',
          //800: '#C0D6CD',
          //700: '#A2C3B6',
          //600: '#84AE9D',
          //500: '#659A84',
          //400: '#517B6A',
          //250: '#324D42',
          //200: '#283E35',
          //150: '#141F1B',
        },
        // Evolved Coniferous Green
        'evolved-green': {
          500: '#adc604',
          700: '#adc604',
          900: '#adc604',
          //500: '#0DF293',
          //700: '#6EF7BE',
          //900: '#CFFCE9',
        },
        // Synthetic Quartz
        quartz: {
          950: '#F7EBFA',
          900: '#EFD6F5',
          800: '#DDACEA',
          700: '#CE85E0',
          600: '#BD5DD5',
          500: '#AD34CB',
          400: '#8A2AA2',
          300: '#681F7A',
          200: '#451551',
          150: '#34103D',
        },
        // Evolved synthetic quartz
        'evolved-quartz': {
          500: '#C40DF2',
          700: '#DC6EF7',
          900: '#F3CFFC',
        },
        // Acrylic Blue
        blue: {
          950: '#adc604',
          900: '#adc604',
          800: '#adc604',
          700: '#adc604',
          600: '#adc604',
          500: '#adc604',
          400: '#adc604',
          300: '#adc604',
          200: '#adc604',
          150: '#adc604',
        },
        // Evolved Acrylic Blue
        'evolved-blue': {
          //500: '#0039FF',
          500: '#adc604',
        },
        // Safety Green
        success: {
          950: '#E7FEE9',
          300: '#089113',
          200: '#05610C',
          150: '#044909',
        },
        // Safety Red
        danger: {
          950: '#FFE5E5',
          500: '#FF0000',
          350: '#B30000',
        },
      },
      fontSize: {
        // rem values calculated with a base font of 16px
        caption: ['0.75rem', { letterSpacing: '-0.01em', lineHeight: '136%' }], // 12px - Caption
        'label-sm': ['0.625rem', { letterSpacing: '0.04em', lineHeight: '136%' }], // 10px - Small Label
        label: ['0.75rem', { letterSpacing: '0.04em', lineHeight: '136%' }], // 12px - Label
        overline: ['0.875rem', { letterSpacing: '0.04em', lineHeight: '136%' }], // 14px - Overline
        'p-xs': ['0.625rem', { letterSpacing: '0.0025em', lineHeight: '150%' }], // 10px - XSmall Paragraph
        'p-sm': ['0.75rem', { letterSpacing: '-0.01em', lineHeight: '150%' }], // 12px - Small Paragraph
        p: ['0.875rem', { letterSpacing: '0.0025em', lineHeight: '150%' }], // 14px - Paragraph
        'p-lg': ['1rem', { letterSpacing: '0em', lineHeight: '150%' }], // 16px - Large Paragraph
        code: ['1rem', { letterSpacing: '0.03em', lineHeight: '136%' }], // 16px - Code
        'code-sm': ['0.75rem', { letterSpacing: '0.03em', lineHeight: '136%' }], // 12px - Small Code
        // Headings
        logo: ['1.5rem', { letterSpacing: '0em', lineHeight: '100%' }], // 24px - Logo Application
        'h5-m': ['1.125rem', { letterSpacing: '0em', lineHeight: '136%' }], // 18px - Mobile Heading 5
        h5: ['1.3125rem', { letterSpacing: '0em', lineHeight: '136%' }], // 21px - Desktop Heading 5
        'h4-m': ['1.3125rem', { letterSpacing: '0em', lineHeight: '136%' }], // 21px - Mobile Heading 4
        h4: ['1.75rem', { letterSpacing: '0em', lineHeight: '136%' }], // 28px - Desktop Heading 4
        'h3-m': ['1.75rem', { letterSpacing: '0em', lineHeight: '136%' }], // 28px - Mobile Heading 3
        h3: ['2.375rem', { letterSpacing: '0em', lineHeight: '120%' }], // 38px - Desktop Heading 3
        'h2-m': ['2.375rem', { letterSpacing: '0em', lineHeight: '120%' }], // 38px - Mobile Heading 2
        h2: ['3.1875rem', { letterSpacing: '0em', lineHeight: '116%' }], // 51px - Desktop Heading 2
        'h1-m': ['3.1875rem', { letterSpacing: '0em', lineHeight: '116%' }], // 51px - Mobile Heading 1
        h1: ['4.1875rem', { letterSpacing: '0em', lineHeight: '116%' }], // 67px - Desktop Heading 1
      },
      fontFamily: {
        body: ['CohereText', 'Arial', ...defaultTheme.fontFamily.sans],
        variable: ['CohereVariable', 'Arial', ...defaultTheme.fontFamily.serif],
        code: ['CohereMono', ...defaultTheme.fontFamily.mono],
      },
      fontWeight: {
        // Bolded fonts will always use Cohere Variable with the weight 525
        medium: '525',
      },
      minWidth: {
        menu: '174px',
        'left-panel-collapsed': '82px',
        'left-panel-expanded': '288px',
      },
      width: {
        'icon-xs': '12px',
        'icon-sm': '14px',
        'icon-md': '16px',
        'icon-lg': '24px',
        'icon-xl': '36px',
        modal: '648px',
        toast: '320px',
        'toast-sm': '280px',
      },
      maxWidth: {
        message: '976px',
        'left-panel-collapsed': '82px',
        'left-panel-expanded': '288px',
        'share-content': '700px',
      },
      height: {
        'cell-button': '40px',
        'icon-xs': '12px',
        'icon-sm': '14px',
        'icon-md': '16px',
        'icon-lg': '24px',
        'icon-xl': '36px',
        header: '64px',
      },
      minHeight: {
        'cell-xs': '24px',
        'cell-sm': '32px',
        'cell-md': '40px',
        'cell-lg': '50px',
        'cell-xl': '64px',
      },
      maxHeight: {
        modal: 'calc(100vh - 120px)',
        'cell-xs': '24px',
        'cell-sm': '32px',
        'cell-md': '40px',
        'cell-lg': '50px',
        'cell-xl': '64px',
      },
      zIndex: {
        'tag-suggestions': '10',
        'drag-drop-input-overlay': '10',
        navigation: '30',
        'guide-tooltip': '30',
        tooltip: '50',
        dropdown: '60',
        'read-only-conversation-footer': '60',
        menu: '90',
        backdrop: '150',
        modal: '200',
      },
      boxShadow: {
        menu: '0px 4px 12px 0px rgba(197, 188, 172, 0.48)', // secondary-400
        top: '4px 0px 12px 0px rgba(197, 188, 172, 0.48)', // secondary-400
      },
      typography: (theme) => ({
        quoteless: {
          css: {
            'blockquote p:first-of-type::before': { content: 'none' },
            'blockquote p:first-of-type::after': { content: 'none' },
          },
        },
        DEFAULT: {
          css: {
            color: theme('colors.volcanic.300'),
          },
        },
      }),
      keyframes: {
        typing: {
          '0%': {
            width: '0%',
            visibility: 'hidden',
          },
          '100%': {
            width: '100%',
          },
        },
      },
      transitionProperty: {
        spacing: 'padding',
      },
      animation: {
        'typing-ellipsis': 'typing 2s steps(4) infinite',
      },
    },
  },
};
