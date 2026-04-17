import { c as attr, a as attr_class, d as stringify } from "./renderer.js";
import { I as Icon } from "./Icon.js";
import { p as public_env } from "./shared-server.js";
function Button($$renderer, $$props) {
  let {
    href = "",
    variant = "primary",
    icon = "",
    external = false,
    onClick,
    disabled = false,
    children
  } = $$props;
  if (href) {
    $$renderer.push("<!--[0-->");
    $$renderer.push(`<a${attr("href", href)}${attr_class(`button ${stringify(variant)}`, "svelte-18sv61c", { "disabled": disabled })}${attr("target", external ? "_blank" : void 0)}${attr("rel", external ? "noopener noreferrer" : void 0)}>`);
    if (icon) {
      $$renderer.push("<!--[0-->");
      Icon($$renderer, { icon, class: "button-icon" });
    } else {
      $$renderer.push("<!--[-1-->");
    }
    $$renderer.push(`<!--]--> `);
    children?.($$renderer);
    $$renderer.push(`<!----> `);
    if (external) {
      $$renderer.push("<!--[0-->");
      Icon($$renderer, { icon: "mdi:open-in-new", class: "external-icon" });
    } else {
      $$renderer.push("<!--[-1-->");
    }
    $$renderer.push(`<!--]--></a>`);
  } else {
    $$renderer.push("<!--[-1-->");
    $$renderer.push(`<button${attr_class(`button ${stringify(variant)}`, "svelte-18sv61c", { "disabled": disabled })}${attr("disabled", disabled, true)}>`);
    if (icon) {
      $$renderer.push("<!--[0-->");
      Icon($$renderer, { icon, class: "button-icon" });
    } else {
      $$renderer.push("<!--[-1-->");
    }
    $$renderer.push(`<!--]--> `);
    children?.($$renderer);
    $$renderer.push(`<!----></button>`);
  }
  $$renderer.push(`<!--]-->`);
}
(public_env.PUBLIC_API_BASE_URL || "http://localhost:5000").replace(
  /\/$/,
  ""
);
export {
  Button as B
};
