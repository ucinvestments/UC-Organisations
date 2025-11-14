# UC Investments Design System - Quick Start

## Overview

A modular, tokenized UI component library built following Unix philosophy principles. Based on UC Berkeley brand guidelines and the UC-wages design system.

## What's Included

✅ **Design Tokens** - Colors, typography, spacing, shadows, borders
✅ **Icon Library** - 40+ pre-configured Lucide icons
✅ **Button Component** - 4 variants, 3 sizes, loading states, icon support
✅ **SearchBar Component** - Clearable, loading states, 3 sizes
✅ **Tailwind CSS v4** - Configured with UC Berkeley colors
✅ **TypeScript** - Full type safety
✅ **Documentation** - Complete usage examples

## Quick Start

### 1. View the Demo

```bash
cd webapp
npm run dev
```

Visit `http://localhost:3000` to see all components in action.

### 2. Use Components

```tsx
import { Button, SearchBar } from '@/src/design-system';
import { Search } from '@/src/design-system/icons';

export function MyComponent() {
  return (
    <>
      <Button variant="primary" leftIcon={Search}>
        Search
      </Button>
      <SearchBar placeholder="Search..." />
    </>
  );
}
```

### 3. Use Design Tokens

```tsx
import { colors, typography, spacing } from '@/src/design-system/tokens';

const myStyles = {
  color: colors.primary.berkeleyBlue,
  fontSize: typography.fontSize.lg,
  padding: spacing.md,
};
```

## File Structure

```
webapp/src/design-system/
├── tokens/          # Design tokens (colors, typography, etc.)
├── styles/          # Global CSS with Tailwind config
├── components/      # UI components (Button, SearchBar)
├── icons/           # Icon library (Lucide icons)
├── index.ts         # Main export
├── README.md        # Full documentation
└── STRUCTURE.md     # Architecture details
```

## Key Features

### Unix Philosophy

- **Modular**: Import only what you need
- **Composable**: Components work together seamlessly
- **Simple**: Clear, minimal APIs
- **Focused**: Each component does one thing well

### Design System

- **Berkeley Blue & California Gold** as primary colors
- **15+ extended palette colors** from UC Berkeley brand
- **Inter font family** for typography
- **Consistent spacing, shadows, and borders**
- **Glass morphism & gradient utilities**

## Available Components

### Button

4 variants: `primary`, `secondary`, `accent`, `ghost`
3 sizes: `sm`, `md`, `lg`
States: `loading`, `disabled`
Features: Icon support (left/right), full width option

```tsx
<Button variant="primary" size="md" leftIcon={Search} loading>
  Search
</Button>
```

### SearchBar

3 sizes: `sm`, `md`, `lg`
States: `loading`
Features: Auto-clear button, custom callbacks

```tsx
<SearchBar
  value={query}
  onChange={(e) => setQuery(e.target.value)}
  onClear={() => setQuery('')}
  loading={isSearching}
/>
```

## Color Palette

| Color | Hex | Tailwind Class |
|-------|-----|----------------|
| Berkeley Blue | #003262 | `bg-berkeley-blue` |
| California Gold | #FDB515 | `bg-california-gold` |
| Founders Rock | #3B7EA1 | `bg-founders-rock` |
| Lawrence | #00B0DA | `bg-lawrence` |
| West Gate | #00A598 | `bg-west-gate` |

[See all 15+ colors in the demo page]

## Documentation

- **Full Docs**: `webapp/src/design-system/README.md`
- **Structure**: `webapp/src/design-system/STRUCTURE.md`
- **Demo**: Run `npm run dev` and visit localhost:3000

## Adding Components

1. Create component directory in `src/design-system/components/`
2. Follow the pattern: `Component.tsx`, `Component.types.ts`, `index.ts`
3. Export from `components/index.ts`
4. Document in README

## Next Steps

1. ✅ Design system initialized
2. ⏭️ Add more components as needed (Card, Modal, Input, etc.)
3. ⏭️ Expand icon library with project-specific icons
4. ⏭️ Add component variants based on feedback

## Dependencies

- **React 19** - UI framework
- **Next.js 16** - Framework
- **Tailwind CSS v4** - Styling
- **Lucide React** - Icons
- **TypeScript** - Type safety

## Build & Test

```bash
# Development
npm run dev

# Production build
npm run build

# Type checking
npx tsc --noEmit

# Linting
npm run lint
```

## Philosophy

> "Make each component simple and composable. Let developers build complex UIs from simple, well-designed pieces."

This design system follows:
- Single responsibility principle
- Composition over inheritance
- Explicit over implicit
- Simple over complex

---

Built with Unix philosophy for UC Investments
