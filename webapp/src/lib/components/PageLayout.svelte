<script lang="ts">
  import type { Snippet } from "svelte";

  let {
    backgroundGradient = true,
    children,
  }: {
    backgroundGradient?: boolean;
    children?: Snippet;
  } = $props();
</script>

<div class="page-layout" class:gradient={backgroundGradient}>
  {@render children?.()}
</div>

<style>
  .page-layout {
    min-height: 100vh;
    background: var(--bg);
  }

  .page-layout.gradient {
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }
</style>
