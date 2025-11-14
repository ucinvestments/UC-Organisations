/**
 * Organization Node Component
 * Unix philosophy: Simple, composable organization display
 */

'use client';

import React, { useState } from 'react';
import { Info, ChevronDown, ChevronRight } from '@/src/design-system/icons';
import { OrganizationNodeProps } from './OrganizationNode.types';

// Color mapping based on organization type
const typeColors = {
  department: 'bg-california-gold/10 border-california-gold',
  team: 'bg-founders-rock/10 border-founders-rock',
  committee: 'bg-west-gate/10 border-west-gate',
  office: 'bg-berkeley-blue/10 border-berkeley-blue',
  position: 'bg-pacific-fog border-stone-pine',
} as const;

export const OrganizationNode: React.FC<OrganizationNodeProps> = ({
  organization,
  onInfoClick,
  level = 0,
}) => {
  const [isExpanded, setIsExpanded] = useState(level === 0);

  const hasChildren = organization.children && organization.children.length > 0;
  const colorClass = typeColors[organization.type || 'department'];

  return (
    <div className="space-y-3">
      {/* Organization Card */}
      <div
        className={`
          relative
          border-2 rounded-xl
          ${colorClass}
          p-4
          transition-all duration-200
          hover:shadow-md
          ${level > 0 ? 'ml-8' : ''}
        `}
      >
        <div className="flex items-center justify-between gap-4">
          {/* Organization Name */}
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-berkeley-blue">
              {organization.name}
            </h3>
            {organization.type && (
              <p className="text-sm text-gray-600 capitalize mt-1">
                {organization.type}
              </p>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            {/* Info Button */}
            <button
              onClick={() => onInfoClick(organization)}
              className="p-2 rounded-lg hover:bg-white/50 transition-colors text-berkeley-blue"
              aria-label="View information"
              title="View information"
            >
              <Info size={20} />
            </button>

            {/* Expand/Collapse Button */}
            {hasChildren && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="p-2 rounded-lg hover:bg-white/50 transition-colors text-berkeley-blue"
                aria-label={isExpanded ? 'Collapse' : 'Expand'}
                title={isExpanded ? 'Collapse sub-organizations' : 'Expand sub-organizations'}
              >
                {isExpanded ? (
                  <ChevronDown size={20} />
                ) : (
                  <ChevronRight size={20} />
                )}
              </button>
            )}
          </div>
        </div>

        {/* Children Count Badge */}
        {hasChildren && (
          <div className="absolute -bottom-2 left-4">
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-berkeley-blue text-white">
              {organization.children!.length} sub-organization{organization.children!.length !== 1 ? 's' : ''}
            </span>
          </div>
        )}
      </div>

      {/* Children */}
      {hasChildren && isExpanded && (
        <div className="space-y-3 border-l-2 border-gray-300 ml-4 pl-2">
          {organization.children!.map((child) => (
            <OrganizationNode
              key={child.id}
              organization={child}
              onInfoClick={onInfoClick}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

OrganizationNode.displayName = 'OrganizationNode';
