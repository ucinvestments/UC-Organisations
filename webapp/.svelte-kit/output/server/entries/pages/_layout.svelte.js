import { g as getContext, e as escape_html, a as attr_class, b as ensure_array_like, c as attr, s as store_get, u as unsubscribe_stores, d as stringify, f as derived, h as head } from "../../chunks/renderer.js";
import { I as Icon, h as html } from "../../chunks/Icon.js";
import "clsx";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/root.js";
import "../../chunks/state.svelte.js";
const favicon = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNiIgZmlsbD0iIzAwMzI2MiIvPjx0ZXh0IHg9IjUwJSIgeT0iNTglIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iLWFwcGxlLXN5c3RlbSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4IiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0iI2ZkYjUxNSI+VUM8L3RleHQ+PC9zdmc+Cg==";
const getStores = () => {
  const stores$1 = getContext("__svelte__");
  return {
    /** @type {typeof page} */
    page: {
      subscribe: stores$1.page.subscribe
    },
    /** @type {typeof navigating} */
    navigating: {
      subscribe: stores$1.navigating.subscribe
    },
    /** @type {typeof updated} */
    updated: stores$1.updated
  };
};
const page = {
  subscribe(fn) {
    const store = getStores().page;
    return store.subscribe(fn);
  }
};
function Navbar($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let {
      appName = "UC Data",
      logoIcon = "mdi:chart-donut",
      subtitle = "",
      links = []
    } = $$props;
    let mobileOpen = false;
    $$renderer2.push(`<nav class="navbar svelte-rfuq4y"><div class="nav-container svelte-rfuq4y"><a href="/" class="logo-link svelte-rfuq4y"><div class="logo svelte-rfuq4y">`);
    Icon($$renderer2, { icon: logoIcon, class: "logo-icon" });
    $$renderer2.push(`<!----> <span class="logo-text svelte-rfuq4y"><strong>${escape_html(appName)}</strong> `);
    if (subtitle) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<small class="small-subtitle svelte-rfuq4y">${escape_html(subtitle)}</small>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></span></div></a> <button class="burger-btn svelte-rfuq4y" aria-label="Toggle menu">`);
    Icon($$renderer2, {
      icon: "mdi:menu",
      class: "burger-icon"
    });
    $$renderer2.push(`<!----></button> <div${attr_class("nav-links svelte-rfuq4y", void 0, { "mobile-open": mobileOpen })}><!--[-->`);
    const each_array = ensure_array_like(links);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let link = each_array[$$index];
      $$renderer2.push(`<a${attr("href", link.href)}${attr_class("nav-link svelte-rfuq4y", void 0, {
        "active": store_get($$store_subs ??= {}, "$page", page).url.pathname === link.href,
        "external": link.external
      })}${attr("target", link.external ? "_blank" : void 0)}${attr("rel", link.external ? "noopener noreferrer" : void 0)}>`);
      Icon($$renderer2, { icon: link.icon, class: "nav-icon" });
      $$renderer2.push(`<!----> ${escape_html(link.label)} `);
      if (link.external) {
        $$renderer2.push("<!--[0-->");
        Icon($$renderer2, { icon: "mdi:open-in-new", class: "external-icon" });
      } else {
        $$renderer2.push("<!--[-1-->");
      }
      $$renderer2.push(`<!--]--></a>`);
    }
    $$renderer2.push(`<!--]--></div></div></nav>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
