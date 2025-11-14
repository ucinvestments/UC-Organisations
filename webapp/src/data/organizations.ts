/**
 * UC Investments Organization Data
 * Based on UC Office of the Chief Investment Officer structure
 */

import { Organization } from '@/src/components/OrganizationNode';

export const ucInvestmentsOrg: Organization = {
  id: 'cio',
  name: 'Chief Investment Officer, Senior Vice President – Investments',
  type: 'office',
  description: 'Office of the Chief Investment Officer',
  children: [
    {
      id: 'investment-management',
      name: 'Investment Management',
      type: 'department',
      description: 'Manages UC investment portfolios',
      children: [
        {
          id: 'public-equity',
          name: 'Public Equity',
          type: 'team',
          description: 'Public equity investments and strategies',
        },
        {
          id: 'fixed-income',
          name: 'Fixed Income',
          type: 'team',
          description: 'Fixed income securities and bonds',
        },
        {
          id: 'alternative-investment',
          name: 'Alternative Investment',
          type: 'team',
          description: 'Alternative investment strategies including private equity and real assets',
        },
      ],
    },
    {
      id: 'sustainability',
      name: 'Sustainability',
      type: 'department',
      description: 'Sustainable and responsible investment practices',
    },
    {
      id: 'risk-management',
      name: 'Risk Management',
      type: 'department',
      description: 'Investment risk assessment and management',
    },
    {
      id: 'investment-services',
      name: 'Investment Services',
      type: 'department',
      description: 'Supporting services for investment operations',
      children: [
        {
          id: 'cash-liquidity',
          name: 'Cash and Liquidity Management',
          type: 'team',
          description: 'Managing cash positions and liquidity requirements',
        },
        {
          id: 'data-analytics',
          name: 'Data Mgmt. & Analytics',
          type: 'team',
          description: 'Investment data management and analytical support',
        },
        {
          id: 'client-relations',
          name: 'Client Relations',
          type: 'team',
          description: 'Managing relationships with UC clients and stakeholders',
        },
        {
          id: 'investment-transactions',
          name: 'Investment Transactions',
          type: 'team',
          description: 'Processing and settling investment transactions',
        },
        {
          id: 'investment-support',
          name: 'Investment Support',
          type: 'team',
          description: 'General investment operations support',
        },
      ],
    },
  ],
};

// Governance structure (for reference/future use)
export const governanceOrg: Organization = {
  id: 'regents',
  name: 'The Regents of the University of California',
  type: 'committee',
  description: 'UC System governing board',
  children: [
    {
      id: 'regents-investment-committee',
      name: 'UC Regents Committee on Investments',
      type: 'committee',
      description: 'Oversees UC investment policies',
      children: [
        {
          id: 'investment-advisory',
          name: 'UC Regents Investment Advisory Committee',
          type: 'committee',
          description: 'Provides investment advice and recommendations',
        },
      ],
    },
  ],
};

// Leadership structure
export const leadershipOrg: Organization = {
  id: 'president',
  name: 'President of the University of California',
  type: 'position',
  description: 'UC System President',
  children: [
    {
      id: 'cfo',
      name: 'Chief Financial Officer',
      type: 'position',
      description: 'UC System CFO',
    },
  ],
};

// Complete organizational structure
export const completeOrgStructure: Organization[] = [
  leadershipOrg,
  governanceOrg,
  ucInvestmentsOrg,
];
