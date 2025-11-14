/**
 * UC Investments Design System - Border Tokens
 */

export const borders = {
  // Border radius
  radius: {
    none: '0',
    sm: '0.25rem',   // 4px
    base: '0.375rem', // 6px
    md: '0.5rem',    // 8px
    lg: '0.75rem',   // 12px
    xl: '1rem',      // 16px
    '2xl': '1.5rem', // 24px
    full: '9999px',  // Fully rounded
  },

  // Border widths
  width: {
    none: '0',
    thin: '1px',
    base: '2px',
    thick: '4px',
  },
} as const;

export type BorderToken = typeof borders;
