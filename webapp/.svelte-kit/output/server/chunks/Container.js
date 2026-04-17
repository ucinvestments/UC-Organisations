import { e as escape_html, ad as attr_style, d as stringify } from "./renderer.js";
import "clsx";
function Hero($$renderer, $$props) {
  let { title, subtitle = "", pattern = true, children } = $$props;
  $$renderer.push(`<div class="hero svelte-1q37ri0">`);
  if (pattern) {
    $$renderer.push("<!--[0-->");
    $$renderer.push(`<div class="hero-pattern svelte-1q37ri0"></div>`);
  } else {
    $$renderer.push("<!--[-1-->");
  }
  $$renderer.push(`<!--]--> <div class="hero-content svelte-1q37ri0"><h1 class="hero-title svelte-1q37ri0">${escape_html(title)}</h1> `);
  if (subtitle) {
    $$renderer.push("<!--[0-->");
    $$renderer.push(`<p class="hero-subtitle svelte-1q37ri0">${escape_html(subtitle)}</p>`);
  } else {
    $$renderer.push("<!--[-1-->");
  }
  $$renderer.push(`<!--]--> `);
  children?.($$renderer);
  $$renderer.push(`<!----></div></div>`);
}
function Container($$renderer, $$props) {
  let { maxWidth = "1200px", padding = "3rem 2rem", children } = $$props;
  $$renderer.push(`<div class="container svelte-1ginl5v"${attr_style(`max-width: ${stringify(maxWidth)}; padding: ${stringify(padding)}`)}>`);
  children?.($$renderer);
  $$renderer.push(`<!----></div>`);
}
export {
  Container as C,
  Hero as H
};
