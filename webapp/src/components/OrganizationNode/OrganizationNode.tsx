/**
 * Organization Node Component
 * Renders a centered org chart with connectors using react-d3-tree
 */

'use client';

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import type {
  RawNodeDatum,
  CustomNodeElementProps,
  TreeProps,
} from 'react-d3-tree';
import { Info, ChevronDown } from '@/src/design-system/icons';
import { OrganizationNodeProps, Organization } from './OrganizationNode.types';

// react-d3-tree relies on the browser; load lazily in Next
const Tree = dynamic<React.ComponentType<TreeProps>>(
  () => import('react-d3-tree').then((mod) => mod.default),
  { ssr: false },
);

const BASE_NODE_WIDTH = 230;
const BASE_NODE_HEIGHT = 140;
const LINE_HEIGHT = 18;
const VERTICAL_SPACING = 230;

const palette = [
  {
    border: '#ffb3b8',
    background: 'linear-gradient(135deg, #fff5f3 0%, #ffe4de 100%)',
    avatar: '#ff5f6d',
    shadow: 'rgba(255, 95, 109, 0.25)',
  },
  {
    border: '#b5c7ff',
    background: 'linear-gradient(135deg, #f3f6ff 0%, #e2e8ff 100%)',
    avatar: '#4d77ff',
    shadow: 'rgba(77, 119, 255, 0.25)',
  },
  {
    border: '#b7f4d1',
    background: 'linear-gradient(135deg, #f0fff6 0%, #d9ffe9 100%)',
    avatar: '#2bb673',
    shadow: 'rgba(43, 182, 115, 0.25)',
  },
  {
    border: '#ffe3a7',
    background: 'linear-gradient(135deg, #fff9e6 0%, #ffe9bf 100%)',
    avatar: '#f8b400',
    shadow: 'rgba(248, 180, 0, 0.28)',
  },
  {
    border: '#b3ecff',
    background: 'linear-gradient(135deg, #ecfcff 0%, #cfefff 100%)',
    avatar: '#00bcd4',
    shadow: 'rgba(0, 188, 212, 0.25)',
  },
] as const;

const getInitials = (name?: string) =>
  name
    ?.split(' ')
    .filter(Boolean)
    .map((word) => word[0]?.toUpperCase())
    .slice(0, 2)
    .join('') || '';

type ChartDatum = RawNodeDatum & {
  data: Organization;
};

const getNodeDimensions = (org: Organization) => {
  const widthByName = (org.name?.length || 0) * 8.5;
  const width = Math.max(BASE_NODE_WIDTH, widthByName + 60);
  const charsPerLine = Math.max(18, Math.floor(width / 8.5));
  const descriptionLines = org.description
    ? Math.ceil(org.description.length / charsPerLine)
    : 0;
  const extraLines = org.type ? 1 : 0;
  const verticalPadding = 50;
  const height =
    BASE_NODE_HEIGHT +
    (descriptionLines + extraLines) * LINE_HEIGHT +
    verticalPadding;
  return { width, height };
};

const buildTreeData = (
  node: Organization,
  collapsedMap: Record<string, boolean>,
): ChartDatum => ({
  name: node.name,
  attributes: {
    type: node.type,
    description: node.description,
  },
  data: node,
  children:
    collapsedMap[node.id] || !node.children
      ? undefined
      : node.children.map((child) => buildTreeData(child, collapsedMap)),
});

export const OrganizationNode: React.FC<OrganizationNodeProps> = ({
  organization,
  onInfoClick,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const updateDimensions = () => {
      if (!containerRef.current) return;
      const { width, height } = containerRef.current.getBoundingClientRect();
      setDimensions({
        width,
        height: Math.max(height, 600),
      });
    };

    updateDimensions();

    const observer =
      typeof ResizeObserver !== 'undefined'
        ? new ResizeObserver(() => updateDimensions())
        : null;
    if (observer && containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer?.disconnect();
  }, []);

  const toggleCollapsed = useCallback((id: string) => {
    setCollapsed((prev) => {
      const next = { ...prev };
      if (next[id]) {
        delete next[id];
      } else {
        next[id] = true;
      }
      return next;
    });
  }, []);

  const treeData = useMemo(
    () => [buildTreeData(organization, collapsed)],
    [organization, collapsed],
  );

  const renderCustomNode = useCallback(
    ({ nodeDatum }: CustomNodeElementProps<ChartDatum>) => {
      const org = nodeDatum.data;
      const hasChildren = (org.children?.length || 0) > 0;
      const depthIndex = (nodeDatum.depth || 0) % palette.length;
      const accent = palette[depthIndex];
      const isCollapsed = Boolean(collapsed[org.id]);
      const { width, height } = getNodeDimensions(org);

      return (
        <g>
          <foreignObject
            x={-width / 2}
            y={-height / 2}
            width={width}
            height={height}
          >
            <div
              className="org-tree-card"
              style={{
                borderColor: accent.border,
                background: accent.background,
                boxShadow: `0 25px 40px ${accent.shadow}`,
              }}
            >
              <div className="org-tree-card__header">
                <div
                  className="org-tree-avatar"
                  style={{ background: accent.avatar }}
                >
                  {getInitials(org.name)}
                </div>
                <div className="org-tree-card__text">
                  <p className="org-tree-card__title">{org.name}</p>
                  <p className="org-tree-card__meta">
                    {(org.type && org.type.charAt(0).toUpperCase() + org.type.slice(1)) ||
                      'Organization'}
                    {hasChildren
                      ? ` · ${org.children!.length} sub-organization${
                          org.children!.length !== 1 ? 's' : ''
                        }`
                      : ''}
                  </p>
                </div>
                <div className="org-tree-card__actions">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onInfoClick(org);
                    }}
                    className="org-tree-icon"
                    aria-label="View information"
                  >
                    <Info size={18} />
                  </button>
                  {hasChildren && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleCollapsed(org.id);
                      }}
                      className={`org-tree-icon org-tree-icon--toggle ${
                        isCollapsed ? 'is-collapsed' : ''
                      }`}
                      aria-label={
                        isCollapsed ? 'Expand sub-organizations' : 'Collapse sub-organizations'
                      }
                    >
                      <ChevronDown size={18} />
                    </button>
                  )}
                </div>
              </div>
              {org.description && (
                <p className="org-tree-card__description">{org.description}</p>
              )}
            </div>
          </foreignObject>
        </g>
      );
    },
    [collapsed, onInfoClick, toggleCollapsed],
  );

  return (
    <div
      ref={containerRef}
      className="org-tree-wrapper"
    >
      <Tree
        data={treeData}
        orientation="vertical"
        translate={{
          x: dimensions.width / 2,
          y: BASE_NODE_HEIGHT / 1.4,
        }}
        nodeSize={{ x: BASE_NODE_WIDTH + 200, y: VERTICAL_SPACING }}
        transitionDuration={400}
        separation={{ siblings: 1.5, nonSiblings: 1.8 }}
        renderCustomNodeElement={renderCustomNode}
        pathFunc="straight"
        allowForeignObjects
        collapsible={false}
      />
    </div>
  );
};

OrganizationNode.displayName = 'OrganizationNode';
