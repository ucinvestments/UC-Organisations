/**
 * SearchBar Component Types
 * Simple, composable search interface
 */

import { ComponentPropsWithoutRef } from 'react';

export type SearchBarSize = 'sm' | 'md' | 'lg';

export interface SearchBarProps extends Omit<ComponentPropsWithoutRef<'input'>, 'size'> {
  /** Size variant */
  size?: SearchBarSize;

  /** Show clear button when value exists */
  clearable?: boolean;

  /** Callback when clear button is clicked */
  onClear?: () => void;

  /** Loading state */
  loading?: boolean;

  /** Container className */
  containerClassName?: string;
}
