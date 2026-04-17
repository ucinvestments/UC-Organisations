<script lang="ts">
  import Icon from "@iconify/svelte";
  import Hero from "$lib/components/Hero.svelte";
  import Container from "$lib/components/Container.svelte";
  import Button from "$lib/components/Button.svelte";
  import { ApiError, putJson } from "$lib/api";

  type Status = { type: "success" | "error"; message: string } | null;
  type Tri = "" | "true" | "false";

  const personEditFields: Array<{ key: string; label: string; type: string; placeholder?: string }> = [
    { key: "first_name", label: "First Name", type: "text", placeholder: "Jane" },
    { key: "last_name", label: "Last Name", type: "text", placeholder: "Doe" },
    { key: "middle_name", label: "Middle Name", type: "text", placeholder: "A." },
    { key: "preferred_name", label: "Preferred Name", type: "text" },
    { key: "bio", label: "Bio", type: "textarea" },
    { key: "profile_url", label: "Profile URL", type: "url" },
    { key: "photo_url", label: "Photo URL", type: "url" },
    { key: "social_platform", label: "Social Platform", type: "text" },
    { key: "social_handle", label: "Social Handle", type: "text" },
    { key: "social_url", label: "Social URL", type: "url" },
    { key: "contact_type", label: "Contact Type", type: "text" },
    { key: "contact_value", label: "Contact Value", type: "text" },
    { key: "contact_label", label: "Contact Label", type: "text" },
  ];

  const orgEditFields: Array<{ key: string; label: string; type: string; placeholder?: string }> = [
    { key: "name", label: "Name", type: "text" },
    { key: "slug", label: "Slug", type: "text" },
    { key: "description", label: "Description", type: "textarea" },
    { key: "main_url", label: "Main URL", type: "url" },
    { key: "hierarchy_level", label: "Hierarchy Level", type: "number" },
    { key: "full_path", label: "Full Path", type: "text" },
    { key: "directory_path", label: "Directory Path", type: "text" },
    { key: "parent_id", label: "Parent ID", type: "number" },
    { key: "parent_slug", label: "Parent Slug", type: "text" },
    { key: "parent_directory_path", label: "Parent Directory Path", type: "text" },
    { key: "category_id", label: "Category ID", type: "number" },
    { key: "category_slug", label: "Category Slug", type: "text" },
    { key: "start_date", label: "Start Date", type: "date" },
    { key: "end_date", label: "End Date", type: "date" },
  ];

  let personId = $state("");
  let personValues = $state<Record<string, string>>(
    Object.fromEntries(personEditFields.map((f) => [f.key, ""])),
  );
  let personActive = $state<Tri>("");
  let personStatus = $state<Status>(null);
  let personLoading = $state(false);

  let orgId = $state("");
  let orgValues = $state<Record<string, string>>(
    Object.fromEntries(orgEditFields.map((f) => [f.key, ""])),
  );
  let orgActive = $state<Tri>("");
  let orgStatus = $state<Status>(null);
  let orgLoading = $state(false);

  const personDisabled = $derived(!personId.trim());
  const orgDisabled = $derived(!orgId.trim());

  function parseNum(v: string): number | undefined {
    if (!v.trim()) return undefined;
    const n = Number(v);
    return Number.isNaN(n) ? undefined : n;
  }

  function buildPersonPayload() {
    const id = parseNum(personId);
    if (typeof id !== "number") throw new Error("A valid person ID is required.");

    const updates: Record<string, unknown> = {};
    const textKeys = [
      "first_name",
      "last_name",
      "middle_name",
      "preferred_name",
      "bio",
      "profile_url",
      "photo_url",
    ];
    for (const key of textKeys) {
      const v = personValues[key]?.trim();
      if (v) updates[key] = v;
    }
    if (personActive) updates.is_active = personActive === "true";

    const payload: Record<string, unknown> = { id, updates };

    if (personValues.social_platform.trim() && personValues.social_url.trim()) {
      payload.social_media = [
        {
          platform: personValues.social_platform.trim(),
          profile_url: personValues.social_url.trim(),
          handle: personValues.social_handle.trim() || undefined,
        },
      ];
    }

    if (personValues.contact_type.trim() && personValues.contact_value.trim()) {
      payload.contact_info = [
        {
          contact_type: personValues.contact_type.trim(),
          contact_value: personValues.contact_value.trim(),
          contact_label: personValues.contact_label.trim() || undefined,
        },
      ];
    }

    const hasUpdates =
      Object.keys(updates).length > 0 || payload.social_media || payload.contact_info;
    if (!hasUpdates) throw new Error("Provide at least one field to update.");

    return payload;
  }

  function buildOrgPayload() {
    const id = parseNum(orgId);
    if (typeof id !== "number") throw new Error("A valid organization ID is required.");

    const updates: Record<string, unknown> = {};
    const textKeys = [
      "name",
      "slug",
      "description",
      "main_url",
      "full_path",
      "directory_path",
      "parent_slug",
      "parent_directory_path",
      "category_slug",
      "start_date",
      "end_date",
    ];
    for (const key of textKeys) {
      const v = orgValues[key]?.trim();
      if (v) updates[key] = v;
    }
    for (const key of ["hierarchy_level", "parent_id", "category_id"]) {
      const n = parseNum(orgValues[key] ?? "");
      if (typeof n === "number") updates[key] = n;
    }
    if (orgActive) updates.is_active = orgActive === "true";

    if (!Object.keys(updates).length)
      throw new Error("Provide at least one field to update.");

    return { id, updates };
  }

  async function submitPerson(e: Event) {
    e.preventDefault();
    personStatus = null;
    personLoading = true;
    try {
      const payload = buildPersonPayload();
      const updated = await putJson<typeof payload, { id: number; first_name: string; last_name: string }>(
        "/api/people",
        payload,
      );
      personStatus = {
        type: "success",
        message: `Updated ${updated.first_name} ${updated.last_name} (ID ${updated.id}).`,
      };
    } catch (err) {
      personStatus = {
        type: "error",
        message: err instanceof ApiError || err instanceof Error ? err.message : "Unable to update person.",
      };
    } finally {
      personLoading = false;
    }
  }

  async function submitOrg(e: Event) {
    e.preventDefault();
    orgStatus = null;
    orgLoading = true;
    try {
      const payload = buildOrgPayload();
      const updated = await putJson<typeof payload, { id: number; name: string; slug: string }>(
        "/api/organizations",
        payload,
      );
      orgStatus = {
        type: "success",
        message: `Updated ${updated.name} (ID ${updated.id}, slug ${updated.slug}).`,
      };
    } catch (err) {
      orgStatus = {
        type: "error",
        message: err instanceof ApiError || err instanceof Error ? err.message : "Unable to update organization.",
      };
    } finally {
      orgLoading = false;
    }
  }
