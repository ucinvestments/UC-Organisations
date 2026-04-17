import { c as attr, ac as bind_props, a as attr_class, ad as attr_style, d as stringify, e as escape_html, b as ensure_array_like, f as derived } from "../../chunks/renderer.js";
import { I as Icon } from "../../chunks/Icon.js";
import { H as Hero, C as Container } from "../../chunks/Container.js";
function SearchInput($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { value = "", placeholder = "Search...", onInput, onClear } = $$props;
    $$renderer2.push(`<div class="search-wrapper svelte-4cijiw">`);
    Icon($$renderer2, { icon: "mdi:magnify", class: "search-icon" });
    $$renderer2.push(`<!----> <input type="text"${attr("placeholder", placeholder)}${attr("value", value)} class="search-input svelte-4cijiw"/> `);
    if (value) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<button class="clear-btn svelte-4cijiw" aria-label="Clear search">`);
      Icon($$renderer2, { icon: "mdi:close" });
      $$renderer2.push(`<!----></button>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { value });
  });
}
function Card($$renderer, $$props) {
  let { hover = true, padding = "2.5rem", children } = $$props;
  $$renderer.push(`<div${attr_class("card svelte-1udyrqm", void 0, { "hoverable": hover })}${attr_style(`padding: ${stringify(padding)}`)}>`);
  children?.($$renderer);
  $$renderer.push(`<!----></div>`);
}
function OrgChart_1($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { node, depth = 0, onInfoClick } = $$props;
    let collapsed = false;
    const palettes = [
      {
        border: "var(--founder)",
        bg: "linear-gradient(135deg, #f3f6ff 0%, #e2e8ff 100%)",
        avatar: "var(--founder)"
      },
      {
        border: "var(--golden-gate)",
        bg: "linear-gradient(135deg, #fff9e6 0%, #ffe9bf 100%)",
        avatar: "var(--golden-gate)"
      },
      {
        border: "var(--lap-lane)",
        bg: "linear-gradient(135deg, #f0fff6 0%, #d9ffe9 100%)",
        avatar: "var(--lap-lane)"
      },
      {
        border: "var(--rose-garden)",
        bg: "linear-gradient(135deg, #fff5f3 0%, #ffe4de 100%)",
        avatar: "var(--rose-garden)"
      },
      {
        border: "var(--lawrence)",
        bg: "linear-gradient(135deg, #ecfcff 0%, #cfefff 100%)",
        avatar: "var(--lawrence)"
      }
    ];
    const accent = derived(() => palettes[depth % palettes.length]);
    const hasChildren = derived(() => (node.children?.length ?? 0) > 0);
    const initials = derived(() => node.name.split(" ").filter(Boolean).map((w) => w[0]?.toUpperCase()).slice(0, 2).join(""));
    const typeLabel = derived(() => node.type ? node.type.charAt(0).toUpperCase() + node.type.slice(1) : "Organization");
    $$renderer2.push(`<div class="tree-node svelte-1mwttsi"><div class="card svelte-1mwttsi"${attr_style(`border-color: ${stringify(accent().border)}; background: ${stringify(accent().bg)};`)}><div class="card-header svelte-1mwttsi"><div class="avatar svelte-1mwttsi"${attr_style(`background: ${stringify(accent().avatar)}`)}>${escape_html(initials())}</div> <div class="text svelte-1mwttsi"><p class="title svelte-1mwttsi">${escape_html(node.name)}</p> <p class="meta svelte-1mwttsi">${escape_html(typeLabel())}`);
    if (hasChildren()) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`· ${escape_html(node.children.length)} sub-organization${escape_html(node.children.length !== 1 ? "s" : "")}`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></p></div> <div class="actions svelte-1mwttsi"><button class="icon-btn svelte-1mwttsi" aria-label="View information">`);
    Icon($$renderer2, { icon: "mdi:information-outline" });
    $$renderer2.push(`<!----></button> `);
    if (hasChildren()) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<button${attr_class("icon-btn svelte-1mwttsi", void 0, { "collapsed": collapsed })}${attr("aria-label", "Collapse")}>`);
      Icon($$renderer2, { icon: "mdi:chevron-down" });
      $$renderer2.push(`<!----></button>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div></div> `);
    if (node.description) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="description svelte-1mwttsi">${escape_html(node.description)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> `);
    if (hasChildren() && !collapsed) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="children svelte-1mwttsi"><!--[-->`);
      const each_array = ensure_array_like(node.children);
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let child = each_array[$$index];
        $$renderer2.push(`<div class="child-wrapper svelte-1mwttsi">`);
        OrgChart_1($$renderer2, { node: child, depth: depth + 1, onInfoClick });
        $$renderer2.push(`<!----></div>`);
      }
      $$renderer2.push(`<!--]--></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div>`);
  });
}
const ucInvestmentsOrg = {
  id: "cio",
  name: "Chief Investment Officer, Senior Vice President – Investments",
  type: "office",
  description: "Office of the Chief Investment Officer",
  children: [
    {
      id: "investment-management",
      name: "Investment Management",
      type: "department",
      description: "Manages UC investment portfolios",
      children: [
        {
          id: "public-equity",
          name: "Public Equity",
          type: "team",
          description: "Public equity investments and strategies"
        },
        {
          id: "fixed-income",
          name: "Fixed Income",
          type: "team",
          description: "Fixed income securities and bonds"
        },
        {
          id: "alternative-investment",
          name: "Alternative Investment",
          type: "team",
          description: "Alternative investment strategies including private equity and real assets"
        }
      ]
    },
    {
      id: "sustainability",
      name: "Sustainability",
      type: "department",
      description: "Sustainable and responsible investment practices"
    },
    {
      id: "risk-management",
      name: "Risk Management",
      type: "department",
      description: "Investment risk assessment and management"
    },
    {
      id: "investment-services",
      name: "Investment Services",
      type: "department",
      description: "Supporting services for investment operations",
      children: [
        {
          id: "cash-liquidity",
          name: "Cash and Liquidity Management",
          type: "team",
          description: "Managing cash positions and liquidity requirements"
        },
        {
          id: "data-analytics",
          name: "Data Mgmt. & Analytics",
          type: "team",
          description: "Investment data management and analytical support"
        },
        {
          id: "client-relations",
          name: "Client Relations",
          type: "team",
          description: "Managing relationships with UC clients and stakeholders"
        },
        {
          id: "investment-transactions",
          name: "Investment Transactions",
          type: "team",
          description: "Processing and settling investment transactions"
        },
        {
          id: "investment-support",
          name: "Investment Support",
          type: "team",
          description: "General investment operations support"
        }
      ]
    }
  ]
};
const governanceOrg = {
  id: "regents",
  name: "The Regents of the University of California",
  type: "committee",
  description: "UC System governing board",
  children: [
    {
      id: "regents-investment-committee",
      name: "UC Regents Committee on Investments",
      type: "committee",
      description: "Oversees UC investment policies",
      children: [
        {
          id: "investment-advisory",
          name: "UC Regents Investment Advisory Committee",
          type: "committee",
          description: "Provides investment advice and recommendations"
        }
      ]
    }
  ]
};
const leadershipOrg = {
  id: "president",
  name: "President of the University of California",
  type: "position",
  description: "UC System President",
  children: [
    {
      id: "cfo",
      name: "Chief Financial Officer",
      type: "position",
      description: "UC System CFO"
    }
  ]
};
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const rootNode = {
      id: "uc-org-root",
      name: "UC Organisations",
      type: "office",
      description: "University of California Investment Office structure",
      children: [leadershipOrg, governanceOrg, ucInvestmentsOrg]
    };
    let searchQuery = "";
    let selectedOrg = null;
    let modalOpen = false;
    function filterTree(node, query) {
      const normalized = query.toLowerCase();
      const matches = node.name.toLowerCase().includes(normalized) || node.type?.toLowerCase().includes(normalized) || node.description?.toLowerCase().includes(normalized);
      const filteredChildren = node.children?.map((child) => filterTree(child, query)).filter((child) => Boolean(child));
      if (matches || filteredChildren && filteredChildren.length > 0) {
        return { ...node, children: filteredChildren };
      }
      return null;
    }
    function countNodes(node) {
      if (!node) return 0;
      const childCount = node.children?.reduce((sum, child) => sum + countNodes(child), 0) ?? 0;
      return 1 + childCount;
    }
    const filtered = derived(() => searchQuery.trim() ? filterTree(rootNode, searchQuery.trim()) ?? { ...rootNode, children: [] } : rootNode);
    const totalNodes = derived(() => countNodes(filtered()));
    const rootChildren = derived(() => filtered().children?.length ?? 0);
    function openInfo(org) {
      selectedOrg = org;
      modalOpen = true;
    }
    let $$settled = true;
    let $$inner_renderer;
    function $$render_inner($$renderer3) {
      Hero($$renderer3, {
        title: "UC Organisations Hierarchy",
        subtitle: "Explore the Office of the Chief Investment Officer — committees, departments, and reporting lines."
      });
      $$renderer3.push(`<!----> `);
      Container($$renderer3, {
        children: ($$renderer4) => {
          $$renderer4.push(`<div class="search-row svelte-1uha8ag">`);
          SearchInput($$renderer4, {
            placeholder: "Search organizations, types, descriptions…",
            get value() {
              return searchQuery;
            },
            set value($$value) {
              searchQuery = $$value;
              $$settled = false;
            }
          });
          $$renderer4.push(`<!----></div> <div class="stats-row svelte-1uha8ag"><div class="stat-box svelte-1uha8ag"><p class="stat-label svelte-1uha8ag">Total Nodes</p> <p class="stat-value svelte-1uha8ag">${escape_html(totalNodes())}</p></div> <div class="stat-box gold svelte-1uha8ag"><p class="stat-label svelte-1uha8ag">Root Children</p> <p class="stat-value svelte-1uha8ag">${escape_html(rootChildren())}</p></div></div> <div class="chart-scroll svelte-1uha8ag"><!---->`);
          {
            OrgChart_1($$renderer4, { node: filtered(), onInfoClick: openInfo });
          }
          $$renderer4.push(`<!----></div> `);
          if (searchQuery && filtered().children?.length === 0) {
            $$renderer4.push("<!--[0-->");
            $$renderer4.push(`<p class="no-match svelte-1uha8ag">No matches found. Try another search term.</p>`);
          } else {
            $$renderer4.push("<!--[-1-->");
          }
          $$renderer4.push(`<!--]--> `);
          Card($$renderer4, {
            hover: false,
            padding: "1.5rem",
            children: ($$renderer5) => {
              $$renderer5.push(`<h3 class="how-title svelte-1uha8ag">`);
              Icon($$renderer5, { icon: "mdi:lightbulb-on", class: "how-icon" });
              $$renderer5.push(`<!----> How to Use</h3> <ul class="how-list svelte-1uha8ag"><li class="svelte-1uha8ag">`);
              Icon($$renderer5, { icon: "mdi:circle-small" });
              $$renderer5.push(`<!----> Click the <strong>info icon</strong> to view organization details</li> <li class="svelte-1uha8ag">`);
              Icon($$renderer5, { icon: "mdi:circle-small" });
              $$renderer5.push(`<!----> Click the <strong>chevron icon</strong> to expand or collapse sub-organizations</li> <li class="svelte-1uha8ag">`);
              Icon($$renderer5, { icon: "mdi:circle-small" });
              $$renderer5.push(`<!----> Use the <strong>search bar</strong> to filter the tree</li></ul>`);
            }
          });
          $$renderer4.push(`<!---->`);
        }
      });
      $$renderer3.push(`<!----> `);
      if (modalOpen && selectedOrg) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<div class="modal-backdrop svelte-1uha8ag" role="button" tabindex="-1"><div class="modal svelte-1uha8ag" role="dialog" tabindex="-1" aria-labelledby="modal-title"><button class="modal-close svelte-1uha8ag" aria-label="Close">`);
        Icon($$renderer3, { icon: "mdi:close" });
        $$renderer3.push(`<!----></button> <h2 id="modal-title" class="modal-title svelte-1uha8ag">${escape_html(selectedOrg.name)}</h2> <div class="modal-field svelte-1uha8ag"><h3 class="field-label svelte-1uha8ag">Type</h3> <p class="field-value svelte-1uha8ag">${escape_html(selectedOrg.type ?? "Organization")}</p></div> `);
        if (selectedOrg.description) {
          $$renderer3.push("<!--[0-->");
          $$renderer3.push(`<div class="modal-field svelte-1uha8ag"><h3 class="field-label svelte-1uha8ag">Description</h3> <p class="field-value svelte-1uha8ag">${escape_html(selectedOrg.description)}</p></div>`);
        } else {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--> `);
        if (selectedOrg.children && selectedOrg.children.length > 0) {
          $$renderer3.push("<!--[0-->");
          $$renderer3.push(`<div class="modal-field svelte-1uha8ag"><h3 class="field-label svelte-1uha8ag">Sub-Organizations (${escape_html(selectedOrg.children.length)})</h3> <ul class="sub-list svelte-1uha8ag"><!--[-->`);
          const each_array = ensure_array_like(selectedOrg.children);
          for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
            let child = each_array[$$index];
            $$renderer3.push(`<li class="svelte-1uha8ag"><span class="bullet svelte-1uha8ag"></span> ${escape_html(child.name)}</li>`);
          }
          $$renderer3.push(`<!--]--></ul></div>`);
        } else {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--></div></div>`);
      } else {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]-->`);
    }
    do {
      $$settled = true;
      $$inner_renderer = $$renderer2.copy();
      $$render_inner($$inner_renderer);
    } while (!$$settled);
    $$renderer2.subsume($$inner_renderer);
  });
}
export {
  _page as default
};
