<script lang="ts">
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";
  import { fade } from "svelte/transition";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";

  let { children } = $props();

  const navLinks = [
    { href: "/", label: "Org Chart", icon: "mdi:sitemap" },
    { href: "/create", label: "Create", icon: "mdi:plus-circle" },
    { href: "/edit", label: "Edit", icon: "mdi:pencil" },
    {
      href: "https://github.com/ucinvestments/UC-Organisations",
      label: "GitHub",
      icon: "mdi:github",
      external: true,
    },
  ];

  const footerLinks = [
    { href: "/", label: "Org Chart" },
    { href: "/create", label: "Create Records" },
    { href: "/edit", label: "Edit Records" },
  ];
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <title>UC Organisations</title>
</svelte:head>

<Navbar appName="UC Organisations" logoIcon="mdi:sitemap" links={navLinks} />

<main in:fade={{ duration: 300 }}>
  {@render children?.()}
</main>

<Footer
  appName="UC Organisations"
  description="University of California Investment Office organizational structure."
  links={footerLinks}
  contactEmail="admin@ucinvestments.info"
  copyrightHolder="UC Organisations"
  affiliationDisclaimer="Not affiliated with or authorized by the University of California."
/>

<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  main {
    min-height: calc(100vh - 400px);
  }
</style>
