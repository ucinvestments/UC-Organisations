<script lang="ts">
  import Icon from "@iconify/svelte";
  import OrgChart from "./OrgChart.svelte";
  import type { Organization } from "$lib/types";

  interface Props {
    node: Organization;
    depth?: number;
    onInfoClick: (org: Organization) => void;
  }

  let { node, depth = 0, onInfoClick }: Props = $props();

  let collapsed = $state(false);

  const palettes = [
    { border: "var(--founder)", bg: "linear-gradient(135deg, #f3f6ff 0%, #e2e8ff 100%)", avatar: "var(--founder)" },
    { border: "var(--golden-gate)", bg: "linear-gradient(135deg, #fff9e6 0%, #ffe9bf 100%)", avatar: "var(--golden-gate)" },
    { border: "var(--lap-lane)", bg: "linear-gradient(135deg, #f0fff6 0%, #d9ffe9 100%)", avatar: "var(--lap-lane)" },
    { border: "var(--rose-garden)", bg: "linear-gradient(135deg, #fff5f3 0%, #ffe4de 100%)", avatar: "var(--rose-garden)" },
    { border: "var(--lawrence)", bg: "linear-gradient(135deg, #ecfcff 0%, #cfefff 100%)", avatar: "var(--lawrence)" },
  ];

  const accent = $derived(palettes[depth % palettes.length]);
  const hasChildren = $derived((node.children?.length ?? 0) > 0);
  const initials = $derived(
    node.name
      .split(" ")
      .filter(Boolean)
      .map((w) => w[0]?.toUpperCase())
      .slice(0, 2)
      .join(""),
  );
  const typeLabel = $derived(
    node.type ? node.type.charAt(0).toUpperCase() + node.type.slice(1) : "Organization",
  );
</script>

<div class="tree-node">
  <div
    class="card"
    style="border-color: {accent.border}; background: {accent.bg};"
  >
    <div class="card-header">
      <div class="avatar" style="background: {accent.avatar}">
        {initials}
      </div>
      <div class="text">
        <p class="title">{node.name}</p>
        <p class="meta">
          {typeLabel}{#if hasChildren} · {node.children!.length} sub-organization{node.children!.length !== 1 ? "s" : ""}{/if}
        </p>
      </div>
      <div class="actions">
        <button
          class="icon-btn"
          onclick={(e) => {
            e.stopPropagation();
            onInfoClick(node);
          }}
          aria-label="View information"
        >
          <Icon icon="mdi:information-outline" />
        </button>
        {#if hasChildren}
          <button
            class="icon-btn"
            class:collapsed
            onclick={(e) => {
              e.stopPropagation();
              collapsed = !collapsed;
            }}
            aria-label={collapsed ? "Expand" : "Collapse"}
          >
            <Icon icon="mdi:chevron-down" />
          </button>
        {/if}
      </div>
    </div>
    {#if node.description}
      <p class="description">{node.description}</p>
    {/if}
  </div>

  {#if hasChildren && !collapsed}
    <div class="children">
      {#each node.children! as child (child.id)}
        <div class="child-wrapper">
          <OrgChart node={child} depth={depth + 1} {onInfoClick} />
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .tree-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }

  .card {
    border: 2px solid;
    border-radius: 1rem;
    padding: 1rem 1.25rem;
    min-width: 240px;
    max-width: 320px;
    box-shadow: var(--shadow-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    z-index: 1;
  }

  .card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  .card-header {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    color: white;
    font-family: "Space Grotesk", sans-serif;
    font-weight: 700;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .text {
    flex: 1;
    min-width: 0;
  }

  .title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 0.9375rem;
    font-weight: 700;
    color: var(--pri);
    line-height: 1.3;
    margin: 0 0 0.25rem 0;
  }

  .meta {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin: 0;
  }

  .actions {
    display: flex;
    gap: 0.25rem;
    flex-shrink: 0;
  }

  .icon-btn {
    width: 1.75rem;
    height: 1.75rem;
    border: 1px solid var(--border);
    background: white;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .icon-btn:hover {
    color: var(--pri);
    border-color: var(--pri);
  }

  .icon-btn.collapsed {
    transform: rotate(-90deg);
  }

  .description {
    margin: 0.75rem 0 0 0;
    font-size: 0.8125rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .children {
    display: flex;
    gap: 1.5rem;
    margin-top: 2rem;
    position: relative;
    flex-wrap: nowrap;
  }

  /* Vertical line from parent down to children row */
  .children::before {
    content: "";
    position: absolute;
    top: -2rem;
    left: 50%;
    width: 2px;
    height: 1rem;
    background: var(--border);
  }

  /* Horizontal line across children */
  .children::after {
    content: "";
    position: absolute;
    top: -1rem;
    left: calc(50% / var(--child-count, 1));
    right: calc(50% / var(--child-count, 1));
    height: 2px;
    background: var(--border);
  }

  .child-wrapper {
    position: relative;
    display: flex;
    justify-content: center;
  }

  /* Vertical line from the horizontal line down to each child card */
  .child-wrapper::before {
    content: "";
    position: absolute;
    top: -1rem;
    left: 50%;
    width: 2px;
    height: 1rem;
    background: var(--border);
  }

  /* Hide horizontal line extension at first/last child edges */
  .child-wrapper:first-child::after,
  .child-wrapper:last-child::after {
    content: "";
    position: absolute;
    top: -1rem;
    height: 2px;
    background: white;
    width: 50%;
  }

  .child-wrapper:first-child::after {
    left: 0;
  }

  .child-wrapper:last-child::after {
    right: 0;
  }

  @media (max-width: 900px) {
    .children {
      flex-direction: column;
      align-items: center;
    }

    .children::after {
      display: none;
    }

    .child-wrapper:first-child::after,
    .child-wrapper:last-child::after {
      display: none;
    }
  }
</style>
