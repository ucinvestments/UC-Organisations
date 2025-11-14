/**
 * SearchBar Component
 * Unix philosophy: Simple input composition with search affordances
 */

import React from 'react';
import { Search, X } from 'lucide-react';
import { SearchBarProps } from './SearchBar.types';

// Simple size styles - composable
const sizeStyles = {
  sm: {
    container: 'h-9',
    input: 'text-sm pl-9 pr-9',
    icon: 14,
  },
  md: {
    container: 'h-11',
    input: 'text-base pl-11 pr-11',
    icon: 18,
  },
  lg: {
    container: 'h-14',
    input: 'text-lg pl-14 pr-14',
    icon: 22,
  },
} as const;

export const SearchBar = React.forwardRef<HTMLInputElement, SearchBarProps>(
  (
    {
      size = 'md',
      clearable = true,
      onClear,
      loading = false,
      className = '',
      containerClassName = '',
      value,
      ...props
    },
    ref
  ) => {
    const styles = sizeStyles[size];
    const hasValue = value !== undefined && value !== '';

    // Simple container composition
    const containerClasses = [
      'relative flex items-center',
      styles.container,
      containerClassName,
    ]
      .filter(Boolean)
      .join(' ');

    // Simple input composition
    const inputClasses = [
      // Base styles
      'w-full',
      'rounded-xl',
      'border-2 border-border-light',
      'bg-white',
      'transition-all duration-200',

      // Focus state
      'focus:outline-none focus:border-berkeley-blue focus:ring-2 focus:ring-berkeley-blue/20',

      // Hover state
      'hover:border-border-medium',

      // Size specific
      styles.input,

      // Custom classes
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div className={containerClasses}>
        {/* Search icon - left side */}
        <Search
          className="absolute left-3 text-gray-400 pointer-events-none"
          size={styles.icon}
        />

        {/* Input field */}
        <input
          ref={ref}
          type="search"
          value={value}
          className={inputClasses}
          {...props}
        />

        {/* Right side: Loading or Clear button */}
        <div className="absolute right-3">
          {loading ? (
            // Simple loading spinner
            <svg
              className="animate-spin text-gray-400"
              width={styles.icon}
              height={styles.icon}
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
          ) : clearable && hasValue ? (
            // Clear button - simple, composable
            <button
              type="button"
              onClick={onClear}
              className="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded-full hover:bg-gray-100"
              aria-label="Clear search"
            >
              <X size={styles.icon} />
            </button>
          ) : null}
        </div>
      </div>
    );
  }
);

SearchBar.displayName = 'SearchBar';
