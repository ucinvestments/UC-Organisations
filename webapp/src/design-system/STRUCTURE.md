# Design System Structure

## Directory Layout

```
src/design-system/
│
├── tokens/                          # Design Tokens (TypeScript)
│   ├── colors.ts                    # Berkeley colors + extended palette
│   ├── typography.ts                # Font families, sizes, weights
│   ├── spacing.ts                   # Spacing scale (xs to 3xl)
│   ├── shadows.ts                   # Shadow utilities
│   ├── borders.ts                   # Border radius & widths
│   └── index.ts                     # Exports all tokens
│
├── styles/                          # Global Styles
│   └── globals.css                  # Tailwind v4 config + UC tokens
│
├── components/                      # UI Components
│   ├── Button/
│   │   ├── Button.tsx              # Button component
│   │   ├── Button.types.ts         # TypeScript types
│   │   └── index.ts                # Module export
│   │
│   ├── SearchBar/
│   │   ├── SearchBar.tsx           # SearchBar component
│   │   ├── SearchBar.types.ts      # TypeScript types
│   │   └── index.ts                # Module export
│   │
│   └── index.ts                     # Exports all components
│
├── icons/                           # Icon Library
│   └── index.ts                     # Re-exports from lucide-react
│
├── index.ts                         # Main design system export
├── README.md                        # Full documentation
└── STRUCTURE.md                     # This file
```

## Import Patterns

### Tokens
```tsx
import { colors, typography, spacing } from '@/src/design-system/tokens';
```

### Components
```tsx
import { Button, SearchBar } from '@/src/design-system';
```

### Icons
```tsx
import { Search, Menu, User } from '@/src/design-system/icons';
```

### Everything
```tsx
import { Button, colors, Search } from '@/src/design-system';
```

## File Sizes (Approximate)

- **Tokens**: ~5KB total (minimal runtime overhead)
- **Button**: ~2KB (gzipped)
- **SearchBar**: ~2KB (gzipped)
- **Icons**: Tree-shakeable (only imports used icons)

## Unix Philosophy Applied

1. **Modularity**: Each token file exports a single concern
2. **Composability**: Components accept className for extension
3. **Simplicity**: Clear, minimal APIs with sensible defaults
4. **Single Responsibility**: Each component does one thing well
5. **Text as Interface**: Design tokens are plain TypeScript objects

## Adding New Components

1. Create directory: `src/design-system/components/NewComponent/`
2. Create files:
   - `NewComponent.tsx` - Component implementation
   - `NewComponent.types.ts` - TypeScript interfaces
   - `index.ts` - Module export
3. Export from `src/design-system/components/index.ts`
4. Document in `README.md`

## Color System

**Primary Brand:**
- Berkeley Blue (#003262) - Primary actions, headers
- California Gold (#FDB515) - Accent, CTAs

**Extended Palette:**
15+ UC Berkeley colors for various use cases

**Semantic:**
- Success: West Gate (#00A598)
- Warning: California Gold (#FDB515)
- Error: Sather Gate (#B13C26)
- Info: Founders Rock (#3B7EA1)

## Typography System

**Font:** Inter (primary), with system font fallbacks

**Sizes:**
- xs (12px) → 4xl (36px)
- 8 size steps

**Weights:**
- Light (300) → Bold (700)
- 5 weight options

## Spacing System

Consistent scale from 4px to 64px:
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

## Component Conventions

1. **Props**: Extend native HTML element props when possible
2. **Refs**: Forward refs for direct DOM access
3. **Types**: Export all types alongside components
4. **Variants**: Use string unions for type safety
5. **Defaults**: Provide sensible defaults for all optional props
6. **Composition**: Accept children and className

## Testing Your Changes

```bash
# Development
npm run dev

# Type checking
npx tsc --noEmit

# Build
npm run build
```

## Demo Page

View all components at: `http://localhost:3000/` (after running `npm run dev`)
