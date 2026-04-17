<script lang="ts">
  import Icon from "@iconify/svelte";
  import Hero from "$lib/components/Hero.svelte";
  import Container from "$lib/components/Container.svelte";
  import Button from "$lib/components/Button.svelte";
  import { ApiError, postJson } from "$lib/api";

  type Status = { type: "success" | "error"; message: string } | null;

  const personFields = [
    { key: "first_name", label: "First Name *", type: "text", required: true, placeholder: "Jane" },
    { key: "last_name", label: "Last Name *", type: "text", required: true, placeholder: "Doe" },
    { key: "middle_name", label: "Middle Name", type: "text", placeholder: "A." },
    { key: "preferred_name", label: "Preferred Name", type: "text", placeholder: "Janey" },
    { key: "bio", label: "Bio", type: "textarea", placeholder: "Short biography…" },
    { key: "profile_url", label: "Profile URL", type: "url", placeholder: "https://…" },
    { key: "photo_url", label: "Photo URL", type: "url", placeholder: "https://…" },
    { key: "social_platform", label: "Social Platform", type: "text", placeholder: "LinkedIn" },
    { key: "social_handle", label: "Social Handle", type: "text", placeholder: "@jane" },
    { key: "social_url", label: "Social URL", type: "url", placeholder: "https://…" },
    { key: "contact_type", label: "Contact Type", type: "text", placeholder: "email" },
    { key: "contact_value", label: "Contact Value", type: "text", placeholder: "jane@example.com" },
    { key: "contact_label", label: "Contact Label", type: "text", placeholder: "Work" },
  ];

  const orgFields = [
    { key: "name", label: "Name *", type: "text", required: true, placeholder: "Investment Management" },
    { key: "slug", label: "Slug", type: "text", placeholder: "investment-management" },
    { key: "description", label: "Description", type: "textarea", placeholder: "What this org does…" },
    { key: "main_url", label: "Main URL", type: "url", placeholder: "https://…" },
    { key: "hierarchy_level", label: "Hierarchy Level", type: "number", placeholder: "2" },
    { key: "full_path", label: "Full Path", type: "text", placeholder: "/root/department" },
    { key: "directory_path", label: "Directory Path", type: "text", placeholder: "investments/management" },
    { key: "parent_id", label: "Parent ID", type: "number", placeholder: "12" },
    { key: "parent_slug", label: "Parent Slug", type: "text", placeholder: "parent-org" },
    { key: "category_id", label: "Category ID", type: "number", placeholder: "3" },
    { key: "category_slug", label: "Category Slug", type: "text", placeholder: "research" },
    { key: "start_date", label: "Start Date", type: "date" },
    { key: "end_date", label: "End Date", type: "date" },
  ];

  let personValues = $state<Record<string, string>>(
    Object.fromEntries(personFields.map((f) => [f.key, ""])),
  );
  let personActive = $state(true);
  let personStatus = $state<Status>(null);
  let personLoading = $state(false);

  let orgValues = $state<Record<string, string>>(
    Object.fromEntries(orgFields.map((f) => [f.key, ""])),
  );
  let orgActive = $state(true);
  let orgStatus = $state<Status>(null);
  let orgLoading = $state(false);

  const personDisabled = $derived(!personValues.first_name.trim() || !personValues.last_name.trim());
  const orgDisabled = $derived(!orgValues.name.trim());

  function parseNum(v: string): number | undefined {
    if (!v.trim()) return undefined;
    const n = Number(v);
    return Number.isNaN(n) ? undefined : n;
  }

  function buildPersonPayload() {
    const payload: Record<string, unknown> = {
      first_name: personValues.first_name.trim(),
      last_name: personValues.last_name.trim(),
      is_active: personActive,
    };
    for (const key of ["middle_name", "preferred_name", "bio", "profile_url", "photo_url"]) {
      const v = personValues[key]?.trim();
      if (v) payload[key] = v;
    }
    if (personValues.social_platform && personValues.social_url) {
      payload.social_media = [
        {
          platform: personValues.social_platform.trim(),
          handle: personValues.social_handle?.trim() || undefined,
          profile_url: personValues.social_url.trim(),
        },
      ];
    }
    if (personValues.contact_type && personValues.contact_value) {
      payload.contact_info = [
        {
          contact_type: personValues.contact_type.trim(),
          contact_value: personValues.contact_value.trim(),
          contact_label: personValues.contact_label?.trim() || undefined,
        },
      ];
    }
    return payload;
  }

  function buildOrgPayload() {
    const payload: Record<string, unknown> = {
      name: orgValues.name.trim(),
      is_active: orgActive,
    };
    for (const key of [
      "slug",
      "description",
      "main_url",
      "full_path",
      "directory_path",
      "parent_slug",
      "category_slug",
      "start_date",
      "end_date",
    ]) {
      const v = orgValues[key]?.trim();
      if (v) payload[key] = v;
    }
    for (const key of ["hierarchy_level", "parent_id", "category_id"]) {
      const n = parseNum(orgValues[key] ?? "");
      if (typeof n === "number") payload[key] = n;
    }
    return payload;
  }

  async function submitPerson(e: Event) {
    e.preventDefault();
    if (personDisabled) {
      personStatus = { type: "error", message: "First and last name are required." };
      return;
    }
    personStatus = null;
    personLoading = true;
    try {
      const created = await postJson<Record<string, unknown>, { id: number; first_name: string; last_name: string }>(
        "/api/people",
        buildPersonPayload(),
      );
      personStatus = {
        type: "success",
        message: `Created ${created.first_name} ${created.last_name} (ID ${created.id}).`,
      };
      personValues = Object.fromEntries(personFields.map((f) => [f.key, ""]));
      personActive = true;
    } catch (err) {
      personStatus = {
        type: "error",
        message: err instanceof ApiError ? err.message : "Unable to create person.",
      };
    } finally {
      personLoading = false;
    }
  }

  async function submitOrg(e: Event) {
    e.preventDefault();
    if (orgDisabled) {
      orgStatus = { type: "error", message: "Organization name is required." };
      return;
    }
    orgStatus = null;
    orgLoading = true;
    try {
      const created = await postJson<Record<string, unknown>, { id: number; name: string; slug: string }>(
        "/api/organizations",
        buildOrgPayload(),
      );
      orgStatus = {
        type: "success",
        message: `Created ${created.name} (ID ${created.id}, slug ${created.slug}).`,
      };
      orgValues = Object.fromEntries(orgFields.map((f) => [f.key, ""]));
      orgActive = true;
    } catch (err) {
      orgStatus = {
        type: "error",
        message: err instanceof ApiError ? err.message : "Unable to create organization.",
      };
    } finally {
      orgLoading = false;
    }
  }
