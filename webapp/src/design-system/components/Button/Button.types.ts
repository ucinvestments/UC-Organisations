/**
 * Button Component Types
 * Simple, composable button interface
 */

import { ComponentPropsWithoutRef, ReactNode } from 'react';
import { LucideIcon } from 'lucide-react';

export type ButtonVariant = 'primary' | 'secondary' | 'accent' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ComponentPropsWithoutRef<'button'> {
  /** Visual variant */
  variant?: ButtonVariant;

  /** Size variant */
  size?: ButtonSize;

  /** Icon to display before content */
  leftIcon?: LucideIcon;

  /** Icon to display after content */
  rightIcon?: LucideIcon;

  /** Loading state */
  loading?: boolean;

  /** Full width */
  fullWidth?: boolean;

  /** Button content */
  children: ReactNode;
}
