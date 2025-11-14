# UC Organizations Web Application

Interactive organizational chart for the University of California Investment Office.

## Quick Start

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Visit `http://localhost:3000`

## Features

- **Interactive Org Chart**: Expandable/collapsible organization hierarchy
- **Information Modals**: Detailed view of each organization
- **Search**: Find organizations quickly
- **Responsive**: Works on all devices
- **UC Branding**: Official Berkeley colors and typography

## Project Structure

```
webapp/
├── app/
│   ├── page.tsx              # Main org chart
│   ├── layout.tsx            # Root layout
│   └── design-system/        # Component showcase
├── src/
│   ├── components/           # React components
│   │   └── OrganizationNode/ # Org chart node
│   ├── data/                 # Organization data
│   │   └── organizations.ts  # UC org structure
│   └── design-system/        # UI library
│       ├── components/       # Button, Modal, SearchBar
│       ├── tokens/           # Design tokens
│       ├── styles/           # Global CSS
│       └── icons/            # Icon library
└── public/                   # Static assets
```

## Pages

- `/` - Interactive organization chart
- `/design-system` - Component showcase and documentation

## Documentation

- [ORG_CHART.md](../ORG_CHART.md) - Org chart feature docs
- [DESIGN_SYSTEM.md](../DESIGN_SYSTEM.md) - Design system overview
- [src/design-system/README.md](src/design-system/README.md) - Component API docs
- [src/design-system/STRUCTURE.md](src/design-system/STRUCTURE.md) - Architecture

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Icons**: Lucide React

## Development

### Adding Organizations

Edit `src/data/organizations.ts`:

```typescript
export const myOrg: Organization = {
  id: 'my-org',
  name: 'My Organization',
  type: 'department',
  description: 'Description here',
  children: [
    // Sub-organizations
  ],
};
```

### Creating Components

```typescript
// src/components/MyComponent/MyComponent.tsx
export const MyComponent: React.FC<Props> = ({ ... }) => {
  return <div>...</div>;
};

// src/components/MyComponent/index.ts
export { MyComponent } from './MyComponent';
export type { Props } from './MyComponent.types';
```

## Design System

Import components from the design system:

```tsx
import { Button, Modal, SearchBar } from '@/src/design-system';
import { Search, Info } from '@/src/design-system/icons';

<Button variant="primary" leftIcon={Search}>
  Search
</Button>
```

See full docs at `/design-system` route.

## Customization

### Colors

Edit `src/design-system/tokens/colors.ts`

### Typography

Edit `src/design-system/tokens/typography.ts`

### Global Styles

Edit `src/design-system/styles/globals.css`

## Building

```bash
# Development build
npm run dev

# Production build
npm run build

# Type check
npx tsc --noEmit

# Lint
npm run lint
```

## Deployment

Built for deployment on Vercel, Netlify, or any Node.js hosting.

```bash
npm run build
npm start
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Create production build
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment

- Node.js 18+ required
- npm or yarn package manager

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

UC Investments internal project.
