# UC Investments Design System

A modular, composable UI component library built with Unix philosophy principles.

## Philosophy

- **Do one thing well**: Each component has a single, clear purpose
- **Composability**: Components work together seamlessly
- **Simplicity**: Minimal, focused APIs
- **Modularity**: Import only what you need

## Installation

Components are already available in this project. Import from `@/design-system`:

```tsx
import { Button, SearchBar } from '@/design-system';
import { colors } from '@/design-system/tokens';
import { Search } from '@/design-system/icons';
```

## Design Tokens

### Colors

```tsx
import { colors } from '@/design-system/tokens';

// Primary brand colors
colors.primary.berkeleyBlue  // #003262
colors.primary.californiaGold // #FDB515

// Extended palette
colors.palette.foundersRock   // #3B7EA1
colors.palette.lawrence       // #00B0DA
// ... 13 more colors

// Semantic colors
colors.text.primary           // #1A1A1A
colors.background.primary     // #FFFFFF
colors.state.success          // #00A598
```

### Typography

```tsx
import { typography } from '@/design-system/tokens';

typography.fontSize.base      // 1rem
typography.fontWeight.medium  // 500
typography.fontFamily.sans    // Inter, ...
```

### Spacing, Shadows, Borders

```tsx
import { spacing, shadows, borders } from '@/design-system/tokens';

spacing.md                    // 1rem
shadows.lg                    // Large shadow
borders.radius.xl             // 1rem
```

## Components

### Button

Simple, composable button with variants and states.

```tsx
import { Button } from '@/design-system';
import { Search } from '@/design-system/icons';

// Basic usage
<Button>Click me</Button>

// With variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="accent">Accent</Button>
<Button variant="ghost">Ghost</Button>

// With sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>

// With icons
<Button leftIcon={Search}>Search</Button>
<Button rightIcon={Search}>Search</Button>

// States
<Button loading>Loading...</Button>
<Button disabled>Disabled</Button>

// Full width
<Button fullWidth>Full Width</Button>
```

**Props:**
- `variant`: 'primary' | 'secondary' | 'accent' | 'ghost'
- `size`: 'sm' | 'md' | 'lg'
- `leftIcon`: LucideIcon
- `rightIcon`: LucideIcon
- `loading`: boolean
- `fullWidth`: boolean
- Plus all native button props

### SearchBar

Simple search input with clear button and loading state.

```tsx
import { SearchBar } from '@/design-system';
import { useState } from 'react';

function MyComponent() {
  const [search, setSearch] = useState('');

  return (
    <SearchBar
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      onClear={() => setSearch('')}
      placeholder="Search..."
    />
  );
}

// Sizes
<SearchBar size="sm" />
<SearchBar size="md" />
<SearchBar size="lg" />

// States
<SearchBar loading />
<SearchBar clearable={false} />
```

**Props:**
- `size`: 'sm' | 'md' | 'lg'
- `clearable`: boolean (default: true)
- `onClear`: () => void
- `loading`: boolean
- Plus all native input props (except size)

## Icons

Pre-exported commonly used icons from Lucide React:

```tsx
import { Search, Menu, User, Settings } from '@/design-system/icons';

// Use directly
<Search size={20} />

// In components
<Button leftIcon={Search}>Search</Button>
```

**Available Icons:**
- Navigation: Menu, X, ChevronLeft, ChevronRight, ArrowLeft, ArrowRight
- Actions: Search, Plus, Edit, Trash2, Save, Download, Upload
- UI: Eye, Info, AlertCircle, CheckCircle, XCircle
- Content: File, Image, Video, Link
- User: User, Users, Settings, LogOut, LogIn
- Data: Calendar, Clock, TrendingUp, BarChart

[See full list in `/src/design-system/icons/index.ts`]

## Usage Examples

### Simple Form

```tsx
import { Button, SearchBar } from '@/design-system';
import { Search } from '@/design-system/icons';
import { useState } from 'react';

export function SearchForm() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // ... search logic
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <SearchBar
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onClear={() => setQuery('')}
        placeholder="Search organisations..."
        loading={loading}
      />
      <Button
        type="submit"
        leftIcon={Search}
        loading={loading}
        fullWidth
      >
        Search
      </Button>
    </form>
  );
}
```

## Customization

All components accept `className` props for additional styling:

```tsx
<Button className="shadow-xl">Custom Button</Button>
<SearchBar containerClassName="max-w-md" />
```

## Design System Files

```
src/design-system/
├── tokens/              # Design tokens (colors, typography, etc.)
│   ├── colors.ts
│   ├── typography.ts
│   ├── spacing.ts
│   ├── shadows.ts
│   ├── borders.ts
│   └── index.ts
├── styles/              # Global styles
│   └── globals.css      # Tailwind config + UC design tokens
├── components/          # UI components
│   ├── Button/
│   ├── SearchBar/
│   └── index.ts
├── icons/               # Icon library
│   └── index.ts
└── index.ts             # Main export
```

## Contributing

When adding new components:

1. Follow Unix philosophy: simple, focused, composable
2. Use TypeScript for type safety
3. Export types alongside components
4. Keep dependencies minimal
5. Document props and usage
6. Use design tokens for consistency

## Color Palette Reference

| Color Name | Hex | Usage |
|------------|-----|-------|
| Berkeley Blue | #003262 | Primary brand, buttons, headers |
| California Gold | #FDB515 | Accent, highlights, CTAs |
| Founders Rock | #3B7EA1 | Secondary blue |
| Lawrence | #00B0DA | Bright blue accents |
| West Gate | #00A598 | Success states |
| Sather Gate | #B13C26 | Error states |

[See all 15+ colors in `/src/design-system/tokens/colors.ts`]
