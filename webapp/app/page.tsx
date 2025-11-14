'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Modal, Button, SearchBar } from '@/src/design-system';
import { Building2, Palette } from '@/src/design-system/icons';
import { OrganizationNode, Organization } from '@/src/components/OrganizationNode';
import { ucInvestmentsOrg, leadershipOrg, governanceOrg } from '@/src/data/organizations';

export default function Home() {
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

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

        {/* Organization Charts */}
        <div className="space-y-12">
          {/* Leadership Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="h-1 w-12 bg-berkeley-blue rounded-full" />
              <h2 className="text-2xl font-semibold text-berkeley-blue">
                Leadership
              </h2>
            </div>
            <OrganizationNode
              organization={leadershipOrg}
              onInfoClick={handleInfoClick}
            />
          </section>

          {/* Governance Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="h-1 w-12 bg-west-gate rounded-full" />
              <h2 className="text-2xl font-semibold text-berkeley-blue">
                Governance
              </h2>
            </div>
            <OrganizationNode
              organization={governanceOrg}
              onInfoClick={handleInfoClick}
            />
          </section>

          {/* Investment Office Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="h-1 w-12 bg-california-gold rounded-full" />
              <h2 className="text-2xl font-semibold text-berkeley-blue">
                Office of the Chief Investment Officer
              </h2>
            </div>
            <OrganizationNode
              organization={ucInvestmentsOrg}
              onInfoClick={handleInfoClick}
            />
          </section>
        </div>

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
