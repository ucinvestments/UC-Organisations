'use client';

import Link from 'next/link';
import { Button } from '@/src/design-system';
import { ArrowLeft, Building2, Palette, Plus } from '@/src/design-system/icons';
import { EditEntitiesPanel } from '@/src/components/EditEntitiesPanel';

export default function EditPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-bay-fog/40 to-pacific-fog/30">
      <header className="bg-white border-b-2 border-berkeley-blue shadow-md">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-3">
              <Building2 className="text-berkeley-blue" size={40} />
              <div>
                <p className="text-sm uppercase tracking-wide text-berkeley-blue/60">
                  UC Investments
                </p>
                <h1 className="text-3xl font-bold text-berkeley-blue">Edit Records</h1>
                <p className="text-gray-600 mt-1">
                  Provide record IDs plus the exact fields to modify, then push the updates via the API.
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link href="/">
                <Button variant="secondary" leftIcon={ArrowLeft}>
                  View Org Chart
                </Button>
              </Link>
              <Link href="/create">
                <Button variant="accent" leftIcon={Plus}>
                  Add Records
                </Button>
              </Link>
              <Link href="/design-system">
                <Button variant="ghost" leftIcon={Palette}>
                  Design System
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <EditEntitiesPanel />
      </main>
    </div>
  );
}
