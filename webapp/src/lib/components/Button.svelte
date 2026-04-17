<script lang="ts">
  import Icon from "@iconify/svelte";
  import type { Snippet } from "svelte";

  let {
    href = "",
    variant = "primary",
    icon = "",
    external = false,
    onClick,
    disabled = false,
    children,
  }: {
    href?: string;
    variant?: "primary" | "secondary" | "accent";
    icon?: string;
    external?: boolean;
    onClick?: () => void;
    disabled?: boolean;
    children?: Snippet;
  } = $props();
</script>

{#if href}
  <a
    {href}
    class="button {variant}"
    class:disabled
    target={external ? "_blank" : undefined}
    rel={external ? "noopener noreferrer" : undefined}
  >
    {#if icon}
      <Icon {icon} class="button-icon" />
    {/if}
    {@render children?.()}
    {#if external}
      <Icon icon="mdi:open-in-new" class="external-icon" />
    {/if}
  </a>
{:else}
  <button class="button {variant}" class:disabled onclick={onClick} {disabled}>
    {#if icon}
      <Icon {icon} class="button-icon" />
    {/if}
    {@render children?.()}
  </button>
{/if}

<style>
  .button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
    text-decoration: none;
    cursor: pointer;
    border: none;
    font-size: inherit;
    font-family: inherit;
  }

  .button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  .button:hover:not(.disabled) {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .primary {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
  }

  .secondary {
    background: white;
    color: var(--pri);
    border: 2px solid var(--border);
  }

  .accent {
    background: linear-gradient(135deg, var(--golden-gate), var(--sec));
    color: white;
  }

  :global(.button-icon) {
    font-size: 1.125rem;
  }

  :global(.external-icon) {
    font-size: 0.875rem;
    margin-left: -0.125rem;
  }

  @media (max-width: 768px) {
    .button {
      justify-content: center;
    }
  }
</style>
