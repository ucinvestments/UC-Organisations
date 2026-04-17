<script lang="ts">
  import type { Snippet } from "svelte";

  let {
    maxWidth = "1200px",
    padding = "3rem 2rem",
    children,
  }: {
    maxWidth?: string;
    padding?: string;
    children?: Snippet;
  } = $props();
</script>

<div class="container" style="max-width: {maxWidth}; padding: {padding}">
  {@render children?.()}
</div>

<style>
  .container {
    margin: 0 auto;
  }

  @media (max-width: 768px) {
    .container {
      padding: 2rem 1rem !important;
    }
  }
</style>
