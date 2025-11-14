/**
 * Button Component
 * Unix philosophy: Simple, composable, focused on one task
 */

import React from 'react';
import { ButtonProps } from './Button.types';

// Simple variant styles - composable via className
const variantStyles = {
  primary: 'bg-berkeley-blue text-white hover:opacity-90',
  secondary: 'bg-white text-berkeley-blue border-2 border-berkeley-blue hover:bg-berkeley-blue hover:text-white',
  accent: 'bg-california-gold text-berkeley-blue hover:opacity-90',
  ghost: 'bg-transparent text-berkeley-blue hover:bg-berkeley-blue/10',
} as const;

// Simple size styles - composable via className
const sizeStyles = {
  sm: 'text-sm px-3 py-1.5',
  md: 'text-base px-4 py-2',
  lg: 'text-lg px-6 py-3',
} as const;

// Icon size mapping
const iconSizes = {
  sm: 16,
  md: 20,
  lg: 24,
} as const;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      leftIcon: LeftIcon,
      rightIcon: RightIcon,
      loading = false,
      fullWidth = false,
      disabled,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Compose classes - Unix: build from simple parts
    const classes = [
      // Base styles
      'inline-flex items-center justify-center gap-2',
      'rounded-xl font-medium',
      'transition-all duration-200',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'focus:outline-none focus:ring-2 focus:ring-berkeley-blue focus:ring-offset-2',

      // Variant and size
      variantStyles[variant],
      sizeStyles[size],

      // Width
      fullWidth ? 'w-full' : '',

      // Hover effects
      !disabled && !loading ? 'hover:shadow-md hover:scale-[1.02]' : '',

      // Custom classes
      className,
    ]
      .filter(Boolean)
      .join(' ');

    const iconSize = iconSizes[size];
    const isDisabled = disabled || loading;

    return (
      <button ref={ref} disabled={isDisabled} className={classes} {...props}>
        {/* Left icon - simple composition */}
        {LeftIcon && !loading && <LeftIcon size={iconSize} />}

        {/* Loading spinner - simple, minimal */}
        {loading && (
          <svg
            className="animate-spin"
            width={iconSize}
            height={iconSize}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}

        {/* Content */}
        {children}

        {/* Right icon - simple composition */}
        {RightIcon && !loading && <RightIcon size={iconSize} />}
      </button>
    );
  }
);

Button.displayName = 'Button';
