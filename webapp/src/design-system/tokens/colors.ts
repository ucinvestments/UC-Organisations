/**
 * UC Investments Design System - Color Tokens
 * Based on UC Berkeley brand colors and extended palette
 */

export const colors = {
  // Primary brand colors
  primary: {
    berkeleyBlue: '#003262',
    californiaGold: '#FDB515',
    white: '#FFFFFF',
  },

  // Extended UC Berkeley palette
  palette: {
    foundersRock: '#3B7EA1',
    medalist: '#C4820E',
    lawrence: '#00B0DA',
    bayFog: '#DDD5C7',
    stonePine: '#584F29',
    southHall: '#6C3302',
    pacificFog: '#B9D3B6',
    satherGate: '#B13C26',
    ross: '#CFDD45',
    wellmanTile: '#D9661F',
    ion: '#CFDD45',
    goldenGate: '#ED4E33',
    westGate: '#00A598',
    metallicGold: '#BC9B6A',
    lap: '#EE1F60',
  },

  // System colors
  system: {
    black: '#000000',
    white: '#FFFFFF',
  },

  // Semantic colors
  text: {
    primary: '#1A1A1A',
    secondary: '#666666',
    tertiary: '#999999',
    inverse: '#FFFFFF',
  },

  // Background colors
  background: {
    primary: '#FFFFFF',
    secondary: '#F5F5F5',
    tertiary: '#EEEEEE',
    dark: '#1A1A1A',
    overlay: 'rgba(0, 0, 0, 0.5)',
  },

  // Border colors
  border: {
    light: '#E5E5E5',
    medium: '#CCCCCC',
    dark: '#999999',
  },

  // State colors
  state: {
    success: '#00A598',
    warning: '#FDB515',
    error: '#B13C26',
    info: '#3B7EA1',
  },
} as const;

export type ColorToken = typeof colors;
