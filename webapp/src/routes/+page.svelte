<script lang="ts">
  import Icon from "@iconify/svelte";
  import Hero from "$lib/components/Hero.svelte";
  import Container from "$lib/components/Container.svelte";
  import SearchInput from "$lib/components/SearchInput.svelte";
  import Card from "$lib/components/Card.svelte";
  import OrgChart from "$lib/components/OrgChart.svelte";
  import {
    ucInvestmentsOrg,
    leadershipOrg,
    governanceOrg,
  } from "$lib/data/organizations";
  import type { Organization } from "$lib/types";

  const rootNode: Organization = {
    id: "uc-org-root",
    name: "UC Organisations",
    type: "office",
    description: "University of California Investment Office structure",
    children: [leadershipOrg, governanceOrg, ucInvestmentsOrg],
  };

  let searchQuery = $state("");
  let selectedOrg = $state<Organization | null>(null);
  let modalOpen = $state(false);

  function filterTree(node: Organization, query: string): Organization | null {
    const normalized = query.toLowerCase();
    const matches =
      node.name.toLowerCase().includes(normalized) ||
      node.type?.toLowerCase().includes(normalized) ||
      node.description?.toLowerCase().includes(normalized);

    const filteredChildren = node.children
      ?.map((child) => filterTree(child, query))
      .filter((child): child is Organization => Boolean(child));

    if (matches || (filteredChildren && filteredChildren.length > 0)) {
      return { ...node, children: filteredChildren };
    }
    return null;
  }

  function countNodes(node: Organization | null | undefined): number {
    if (!node) return 0;
    const childCount =
      node.children?.reduce((sum, child) => sum + countNodes(child), 0) ?? 0;
    return 1 + childCount;
  }

  const filtered = $derived(
    searchQuery.trim()
      ? filterTree(rootNode, searchQuery.trim()) ?? { ...rootNode, children: [] }
      : rootNode,
  );
  const totalNodes = $derived(countNodes(filtered));
  const rootChildren = $derived(filtered.children?.length ?? 0);

  function openInfo(org: Organization) {
    selectedOrg = org;
    modalOpen = true;
  }

  function closeModal() {
    modalOpen = false;
    setTimeout(() => (selectedOrg = null), 200);
  }
</script>

<Hero
  title="UC Organisations Hierarchy"
  subtitle="Explore the Office of the Chief Investment Officer — committees, departments, and reporting lines."
/>

<Container>
  <div class="search-row">
    <SearchInput
      bind:value={searchQuery}
      placeholder="Search organizations, types, descriptions…"
    />
  </div>

  <div class="stats-row">
    <div class="stat-box">
      <p class="stat-label">Total Nodes</p>
      <p class="stat-value">{totalNodes}</p>
    </div>
    <div class="stat-box gold">
      <p class="stat-label">Root Children</p>
      <p class="stat-value">{rootChildren}</p>
    </div>
  </div>

  <div class="chart-scroll">
    {#key searchQuery}
      <OrgChart node={filtered} onInfoClick={openInfo} />
    {/key}
  </div>

  {#if searchQuery && filtered.children?.length === 0}
    <p class="no-match">No matches found. Try another search term.</p>
  {/if}

  <Card hover={false} padding="1.5rem" delay={200}>
    <h3 class="how-title">
      <Icon icon="mdi:lightbulb-on" class="how-icon" /> How to Use
    </h3>
    <ul class="how-list">
      <li>
        <Icon icon="mdi:circle-small" /> Click the
        <strong>info icon</strong> to view organization details
      </li>
      <li>
        <Icon icon="mdi:circle-small" /> Click the
        <strong>chevron icon</strong> to expand or collapse sub-organizations
      </li>
      <li>
        <Icon icon="mdi:circle-small" /> Use the
        <strong>search bar</strong> to filter the tree
      </li>
    </ul>
  </Card>
</Container>

{#if modalOpen && selectedOrg}
  <div
    class="modal-backdrop"
    onclick={closeModal}
    onkeydown={(e) => e.key === "Escape" && closeModal()}
    role="button"
    tabindex="-1"
  >
    <div
      class="modal"
      onclick={(e) => e.stopPropagation()}
      role="dialog"
      tabindex="-1"
      aria-labelledby="modal-title"
    >
      <button class="modal-close" onclick={closeModal} aria-label="Close">
        <Icon icon="mdi:close" />
      </button>
      <h2 id="modal-title" class="modal-title">{selectedOrg.name}</h2>

      <div class="modal-field">
        <h3 class="field-label">Type</h3>
        <p class="field-value">{selectedOrg.type ?? "Organization"}</p>
      </div>

      {#if selectedOrg.description}
        <div class="modal-field">
          <h3 class="field-label">Description</h3>
          <p class="field-value">{selectedOrg.description}</p>
        </div>
      {/if}

      {#if selectedOrg.children && selectedOrg.children.length > 0}
        <div class="modal-field">
          <h3 class="field-label">
            Sub-Organizations ({selectedOrg.children.length})
          </h3>
          <ul class="sub-list">
            {#each selectedOrg.children as child (child.id)}
              <li>
                <span class="bullet"></span>
                {child.name}
              </li>
            {/each}
          </ul>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .search-row {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .stats-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .stat-box {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1rem 1.5rem;
    text-align: center;
    min-width: 140px;
    box-shadow: var(--shadow-sm);
  }

  .stat-box.gold {
    border-color: var(--sec);
  }

  .stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
    margin: 0 0 0.25rem 0;
  }

  .stat-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0;
  }

  .chart-scroll {
    overflow-x: auto;
    padding: 1rem 0 2rem;
    display: flex;
    justify-content: center;
    min-height: 400px;
  }

  .no-match {
    text-align: center;
    color: var(--text-secondary);
    margin: 2rem 0;
    font-size: 0.925rem;
  }

  .how-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 0.75rem 0;
  }

  :global(.how-icon) {
    color: var(--sec);
    font-size: 1.25rem;
  }

  .how-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    color: var(--text-secondary);
    font-size: 0.925rem;
  }

  .how-list li {
    display: flex;
    align-items: center;
    gap: 0.375rem;
  }

  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 400;
    padding: 1rem;
  }

  .modal {
    background: white;
    border-radius: 1.5rem;
    padding: 2rem;
    max-width: 32rem;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: var(--shadow-lg);
  }

  .modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-secondary);
    font-size: 1.5rem;
    padding: 0.25rem;
    display: flex;
  }

  .modal-close:hover {
    color: var(--pri);
  }

  .modal-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0 2rem 1.5rem 0;
  }

  .modal-field {
    margin-bottom: 1.25rem;
  }

  .field-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
    margin: 0 0 0.25rem 0;
    font-weight: 600;
  }

  .field-value {
    color: var(--text-primary);
    margin: 0;
    line-height: 1.6;
    text-transform: capitalize;
  }

  .sub-list {
    list-style: none;
    padding: 0;
    margin: 0.5rem 0 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
  }

  .sub-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-secondary);
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    color: var(--text-primary);
    font-size: 0.925rem;
  }

  .bullet {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: var(--sec);
    flex-shrink: 0;
  }
</style>
