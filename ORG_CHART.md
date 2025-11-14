# UC Organizations - Interactive Org Chart

## Overview

An interactive organizational chart application for visualizing the University of California Investment Office structure. Built with Next.js, React, and a custom design system following Unix philosophy.

## Features

### Interactive Organization Nodes
- **Expandable/Collapsible**: Click chevron icons to show/hide sub-organizations
- **Information Modal**: Click info icons to view detailed organization information
- **Color-Coded Types**: Visual distinction between departments, teams, committees, offices, and positions
- **Badge Indicators**: Shows count of sub-organizations

### Organization Types
- **Office**: Main organizational offices (blue)
- **Department**: Major departments (gold)
- **Team**: Operational teams (founders rock blue)
- **Committee**: Governance committees (west gate green)
- **Position**: Individual leadership positions (pacific fog)

### User Interface
- **Search Bar**: Find organizations quickly (ready for implementation)
- **Responsive Design**: Works on desktop and mobile
- **UC Berkeley Branding**: Official colors and typography
- **Smooth Animations**: Expand/collapse transitions

## Structure

### UC Investments Organization

```
Chief Investment Officer
├── Investment Management
│   ├── Public Equity
│   ├── Fixed Income
│   └── Alternative Investment
├── Sustainability
├── Risk Management
└── Investment Services
    ├── Cash and Liquidity Management
    ├── Data Mgmt. & Analytics
    ├── Client Relations
    ├── Investment Transactions
    └── Investment Support
```

### Governance Structure

```
The Regents of the University of California
└── UC Regents Committee on Investments
    └── UC Regents Investment Advisory Committee
```

### Leadership Structure

```
President of the University of California
└── Chief Financial Officer
```

## Usage

### Running the Application

```bash
cd webapp
npm run dev
```

Visit `http://localhost:3000` to see the org chart.

### Adding New Organizations

Edit `webapp/src/data/organizations.ts`:

```typescript
const newOrg: Organization = {
  id: 'unique-id',
  name: 'Organization Name',
  type: 'department', // or 'team', 'committee', 'office', 'position'
  description: 'Description of the organization',
  children: [
    // Sub-organizations...
  ],
};
```

### Organization Data Structure

```typescript
interface Organization {
  id: string;                    // Unique identifier
  name: string;                  // Display name
  description?: string;          // Optional description
  type?: 'department' | 'team' | 'committee' | 'office' | 'position';
  children?: Organization[];     // Sub-organizations
  metadata?: Record<string, unknown>; // Additional data
}
```

## Components

### OrganizationNode

**Location**: `src/components/OrganizationNode/`

**Props**:
- `organization`: Organization data
- `onInfoClick`: Callback when info button is clicked
- `level`: Nesting level (auto-calculated)

**Features**:
- Recursive rendering of organization hierarchy
- Color-coded by organization type
- Expandable/collapsible with state management
- Badge showing sub-organization count

### Modal

**Location**: `src/design-system/components/Modal/`

**Props**:
- `open`: Boolean to control visibility
- `onClose`: Callback when modal should close
- `title`: Modal header title
- `size`: 'sm' | 'md' | 'lg' | 'xl' | 'full'
- `children`: Modal content
- `footer`: Optional footer content
- `showClose`: Show close button (default: true)
- `preventBackdropClose`: Prevent closing on backdrop click

**Features**:
- Escape key to close
- Backdrop click to close (optional)
- Body scroll lock when open
- Smooth animations
- Responsive sizing

## Pages

### Main Page (`/`)
- Interactive organization chart
- Search functionality (UI ready)
- Three sections: Leadership, Governance, Investment Office
- Info modal for organization details
- How-to-use instructions

### Design System Showcase (`/design-system`)
- Component examples
- Color palette
- Button variants
- SearchBar demos
- Typography samples

## Customization

### Colors

Edit `src/design-system/tokens/colors.ts` to modify the color palette.

Current organization type colors:
- **Department**: California Gold (#FDB515)
- **Team**: Founders Rock (#3B7EA1)
- **Committee**: West Gate (#00A598)
- **Office**: Berkeley Blue (#003262)
- **Position**: Pacific Fog/Stone Pine

### Styling

All components accept `className` for custom styling:

```tsx
<OrganizationNode
  organization={org}
  onInfoClick={handleClick}
  className="custom-styles"
/>
```

## Future Enhancements

### Search Implementation
The search bar is in place. To implement:

```typescript
const filteredOrgs = filterOrganizations(allOrgs, searchQuery);
```

### Data Integration
Connect to backend API:

```typescript
// src/data/organizations.ts
export async function fetchOrganizations() {
  const response = await fetch('/api/organizations');
  return response.json();
}
```

### Export/Print
Add export to PDF or image:

```typescript
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
```

### Drag & Drop
Allow reorganization:

```typescript
import { DndContext } from '@dnd-kit/core';
```

### Permissions
Add role-based access:

```typescript
interface Organization {
  // ...
  permissions?: {
    view: string[];
    edit: string[];
  };
}
```

## File Structure

```
webapp/
├── app/
│   ├── page.tsx                    # Main org chart page
│   └── design-system/
│       └── page.tsx                # Design system showcase
├── src/
│   ├── components/
│   │   └── OrganizationNode/       # Org chart node component
│   ├── data/
│   │   └── organizations.ts        # Organization data
│   └── design-system/              # UI component library
└── public/                         # Static assets
```

## Design Philosophy

Following Unix principles:
- **Modular**: Each component has a single responsibility
- **Composable**: Components work together seamlessly
- **Simple**: Clear, focused APIs
- **Data-Driven**: Organization structure defined as data

## Development

### Adding a Component

1. Create component directory in `src/components/`
2. Create files: `Component.tsx`, `Component.types.ts`, `index.ts`
3. Follow existing patterns
4. Export from index

### Styling Guidelines

- Use Tailwind classes for consistency
- Use design tokens for colors
- Follow UC Berkeley brand guidelines
- Ensure responsive design

### TypeScript

- Define types for all props
- Use strict type checking
- Export types alongside components

## Testing

```bash
# Type checking
npx tsc --noEmit

# Build
npm run build

# Development
npm run dev
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Accessibility

- Keyboard navigation (Escape to close modal)
- ARIA labels on buttons
- Semantic HTML structure
- Focus management

## Performance

- Static rendering where possible
- Lazy loading for large org charts (future)
- Optimized re-renders with React

## License

UC Investments internal project.

---

**Built with Unix philosophy for the University of California**
