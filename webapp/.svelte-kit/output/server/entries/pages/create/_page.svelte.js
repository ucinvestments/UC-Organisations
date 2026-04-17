import { b as ensure_array_like, a as attr_class, c as attr, e as escape_html, f as derived } from "../../../chunks/renderer.js";
import "../../../chunks/Icon.js";
import { H as Hero, C as Container } from "../../../chunks/Container.js";
import { B as Button } from "../../../chunks/api.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const personFields = [
      {
        key: "first_name",
        label: "First Name *",
        type: "text",
        required: true,
        placeholder: "Jane"
      },
      {
        key: "last_name",
        label: "Last Name *",
        type: "text",
        required: true,
        placeholder: "Doe"
      },
      {
        key: "middle_name",
        label: "Middle Name",
        type: "text",
        placeholder: "A."
      },
      {
        key: "preferred_name",
        label: "Preferred Name",
        type: "text",
        placeholder: "Janey"
      },
      {
        key: "bio",
        label: "Bio",
        type: "textarea",
        placeholder: "Short biography…"
      },
      {
        key: "profile_url",
        label: "Profile URL",
        type: "url",
        placeholder: "https://…"
      },
      {
        key: "photo_url",
        label: "Photo URL",
        type: "url",
        placeholder: "https://…"
      },
      {
        key: "social_platform",
        label: "Social Platform",
        type: "text",
        placeholder: "LinkedIn"
      },
      {
        key: "social_handle",
        label: "Social Handle",
        type: "text",
        placeholder: "@jane"
      },
      {
        key: "social_url",
        label: "Social URL",
        type: "url",
        placeholder: "https://…"
      },
      {
        key: "contact_type",
        label: "Contact Type",
        type: "text",
        placeholder: "email"
      },
      {
        key: "contact_value",
        label: "Contact Value",
        type: "text",
        placeholder: "jane@example.com"
      },
      {
        key: "contact_label",
        label: "Contact Label",
        type: "text",
        placeholder: "Work"
      }
    ];
    const orgFields = [
      {
        key: "name",
        label: "Name *",
        type: "text",
        required: true,
        placeholder: "Investment Management"
      },
      {
        key: "slug",
        label: "Slug",
        type: "text",
        placeholder: "investment-management"
      },
      {
        key: "description",
        label: "Description",
        type: "textarea",
        placeholder: "What this org does…"
      },
      {
        key: "main_url",
        label: "Main URL",
        type: "url",
        placeholder: "https://…"
      },
      {
        key: "hierarchy_level",
        label: "Hierarchy Level",
        type: "number",
        placeholder: "2"
      },
      {
        key: "full_path",
        label: "Full Path",
        type: "text",
        placeholder: "/root/department"
      },
      {
        key: "directory_path",
        label: "Directory Path",
        type: "text",
        placeholder: "investments/management"
      },
      {
        key: "parent_id",
        label: "Parent ID",
        type: "number",
        placeholder: "12"
      },
      {
        key: "parent_slug",
        label: "Parent Slug",
        type: "text",
        placeholder: "parent-org"
      },
      {
        key: "category_id",
        label: "Category ID",
        type: "number",
        placeholder: "3"
      },
      {
        key: "category_slug",
        label: "Category Slug",
        type: "text",
        placeholder: "research"
      },
      { key: "start_date", label: "Start Date", type: "date" },
      { key: "end_date", label: "End Date", type: "date" }
    ];
    let personValues = Object.fromEntries(personFields.map((f) => [f.key, ""]));
    let personActive = true;
    let personLoading = false;
    let orgValues = Object.fromEntries(orgFields.map((f) => [f.key, ""]));
    let orgActive = true;
    let orgLoading = false;
    const personDisabled = derived(() => !personValues.first_name.trim() || !personValues.last_name.trim());
    const orgDisabled = derived(() => !orgValues.name.trim());
    Hero($$renderer2, {
      title: "Create Records",
      subtitle: "Push new people and organization profiles into the canonical database via the Flask API."
    });
    $$renderer2.push(`<!----> `);
    Container($$renderer2, {
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="grid svelte-jztt4t"><form class="form-card svelte-jztt4t"><div class="form-header svelte-jztt4t"><h3 class="form-title svelte-jztt4t">Create Person</h3> <p class="form-desc svelte-jztt4t">POST /api/people — core profile data plus optional contact metadata.</p></div> <div class="fields svelte-jztt4t"><!--[-->`);
        const each_array = ensure_array_like(personFields);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let field = each_array[$$index];
          $$renderer3.push(`<div${attr_class("field svelte-jztt4t", void 0, { "full": field.type === "textarea" })}><label${attr("for", `p-${field.key}`)} class="svelte-jztt4t">${escape_html(field.label)}</label> `);
          if (field.type === "textarea") {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<textarea${attr("id", `p-${field.key}`)}${attr("placeholder", field.placeholder)} rows="3" class="svelte-jztt4t">`);
            const $$body = escape_html(personValues[field.key]);
            if ($$body) {
              $$renderer3.push(`${$$body}`);
            }
            $$renderer3.push(`</textarea>`);
          } else {
            $$renderer3.push("<!--[-1-->");
            $$renderer3.push(`<input${attr("id", `p-${field.key}`)}${attr("type", field.type)}${attr("value", personValues[field.key])}${attr("placeholder", field.placeholder)}${attr("required", field.required, true)} class="svelte-jztt4t"/>`);
          }
          $$renderer3.push(`<!--]--></div>`);
        }
        $$renderer3.push(`<!--]--> <label class="checkbox svelte-jztt4t"><input type="checkbox"${attr("checked", personActive, true)}/> Active</label></div> `);
        {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--> `);
        Button($$renderer3, {
          variant: "primary",
          icon: "mdi:plus",
          disabled: personDisabled() || personLoading,
          children: ($$renderer4) => {
            $$renderer4.push(`<!---->${escape_html("Create Person")}`);
          }
        });
        $$renderer3.push(`<!----></form> <form class="form-card svelte-jztt4t"><div class="form-header svelte-jztt4t"><h3 class="form-title svelte-jztt4t">Create Organization</h3> <p class="form-desc svelte-jztt4t">POST /api/organizations — org metadata and hierarchy placement.</p></div> <div class="fields svelte-jztt4t"><!--[-->`);
        const each_array_1 = ensure_array_like(orgFields);
        for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
          let field = each_array_1[$$index_1];
          $$renderer3.push(`<div${attr_class("field svelte-jztt4t", void 0, { "full": field.type === "textarea" })}><label${attr("for", `o-${field.key}`)} class="svelte-jztt4t">${escape_html(field.label)}</label> `);
          if (field.type === "textarea") {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<textarea${attr("id", `o-${field.key}`)}${attr("placeholder", field.placeholder)} rows="3" class="svelte-jztt4t">`);
            const $$body_1 = escape_html(orgValues[field.key]);
            if ($$body_1) {
              $$renderer3.push(`${$$body_1}`);
            }
            $$renderer3.push(`</textarea>`);
          } else {
            $$renderer3.push("<!--[-1-->");
            $$renderer3.push(`<input${attr("id", `o-${field.key}`)}${attr("type", field.type)}${attr("value", orgValues[field.key])}${attr("placeholder", field.placeholder)}${attr("required", field.required, true)} class="svelte-jztt4t"/>`);
          }
          $$renderer3.push(`<!--]--></div>`);
        }
        $$renderer3.push(`<!--]--> <label class="checkbox svelte-jztt4t"><input type="checkbox"${attr("checked", orgActive, true)}/> Active</label></div> `);
        {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--> `);
        Button($$renderer3, {
          variant: "primary",
          icon: "mdi:plus",
          disabled: orgDisabled() || orgLoading,
          children: ($$renderer4) => {
            $$renderer4.push(`<!---->${escape_html("Create Organization")}`);
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
