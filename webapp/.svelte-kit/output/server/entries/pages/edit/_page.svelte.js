import { c as attr, b as ensure_array_like, a as attr_class, e as escape_html, f as derived } from "../../../chunks/renderer.js";
import "../../../chunks/Icon.js";
import { H as Hero, C as Container } from "../../../chunks/Container.js";
import { B as Button } from "../../../chunks/api.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const personEditFields = [
      {
        key: "first_name",
        label: "First Name",
        type: "text",
        placeholder: "Jane"
      },
      {
        key: "last_name",
        label: "Last Name",
        type: "text",
        placeholder: "Doe"
      },
      {
        key: "middle_name",
        label: "Middle Name",
        type: "text",
        placeholder: "A."
      },
      { key: "preferred_name", label: "Preferred Name", type: "text" },
      { key: "bio", label: "Bio", type: "textarea" },
      { key: "profile_url", label: "Profile URL", type: "url" },
      { key: "photo_url", label: "Photo URL", type: "url" },
      {
        key: "social_platform",
        label: "Social Platform",
        type: "text"
      },
      { key: "social_handle", label: "Social Handle", type: "text" },
      { key: "social_url", label: "Social URL", type: "url" },
      { key: "contact_type", label: "Contact Type", type: "text" },
      { key: "contact_value", label: "Contact Value", type: "text" },
      { key: "contact_label", label: "Contact Label", type: "text" }
    ];
    const orgEditFields = [
      { key: "name", label: "Name", type: "text" },
      { key: "slug", label: "Slug", type: "text" },
      { key: "description", label: "Description", type: "textarea" },
      { key: "main_url", label: "Main URL", type: "url" },
      {
        key: "hierarchy_level",
        label: "Hierarchy Level",
        type: "number"
      },
      { key: "full_path", label: "Full Path", type: "text" },
      { key: "directory_path", label: "Directory Path", type: "text" },
      { key: "parent_id", label: "Parent ID", type: "number" },
      { key: "parent_slug", label: "Parent Slug", type: "text" },
      {
        key: "parent_directory_path",
        label: "Parent Directory Path",
        type: "text"
      },
      { key: "category_id", label: "Category ID", type: "number" },
      { key: "category_slug", label: "Category Slug", type: "text" },
      { key: "start_date", label: "Start Date", type: "date" },
      { key: "end_date", label: "End Date", type: "date" }
    ];
    let personId = "";
    let personValues = Object.fromEntries(personEditFields.map((f) => [f.key, ""]));
    let personActive = "";
    let personLoading = false;
    let orgId = "";
    let orgValues = Object.fromEntries(orgEditFields.map((f) => [f.key, ""]));
    let orgActive = "";
    let orgLoading = false;
    const personDisabled = derived(() => !personId.trim());
    const orgDisabled = derived(() => !orgId.trim());
    Hero($$renderer2, {
      title: "Edit Records",
      subtitle: "Resolve a record by ID and push only the fields you want to change via the Flask API."
    });
    $$renderer2.push(`<!----> `);
    Container($$renderer2, {
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="grid svelte-17v3h6h"><form class="form-card svelte-17v3h6h"><div class="form-header svelte-17v3h6h"><h3 class="form-title svelte-17v3h6h">Edit Person</h3> <p class="form-desc svelte-17v3h6h">PUT /api/people — partial update. Blank fields are ignored.</p></div> <div class="fields svelte-17v3h6h"><div class="field full svelte-17v3h6h"><label for="person-id" class="svelte-17v3h6h">Person ID *</label> <input id="person-id" type="number"${attr("value", personId)} required="" class="svelte-17v3h6h"/></div> <!--[-->`);
        const each_array = ensure_array_like(personEditFields);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let field = each_array[$$index];
          $$renderer3.push(`<div${attr_class("field svelte-17v3h6h", void 0, { "full": field.type === "textarea" })}><label${attr("for", `pe-${field.key}`)} class="svelte-17v3h6h">${escape_html(field.label)}</label> `);
          if (field.type === "textarea") {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<textarea${attr("id", `pe-${field.key}`)}${attr("placeholder", field.placeholder)} rows="3" class="svelte-17v3h6h">`);
            const $$body = escape_html(personValues[field.key]);
            if ($$body) {
              $$renderer3.push(`${$$body}`);
            }
            $$renderer3.push(`</textarea>`);
          } else {
            $$renderer3.push("<!--[-1-->");
            $$renderer3.push(`<input${attr("id", `pe-${field.key}`)}${attr("type", field.type)}${attr("value", personValues[field.key])}${attr("placeholder", field.placeholder)} class="svelte-17v3h6h"/>`);
          }
          $$renderer3.push(`<!--]--></div>`);
        }
        $$renderer3.push(`<!--]--> <div class="field svelte-17v3h6h"><label for="person-active" class="svelte-17v3h6h">Active</label> `);
        $$renderer3.select(
          { id: "person-active", value: personActive, class: "" },
          ($$renderer4) => {
            $$renderer4.option({ value: "" }, ($$renderer5) => {
              $$renderer5.push(`— no change —`);
            });
            $$renderer4.option({ value: "true" }, ($$renderer5) => {
              $$renderer5.push(`Active`);
            });
            $$renderer4.option({ value: "false" }, ($$renderer5) => {
              $$renderer5.push(`Inactive`);
            });
          },
          "svelte-17v3h6h"
        );
        $$renderer3.push(`</div></div> `);
        {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--> `);
        Button($$renderer3, {
          variant: "primary",
          icon: "mdi:content-save",
          disabled: personDisabled() || personLoading,
          children: ($$renderer4) => {
            $$renderer4.push(`<!---->${escape_html("Update Person")}`);
          }
        });
        $$renderer3.push(`<!----></form> <form class="form-card svelte-17v3h6h"><div class="form-header svelte-17v3h6h"><h3 class="form-title svelte-17v3h6h">Edit Organization</h3> <p class="form-desc svelte-17v3h6h">PUT /api/organizations — partial update. Blank fields are ignored.</p></div> <div class="fields svelte-17v3h6h"><div class="field full svelte-17v3h6h"><label for="org-id" class="svelte-17v3h6h">Organization ID *</label> <input id="org-id" type="number"${attr("value", orgId)} required="" class="svelte-17v3h6h"/></div> <!--[-->`);
        const each_array_1 = ensure_array_like(orgEditFields);
        for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
          let field = each_array_1[$$index_1];
          $$renderer3.push(`<div${attr_class("field svelte-17v3h6h", void 0, { "full": field.type === "textarea" })}><label${attr("for", `oe-${field.key}`)} class="svelte-17v3h6h">${escape_html(field.label)}</label> `);
          if (field.type === "textarea") {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<textarea${attr("id", `oe-${field.key}`)}${attr("placeholder", field.placeholder)} rows="3" class="svelte-17v3h6h">`);
            const $$body_1 = escape_html(orgValues[field.key]);
            if ($$body_1) {
              $$renderer3.push(`${$$body_1}`);
            }
            $$renderer3.push(`</textarea>`);
          } else {
            $$renderer3.push("<!--[-1-->");
            $$renderer3.push(`<input${attr("id", `oe-${field.key}`)}${attr("type", field.type)}${attr("value", orgValues[field.key])}${attr("placeholder", field.placeholder)} class="svelte-17v3h6h"/>`);
          }
          $$renderer3.push(`<!--]--></div>`);
        }
        $$renderer3.push(`<!--]--> <div class="field svelte-17v3h6h"><label for="org-active" class="svelte-17v3h6h">Active</label> `);
        $$renderer3.select(
          { id: "org-active", value: orgActive, class: "" },
          ($$renderer4) => {
            $$renderer4.option({ value: "" }, ($$renderer5) => {
              $$renderer5.push(`— no change —`);
            });
            $$renderer4.option({ value: "true" }, ($$renderer5) => {
              $$renderer5.push(`Active`);
            });
            $$renderer4.option({ value: "false" }, ($$renderer5) => {
              $$renderer5.push(`Inactive`);
            });
          },
          "svelte-17v3h6h"
        );
        $$renderer3.push(`</div></div> `);
        {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--> `);
        Button($$renderer3, {
          variant: "primary",
          icon: "mdi:content-save",
          disabled: orgDisabled() || orgLoading,
          children: ($$renderer4) => {
            $$renderer4.push(`<!---->${escape_html("Update Organization")}`);
          }
        });
        $$renderer3.push(`<!----></form></div>`);
      }
    });
    $$renderer2.push(`<!---->`);
  });
}
export {
  _page as default
};
