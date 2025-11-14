/**
 * Organization Node Types
 */

export interface Organization {
  id: string;
  name: string;
  description?: string;
  type?: 'department' | 'team' | 'committee' | 'office' | 'position';
  children?: Organization[];
  metadata?: Record<string, unknown>;
}

export interface OrganizationNodeProps {
  organization: Organization;
  onInfoClick: (organization: Organization) => void;
  level?: number;
}