</script>

<Hero
  title="Edit Records"
  subtitle="Resolve a record by ID and push only the fields you want to change via the Flask API."
/>

<Container>
  <div class="grid">
    <form class="form-card" onsubmit={submitPerson}>
      <div class="form-header">
        <h3 class="form-title">Edit Person</h3>
        <p class="form-desc">PUT /api/people — partial update. Blank fields are ignored.</p>
      </div>

      <div class="fields">
        <div class="field full">
          <label for="person-id">Person ID *</label>
          <input id="person-id" type="number" bind:value={personId} required />
        </div>
        {#each personEditFields as field (field.key)}
          <div class="field" class:full={field.type === "textarea"}>
            <label for={`pe-${field.key}`}>{field.label}</label>
            {#if field.type === "textarea"}
              <textarea
                id={`pe-${field.key}`}
                bind:value={personValues[field.key]}
                placeholder={field.placeholder}
                rows="3"
              ></textarea>
            {:else}
              <input
                id={`pe-${field.key}`}
                type={field.type}
                bind:value={personValues[field.key]}
                placeholder={field.placeholder}
              />
            {/if}
          </div>
        {/each}
        <div class="field">
          <label for="person-active">Active</label>
          <select id="person-active" bind:value={personActive}>
            <option value="">— no change —</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>

      {#if personStatus}
        <div class="status" class:success={personStatus.type === "success"} class:error={personStatus.type === "error"}>
          <Icon icon={personStatus.type === "success" ? "mdi:check-circle" : "mdi:alert-circle"} />
          {personStatus.message}
        </div>
      {/if}

      <Button variant="primary" icon="mdi:content-save" disabled={personDisabled || personLoading}>
        {personLoading ? "Updating…" : "Update Person"}
      </Button>
    </form>

    <form class="form-card" onsubmit={submitOrg}>
      <div class="form-header">
        <h3 class="form-title">Edit Organization</h3>
        <p class="form-desc">PUT /api/organizations — partial update. Blank fields are ignored.</p>
      </div>

      <div class="fields">
        <div class="field full">
          <label for="org-id">Organization ID *</label>
          <input id="org-id" type="number" bind:value={orgId} required />
        </div>
        {#each orgEditFields as field (field.key)}
          <div class="field" class:full={field.type === "textarea"}>
            <label for={`oe-${field.key}`}>{field.label}</label>
            {#if field.type === "textarea"}
              <textarea
                id={`oe-${field.key}`}
                bind:value={orgValues[field.key]}
                placeholder={field.placeholder}
                rows="3"
              ></textarea>
            {:else}
              <input
                id={`oe-${field.key}`}
                type={field.type}
                bind:value={orgValues[field.key]}
                placeholder={field.placeholder}
              />
            {/if}
          </div>
        {/each}
        <div class="field">
          <label for="org-active">Active</label>
          <select id="org-active" bind:value={orgActive}>
            <option value="">— no change —</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>

      {#if orgStatus}
        <div class="status" class:success={orgStatus.type === "success"} class:error={orgStatus.type === "error"}>
          <Icon icon={orgStatus.type === "success" ? "mdi:check-circle" : "mdi:alert-circle"} />
          {orgStatus.message}
        </div>
      {/if}

      <Button variant="primary" icon="mdi:content-save" disabled={orgDisabled || orgLoading}>
        {orgLoading ? "Updating…" : "Update Organization"}
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
  .field textarea,
  .field select {
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
  .field textarea:focus,
  .field select:focus {
    outline: none;
    border-color: var(--founder);
    box-shadow: 0 0 0 3px rgba(59, 126, 161, 0.15);
  }

  .field textarea {
    resize: vertical;
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
