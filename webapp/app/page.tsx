'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { Modal, Button, SearchBar } from '@/src/design-system';
import { Building2, Palette } from '@/src/design-system/icons';
import { OrganizationNode, Organization } from '@/src/components/OrganizationNode';
import {
  ucInvestmentsOrg,
  leadershipOrg,
  governanceOrg,
} from '@/src/data/organizations';

const cloneOrg = (org: Organization): Organization => ({
  ...org,
  children: org.children?.map(cloneOrg),
});

const buildChartRoot = (): Organization => ({
  id: 'uc-org-root',
  name: 'UC Organisations',
  type: 'office',
  description: 'University of California Investment Office structure',
  children: [leadershipOrg, governanceOrg, ucInvestmentsOrg].map(cloneOrg),
});

const filterTree = (node: Organization, query: string): Organization | null => {
  const normalized = query.toLowerCase();
  const matches =
    node.name.toLowerCase().includes(normalized) ||
    node.type?.toLowerCase().includes(normalized) ||
    node.description?.toLowerCase().includes(normalized);

  const filteredChildren = node.children
    ?.map((child) => filterTree(child, query))
    .filter((child): child is Organization => Boolean(child));

  if (matches || (filteredChildren && filteredChildren.length > 0)) {
    return {
      ...node,
      children: filteredChildren,
    };
  }

  return null;
};

const countNodes = (node: Organization | null | undefined): number => {
  if (!node) return 0;
  const childCount = node.children?.reduce(
    (sum, child) => sum + countNodes(child),
    0,
  );
  return 1 + (childCount || 0);
};

export default function Home() {
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const baseChart = useMemo(() => buildChartRoot(), []);

  const filteredChart = useMemo(() => {
    if (!searchQuery.trim()) {
      return baseChart;
    }

    const pruned = filterTree(baseChart, searchQuery.trim());
    return pruned || { ...baseChart, children: [] };
  }, [baseChart, searchQuery]);

  const handleInfoClick = (org: Organization) => {
    setSelectedOrg(org);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    // Clear selection after modal closes
    setTimeout(() => setSelectedOrg(null), 200);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-bay-fog/30 to-pacific-fog/20">
      {/* Header */}
      <header className="bg-white border-b-2 border-berkeley-blue shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Building2 className="text-berkeley-blue" size={40} />
              <div>
                <h1 className="text-3xl font-bold text-berkeley-blue">
                  UC Organisations
                </h1>
                <p className="text-gray-600 mt-1">
                  University of California Investment Office Structure
                </p>
              </div>
            </div>
            <Link href="/design-system">
              <Button variant="ghost" leftIcon={Palette}>
                Design System
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onClear={() => setSearchQuery('')}
            placeholder="Search organizations..."
            size="lg"
          />
        </div>

        {/* Chart Canvas */}
        <section className="mt-10">
          <div className="flex flex-wrap items-center gap-6 mb-4">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-california-gold">
                Dynamic Org Chart
              </p>
              <h2 className="text-3xl font-semibold text-berkeley-blue">
                UC Organisations Hierarchy
              </h2>
              <p className="text-gray-600">
                Expand nodes to explore reporting lines and committees.
              </p>
            </div>
            <div className="ml-auto flex gap-4">
              <div className="bg-white/80 border border-berkeley-blue/10 rounded-2xl px-5 py-3 text-center min-w-[140px] shadow-sm">
                <p className="text-xs uppercase tracking-widest text-berkeley-blue/70">
                  Total Nodes
                </p>
                <p className="text-2xl font-semibold text-berkeley-blue">
                  {countNodes(filteredChart)}
                </p>
              </div>
              <div className="bg-white/80 border border-california-gold/20 rounded-2xl px-5 py-3 text-center min-w-[140px] shadow-sm">
                <p className="text-xs uppercase tracking-widest text-california-gold/80">
                  Root Children
                </p>
                <p className="text-2xl font-semibold text-berkeley-blue">
                  {filteredChart.children?.length ?? 0}
                </p>
              </div>
            </div>
          </div>

          <OrganizationNode
            organization={filteredChart}
            onInfoClick={handleInfoClick}
          />

          {searchQuery && filteredChart.children?.length === 0 && (
            <p className="text-center text-sm text-gray-500 mt-6">
              No matches found. Try another search term.
            </p>
          )}
        </section>

        {/* Info Box */}
        <div className="mt-12 bg-white border-2 border-berkeley-blue/20 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-berkeley-blue mb-2">
            How to Use
          </h3>
          <ul className="space-y-2 text-gray-700">
            <li className="flex items-start gap-2">
              <span className="text-berkeley-blue font-bold">•</span>
              <span>Click the <strong>info icon (ℹ)</strong> to view organization details</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-berkeley-blue font-bold">•</span>
              <span>Click the <strong>chevron icon (›)</strong> to expand/collapse sub-organizations</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-berkeley-blue font-bold">•</span>
              <span>Use the <strong>search bar</strong> to find specific organizations</span>
            </li>
          </ul>
        </div>
      </main>

      {/* Info Modal */}
      <Modal
        open={isModalOpen}
        onClose={closeModal}
        title={selectedOrg?.name}
        size="lg"
      >
        {selectedOrg && (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-1">
                Type
              </h3>
              <p className="text-lg text-berkeley-blue capitalize">
                {selectedOrg.type || 'Organization'}
              </p>
            </div>

            {selectedOrg.description && (
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-1">
                  Description
                </h3>
                <p className="text-gray-700">
                  {selectedOrg.description}
                </p>
              </div>
            )}

            {selectedOrg.children && selectedOrg.children.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Sub-Organizations ({selectedOrg.children.length})
                </h3>
                <ul className="space-y-2">
                  {selectedOrg.children.map((child) => (
                    <li
                      key={child.id}
                      className="flex items-center gap-2 text-gray-700 bg-gray-50 rounded-lg px-3 py-2"
                    >
                      <span className="w-2 h-2 rounded-full bg-california-gold" />
                      <span>{child.name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500 italic">
                Additional organization details and information will be displayed here.
              </p>
            </div>
          </div>
        )}
      </Modal>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600">
            UC Investments Organization Chart • Built with Unix philosophy
          </p>
        </div>
      </footer>
    </div>
  );
}