</script>

<Hero
  title="Create Records"
  subtitle="Push new people and organization profiles into the canonical database via the Flask API."
/>

<Container>
  <div class="grid">
    <form class="form-card" onsubmit={submitPerson}>
      <div class="form-header">
        <h3 class="form-title">Create Person</h3>
        <p class="form-desc">POST /api/people — core profile data plus optional contact metadata.</p>
      </div>

      <div class="fields">
        {#each personFields as field (field.key)}
          <div class="field" class:full={field.type === "textarea"}>
            <label for={`p-${field.key}`}>{field.label}</label>
            {#if field.type === "textarea"}
              <textarea
                id={`p-${field.key}`}
                bind:value={personValues[field.key]}
                placeholder={field.placeholder}
                rows="3"
              ></textarea>
            {:else}
              <input
                id={`p-${field.key}`}
                type={field.type}
                bind:value={personValues[field.key]}
                placeholder={field.placeholder}
                required={field.required}
              />
            {/if}
          </div>
        {/each}
        <label class="checkbox">
          <input type="checkbox" bind:checked={personActive} />
          Active
        </label>
      </div>

      {#if personStatus}
        <div class="status" class:success={personStatus.type === "success"} class:error={personStatus.type === "error"}>
          <Icon icon={personStatus.type === "success" ? "mdi:check-circle" : "mdi:alert-circle"} />
          {personStatus.message}
        </div>
      {/if}

      <Button variant="primary" icon="mdi:plus" disabled={personDisabled || personLoading}>
        {personLoading ? "Creating…" : "Create Person"}
      </Button>
    </form>

    <form class="form-card" onsubmit={submitOrg}>
      <div class="form-header">
        <h3 class="form-title">Create Organization</h3>
        <p class="form-desc">POST /api/organizations — org metadata and hierarchy placement.</p>
      </div>

      <div class="fields">
        {#each orgFields as field (field.key)}
          <div class="field" class:full={field.type === "textarea"}>
            <label for={`o-${field.key}`}>{field.label}</label>
            {#if field.type === "textarea"}
              <textarea
                id={`o-${field.key}`}
                bind:value={orgValues[field.key]}
                placeholder={field.placeholder}
                rows="3"
              ></textarea>
            {:else}
              <input
                id={`o-${field.key}`}
                type={field.type}
                bind:value={orgValues[field.key]}
                placeholder={field.placeholder}
                required={field.required}
              />
            {/if}
          </div>
        {/each}
        <label class="checkbox">
          <input type="checkbox" bind:checked={orgActive} />
          Active
        </label>
      </div>

      {#if orgStatus}
        <div class="status" class:success={orgStatus.type === "success"} class:error={orgStatus.type === "error"}>
          <Icon icon={orgStatus.type === "success" ? "mdi:check-circle" : "mdi:alert-circle"} />
          {orgStatus.message}
        </div>
      {/if}

      <Button variant="primary" icon="mdi:plus" disabled={orgDisabled || orgLoading}>
        {orgLoading ? "Creating…" : "Create Organization"}
      </Button>
    </form>
  </div>
</Container>

<style>
  .grid {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  }

  .form-card {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid var(--border);
    border-radius: 1.5rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    box-shadow: var(--shadow-md);
  }

  .form-header h3 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.25rem;
    color: var(--pri);
    margin: 0 0 0.25rem 0;
  }

  .form-desc {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0;
  }

  .fields {
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr 1fr;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
  }

  .field.full {
    grid-column: 1 / -1;
  }

  .field label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: var(--pri);
  }

  .field input,
  .field textarea {
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 0.5rem 0.75rem;
    font-family: inherit;
    font-size: 0.925rem;
    background: white;
    color: var(--text-primary);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .field input:focus,
  .field textarea:focus {
    outline: none;
    border-color: var(--founder);
    box-shadow: 0 0 0 3px rgba(59, 126, 161, 0.15);
  }

  .field textarea {
    resize: vertical;
  }

  .checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.925rem;
    color: var(--text-primary);
    grid-column: 1 / -1;
    cursor: pointer;
  }

  .status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    font-size: 0.875rem;
    border: 1px solid;
  }

  .status.success {
    border-color: var(--sather-gate);
    background: rgba(185, 211, 182, 0.2);
    color: var(--south-hall);
  }

  .status.error {
    border-color: var(--rose-garden);
    background: rgba(238, 31, 96, 0.08);
    color: var(--rose-garden);
  }

  @media (max-width: 640px) {
    .fields {
      grid-template-columns: 1fr;
    }
  }
</style>