function Footer($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let {
      appName = "UC Data",
      description = "University of California data transparency tool.",
      links = [],
      contactEmail = "contact@example.com",
      dataSources = "",
      cryptoAddresses = [],
      copyrightHolder = "",
      affiliationDisclaimer = ""
    } = $$props;
    const emailDomain = derived(() => contactEmail.split("@")[1] ?? "");
    const holder = derived(() => copyrightHolder || appName);
    const year = (/* @__PURE__ */ new Date()).getFullYear();
    $$renderer2.push(`<footer class="footer svelte-jz8lnl"><div class="footer-content svelte-jz8lnl"><div class="footer-section svelte-jz8lnl"><h4 class="footer-title svelte-jz8lnl">${escape_html(appName)}</h4> <p class="footer-text svelte-jz8lnl">${escape_html(description)}</p></div> <div class="footer-section svelte-jz8lnl"><h4 class="footer-title svelte-jz8lnl">Quick Links</h4> <div class="footer-links svelte-jz8lnl"><!--[-->`);
    const each_array = ensure_array_like(links);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let link = each_array[$$index];
      $$renderer2.push(`<a${attr("href", link.href)} class="footer-link svelte-jz8lnl"${attr("target", link.external ? "_blank" : void 0)}${attr("rel", link.external ? "noopener noreferrer" : void 0)}>${escape_html(link.label)} `);
      if (link.external) {
        $$renderer2.push("<!--[0-->");
        Icon($$renderer2, { icon: "mdi:open-in-new", class: "footer-external" });
      } else {
        $$renderer2.push("<!--[-1-->");
      }
      $$renderer2.push(`<!--]--></a>`);
    }
    $$renderer2.push(`<!--]--></div></div> <div class="footer-section svelte-jz8lnl"><h4 class="footer-title svelte-jz8lnl">Contact</h4> <div class="footer-links svelte-jz8lnl"><a${attr("href", `mailto:${stringify(contactEmail)}`)} class="footer-link svelte-jz8lnl">Contact Us</a> `);
    if (emailDomain()) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<a${attr("href", `mailto:press@${stringify(emailDomain())}`)} class="footer-link svelte-jz8lnl">Submit Research</a> <a${attr("href", `mailto:dev@${stringify(emailDomain())}`)} class="footer-link svelte-jz8lnl">Development</a>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div></div> `);
    if (cryptoAddresses.length > 0) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="footer-section svelte-jz8lnl"><h4 class="footer-title svelte-jz8lnl">Support This Project</h4> <p class="footer-text svelte-jz8lnl">Self-funded. Donations help cover hosting and API costs.</p> <div class="donation-links svelte-jz8lnl"><button class="donate-button svelte-jz8lnl">`);
      Icon($$renderer2, { icon: "mdi:heart", class: "donate-icon" });
      $$renderer2.push(`<!----> Donate</button> `);
      {
        $$renderer2.push("<!--[-1-->");
      }
      $$renderer2.push(`<!--]--></div></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    if (dataSources) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="footer-section svelte-jz8lnl"><h4 class="footer-title svelte-jz8lnl">Data Sources</h4> <p class="footer-text svelte-jz8lnl">${html(dataSources)}</p></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="footer-bottom svelte-jz8lnl"><p class="svelte-jz8lnl">© ${escape_html(year)} ${escape_html(holder())}. Educational purposes only. `);
    if (affiliationDisclaimer) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<br/>${escape_html(affiliationDisclaimer)}`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></p></div></footer>`);
  });
}
function _layout($$renderer, $$props) {
  let { children } = $$props;
  const navLinks = [
    { href: "/", label: "Org Chart", icon: "mdi:sitemap" },
    { href: "/create", label: "Create", icon: "mdi:plus-circle" },
    { href: "/edit", label: "Edit", icon: "mdi:pencil" },
    {
      href: "https://github.com/ucinvestments/UC-Organisations",
      label: "GitHub",
      icon: "mdi:github",
      external: true
    }
  ];
  const footerLinks = [
    { href: "/", label: "Org Chart" },
    { href: "/create", label: "Create Records" },
    { href: "/edit", label: "Edit Records" }
  ];
  head("12qhfyh", $$renderer, ($$renderer2) => {
    $$renderer2.title(($$renderer3) => {
      $$renderer3.push(`<title>UC Organisations</title>`);
    });
    $$renderer2.push(`<link rel="icon"${attr("href", favicon)}/>`);
  });
  Navbar($$renderer, {
    appName: "UC Organisations",
    logoIcon: "mdi:sitemap",
    links: navLinks
  });
  $$renderer.push(`<!----> <main class="svelte-12qhfyh">`);
  children?.($$renderer);
  $$renderer.push(`<!----></main> `);
  Footer($$renderer, {
    appName: "UC Organisations",
    description: "University of California Investment Office organizational structure.",
    links: footerLinks,
    contactEmail: "admin@ucinvestments.info",
    copyrightHolder: "UC Organisations",
    affiliationDisclaimer: "Not affiliated with or authorized by the University of California."
  });
  $$renderer.push(`<!---->`);
}
export {
  _layout as default
};
