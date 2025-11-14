'use client';

import { useState } from 'react';
import { Button, SearchBar } from '@/src/design-system';
import { Search, Download, Settings, TrendingUp, Plus } from '@/src/design-system/icons';

export default function Home() {
  const [searchValue, setSearchValue] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-bay-fog p-8">
      <div className="max-w-6xl mx-auto space-y-12">
        {/* Header */}
        <header className="text-center space-y-4">
          <h1 className="text-5xl font-bold text-berkeley-blue">
            UC Investments Design System
          </h1>
          <p className="text-xl text-gray-600">
            Modular, composable components built with Unix philosophy
          </p>
        </header>

        {/* Button Showcase */}
        <section className="space-y-6 bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-semibold text-berkeley-blue">Buttons</h2>

          {/* Variants */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Variants</h3>
            <div className="flex flex-wrap gap-4">
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="accent">Accent</Button>
              <Button variant="ghost">Ghost</Button>
            </div>
          </div>

          {/* Sizes */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Sizes</h3>
            <div className="flex flex-wrap items-center gap-4">
              <Button size="sm">Small</Button>
              <Button size="md">Medium</Button>
              <Button size="lg">Large</Button>
            </div>
          </div>

          {/* With Icons */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">With Icons</h3>
            <div className="flex flex-wrap gap-4">
              <Button leftIcon={Search}>Search</Button>
              <Button variant="secondary" leftIcon={Download}>
                Download
              </Button>
              <Button variant="accent" rightIcon={TrendingUp}>
                Analytics
              </Button>
              <Button variant="ghost" leftIcon={Settings}>
                Settings
              </Button>
            </div>
          </div>

          {/* States */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">States</h3>
            <div className="flex flex-wrap gap-4">
              <Button loading>Loading...</Button>
              <Button disabled>Disabled</Button>
              <Button variant="secondary" loading>
                Processing
              </Button>
            </div>
          </div>

          {/* Full Width */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Full Width</h3>
            <Button fullWidth leftIcon={Plus}>
              Create New Organisation
            </Button>
          </div>
        </section>

        {/* SearchBar Showcase */}
        <section className="space-y-6 bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-semibold text-berkeley-blue">Search Bar</h2>

          {/* Sizes */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Sizes</h3>
            <div className="space-y-3">
              <SearchBar size="sm" placeholder="Small search bar..." />
              <SearchBar size="md" placeholder="Medium search bar..." />
              <SearchBar size="lg" placeholder="Large search bar..." />
            </div>
          </div>

          {/* Interactive Example */}
          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Interactive Example</h3>
            <div className="space-y-3">
              <SearchBar
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onClear={() => setSearchValue('')}
                placeholder="Search organisations..."
                loading={loading}
              />
              <Button
                onClick={handleSearch}
                leftIcon={Search}
                loading={loading}
                fullWidth
              >
                Search
              </Button>
            </div>
          </div>
        </section>

        {/* Color Palette */}
        <section className="space-y-6 bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-semibold text-berkeley-blue">Color Palette</h2>

          <div className="space-y-4">
            <h3 className="text-xl font-medium text-gray-700">Primary Colors</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <div className="h-20 rounded-lg bg-berkeley-blue shadow-md" />
                <p className="text-sm font-medium">Berkeley Blue</p>
                <p className="text-xs text-gray-500">#003262</p>
              </div>
              <div className="space-y-2">
                <div className="h-20 rounded-lg bg-california-gold shadow-md" />
                <p className="text-sm font-medium">California Gold</p>
                <p className="text-xs text-gray-500">#FDB515</p>
              </div>
              <div className="space-y-2">
                <div className="h-20 rounded-lg bg-founders-rock shadow-md" />
                <p className="text-sm font-medium">Founders Rock</p>
                <p className="text-xs text-gray-500">#3B7EA1</p>
              </div>
              <div className="space-y-2">
                <div className="h-20 rounded-lg bg-west-gate shadow-md" />
                <p className="text-sm font-medium">West Gate</p>
                <p className="text-xs text-gray-500">#00A598</p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="text-center text-gray-600 py-8">
          <p>Built with Unix philosophy: Simple, Modular, Composable</p>
          <p className="text-sm mt-2">
            See <code className="bg-gray-100 px-2 py-1 rounded">src/design-system/README.md</code> for full documentation
          </p>
        </footer>
      </div>
    </div>
  );
}
