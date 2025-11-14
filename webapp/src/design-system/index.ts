/**
 * UC Investments Design System
 * Unix philosophy: Modular exports, compose at will
 *
 * Each module is independent and can be imported separately:
 * - import { Button } from '@/design-system';
 * - import { colors } from '@/design-system/tokens';
 * - import { Search } from '@/design-system/icons';
 */

// Design Tokens
export * from './tokens';

// Components
export * from './components';

// Icons (re-export for convenience)
export * as Icons from './icons';
