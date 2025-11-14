import { FormEvent, ReactNode, useMemo, useState } from 'react';
import { Button } from '@/src/design-system';
import { AlertCircle, CheckCircle, Save } from '@/src/design-system/icons';
import { ApiError, putJson } from '@/src/lib/api';

type FormStatus = {
  type: 'success' | 'error';
  message: string;
};

type BooleanSelect = 'unchanged' | 'true' | 'false';

type PersonEditValues = {
  person_id: string;
  first_name: string;
  last_name: string;
  middle_name: string;
  preferred_name: string;
  bio: string;
  profile_url: string;
  photo_url: string;
  is_active: BooleanSelect;
  social_platform: string;
  social_handle: string;
  social_url: string;
  contact_type: string;
  contact_value: string;
  contact_label: string;
};

type OrganizationEditValues = {
  organization_id: string;
  name: string;
  slug: string;
  description: string;
  main_url: string;
  hierarchy_level: string;
  full_path: string;
  directory_path: string;
  parent_id: string;
  parent_slug: string;
  parent_directory_path: string;
  category_id: string;
  category_slug: string;
  start_date: string;
  end_date: string;
  is_active: BooleanSelect;
};

const inputBase =
  'mt-1 block w-full rounded-xl border border-berkeley-blue/20 bg-white/80 px-3 py-2 text-gray-900 shadow-sm focus:border-berkeley-blue focus:ring-2 focus:ring-berkeley-blue/30';
const labelBase = 'text-sm font-semibold text-berkeley-blue';

const initialPersonValues: PersonEditValues = {
  person_id: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  preferred_name: '',
  bio: '',
  profile_url: '',
  photo_url: '',
  is_active: 'unchanged',
  social_platform: '',
  social_handle: '',
  social_url: '',
  contact_type: '',
  contact_value: '',
  contact_label: '',
};

const initialOrganizationValues: OrganizationEditValues = {
  organization_id: '',
  name: '',
  slug: '',
  description: '',
  main_url: '',
  hierarchy_level: '',
  full_path: '',
  directory_path: '',
  parent_id: '',
  parent_slug: '',
  parent_directory_path: '',
  category_id: '',
  category_slug: '',
  start_date: '',
  end_date: '',
  is_active: 'unchanged',
};

const parseNumberField = (value: string) => {
  if (!value.trim()) {
    return undefined;
  }
  const parsed = Number(value);
  return Number.isNaN(parsed) ? undefined : parsed;
};

const isBooleanSelected = (value: BooleanSelect) => value !== 'unchanged';

const StatusMessage = ({ status }: { status: FormStatus | null }) => {
  if (!status) {
    return null;
  }

  const isSuccess = status.type === 'success';
  const baseClasses = isSuccess
    ? 'border-west-gate/40 bg-west-gate/10 text-west-gate'
    : 'border-sather-gate/40 bg-sather-gate/10 text-sather-gate';

  const Icon = isSuccess ? CheckCircle : AlertCircle;

  return (
    <div className={`flex items-center gap-2 rounded-xl border px-3 py-2 text-sm ${baseClasses}`}>
      <Icon size={18} />
      <span>{status.message}</span>
    </div>
  );
};

type FormCardProps = {
  title: string;
  description: string;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  children: ReactNode;
  actions: ReactNode;
  status: FormStatus | null;
};

const FormCard = ({ title, description, onSubmit, children, actions, status }: FormCardProps) => (
  <form
    onSubmit={onSubmit}
    className="flex flex-col gap-5 rounded-2xl border-2 border-berkeley-blue/10 bg-white/90 p-6 shadow-md"
  >
    <div>
      <h3 className="text-xl font-semibold text-berkeley-blue">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>

    {children}

    <div className="flex flex-col gap-4">
      <StatusMessage status={status} />
      {actions}
    </div>
  </form>
);

const buildPersonUpdatePayload = (values: PersonEditValues) => {
  const id = parseNumberField(values.person_id);
  if (typeof id !== 'number') {
    throw new Error('A valid person ID is required.');
  }

  const updates: Record<string, unknown> = {};
  const optionalFields: Array<keyof PersonEditValues> = [
    'first_name',
    'last_name',
    'middle_name',
    'preferred_name',
    'bio',
    'profile_url',
    'photo_url',
  ];

  optionalFields.forEach((field) => {
    const value = values[field];
    if (typeof value === 'string' && value.trim()) {
      updates[field] = value.trim();
    }
  });

  if (isBooleanSelected(values.is_active)) {
    updates.is_active = values.is_active === 'true';
  }

  const payload: Record<string, unknown> = {
    id,
    updates,
  };

  if (values.social_platform.trim() && values.social_url.trim()) {
    payload.social_media = [
      {
        platform: values.social_platform.trim(),
        profile_url: values.social_url.trim(),
        handle: values.social_handle.trim() || undefined,
      },
    ];
  }

  if (values.contact_type.trim() && values.contact_value.trim()) {
    payload.contact_info = [
      {
        contact_type: values.contact_type.trim(),
        contact_value: values.contact_value.trim(),
        contact_label: values.contact_label.trim() || undefined,
      },
    ];
  }

  const hasUpdates =
    Object.keys(updates).length > 0 || payload.social_media || payload.contact_info;
  if (!hasUpdates) {
    throw new Error('Provide at least one field to update.');
  }

  return payload;
};

const buildOrganizationUpdatePayload = (values: OrganizationEditValues) => {
  const id = parseNumberField(values.organization_id);
  if (typeof id !== 'number') {
    throw new Error('A valid organization ID is required.');
  }

  const updates: Record<string, unknown> = {};
  const optionalFields: Array<keyof OrganizationEditValues> = [
    'name',
    'slug',
    'description',
    'main_url',
    'full_path',
    'directory_path',
    'parent_slug',
    'parent_directory_path',
    'category_slug',
    'start_date',
    'end_date',
  ];

  optionalFields.forEach((field) => {
    const value = values[field];
    if (typeof value === 'string' && value.trim()) {
      updates[field] = value.trim();
    }
  });

  const numericFieldMap: Record<string, number | undefined> = {
    hierarchy_level: parseNumberField(values.hierarchy_level),
    parent_id: parseNumberField(values.parent_id),
    category_id: parseNumberField(values.category_id),
  };

  Object.entries(numericFieldMap).forEach(([key, value]) => {
    if (typeof value === 'number') {
      updates[key] = value;
    }
  });

  if (isBooleanSelected(values.is_active)) {
    updates.is_active = values.is_active === 'true';
  }

  if (!Object.keys(updates).length) {
    throw new Error('Provide at least one field to update.');
  }

  return {
    id,
    updates,
  };
};

export const EditEntitiesPanel = () => {
  const [personValues, setPersonValues] = useState<PersonEditValues>(initialPersonValues);
  const [organizationValues, setOrganizationValues] =
    useState<OrganizationEditValues>(initialOrganizationValues);

  const [personStatus, setPersonStatus] = useState<FormStatus | null>(null);
  const [orgStatus, setOrgStatus] = useState<FormStatus | null>(null);

  const [personLoading, setPersonLoading] = useState(false);
  const [orgLoading, setOrgLoading] = useState(false);

  const personDisabled = useMemo(() => !personValues.person_id.trim(), [personValues.person_id]);
  const orgDisabled = useMemo(
    () => !organizationValues.organization_id.trim(),
    [organizationValues.organization_id],
  );

  const handlePersonSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (personDisabled) {
      setPersonStatus({ type: 'error', message: 'Person ID is required.' });
      return;
    }

    setPersonStatus(null);
    setPersonLoading(true);
    try {
      const payload = buildPersonUpdatePayload(personValues);
      const updated = await putJson<typeof payload, { id: number; first_name: string; last_name: string }>(
        '/api/people',
        payload,
      );
      setPersonStatus({
        type: 'success',
        message: `Updated ${updated.first_name} ${updated.last_name} (ID ${updated.id}).`,
      });
    } catch (error) {
      const message =
        error instanceof ApiError || error instanceof Error
          ? error.message
          : 'Unable to update person.';
      setPersonStatus({ type: 'error', message });
    } finally {
      setPersonLoading(false);
    }
  };

  const handleOrganizationSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (orgDisabled) {
      setOrgStatus({ type: 'error', message: 'Organization ID is required.' });
      return;
    }

    setOrgStatus(null);
    setOrgLoading(true);
    try {
      const payload = buildOrganizationUpdatePayload(organizationValues);
      const updated = await putJson<typeof payload, { id: number; name: string; slug: string }>(
        '/api/organizations',
        payload,
      );
      setOrgStatus({
        type: 'success',
        message: `Updated ${updated.name} (ID ${updated.id}, slug ${updated.slug}).`,
      });
    } catch (error) {
      const message =
        error instanceof ApiError || error instanceof Error
          ? error.message
          : 'Unable to update organization.';
      setOrgStatus({ type: 'error', message });
    } finally {
      setOrgLoading(false);
    }
  };

  return (
    <section className="rounded-3xl border-2 border-berkeley-blue/20 bg-white/60 p-6 shadow-lg backdrop-blur">
      <div className="flex flex-col gap-2 pb-6">
        <p className="text-sm uppercase tracking-wide text-berkeley-blue/70">Data Maintenance</p>
        <h2 className="text-2xl font-bold text-berkeley-blue">Update existing records in place</h2>
        <p className="text-sm text-gray-600">
          Use record IDs from the database/API responses, provide only the fields you want to change,
          and this tool will issue PUT requests to the Flask API.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <FormCard
          title="Edit Person"
          description="Resolve the person by ID, then send the supplied updates to /api/people."
          onSubmit={handlePersonSubmit}
          status={personStatus}
          actions={
            <Button type="submit" leftIcon={Save} loading={personLoading} disabled={personDisabled}>
              {personLoading ? 'Saving...' : 'Update Person'}
            </Button>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="person_id">
                Person ID *
              </label>
              <input
                id="person_id"
                name="person_id"
                type="number"
                className={inputBase}
                value={personValues.person_id}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, person_id: event.target.value }))
                }
                placeholder="42"
                required
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_first_name">
                First Name
              </label>
              <input
                id="edit_first_name"
                className={inputBase}
                value={personValues.first_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, first_name: event.target.value }))
                }
                placeholder="Jane"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_last_name">
                Last Name
              </label>
              <input
                id="edit_last_name"
                className={inputBase}
                value={personValues.last_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, last_name: event.target.value }))
                }
                placeholder="Doe"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_middle_name">
                Middle Name
              </label>
              <input
                id="edit_middle_name"
                className={inputBase}
                value={personValues.middle_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, middle_name: event.target.value }))
                }
                placeholder="A."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_preferred_name">
                Preferred Name
              </label>
              <input
                id="edit_preferred_name"
                className={inputBase}
                value={personValues.preferred_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, preferred_name: event.target.value }))
                }
                placeholder="Janey"
              />
            </div>
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="edit_bio">
                Bio
              </label>
              <textarea
                id="edit_bio"
                className={`${inputBase} min-h-[90px]`}
                value={personValues.bio}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, bio: event.target.value }))
                }
                placeholder="Update the short biography"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_profile_url">
                Profile URL
              </label>
              <input
                id="edit_profile_url"
                className={inputBase}
                value={personValues.profile_url}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, profile_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_photo_url">
                Photo URL
              </label>
              <input
                id="edit_photo_url"
                className={inputBase}
                value={personValues.photo_url}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, photo_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_is_active">
                Active Status
              </label>
              <select
                id="edit_is_active"
                className={inputBase}
                value={personValues.is_active}
                onChange={(event) =>
                  setPersonValues((prev) => ({
                    ...prev,
                    is_active: event.target.value as BooleanSelect,
                  }))
                }
              >
                <option value="unchanged">Leave unchanged</option>
                <option value="true">Mark active</option>
                <option value="false">Mark inactive</option>
              </select>
            </div>
            <div className="sm:col-span-2 rounded-2xl bg-bay-fog/20 p-4">
              <p className="text-sm font-semibold text-berkeley-blue">Social Media Upsert</p>
              <div className="mt-3 grid gap-3 sm:grid-cols-3">
                <div>
                  <label className={labelBase} htmlFor="edit_social_platform">
                    Platform
                  </label>
                  <input
                    id="edit_social_platform"
                    className={inputBase}
                    value={personValues.social_platform}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, social_platform: event.target.value }))
                    }
                    placeholder="LinkedIn"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="edit_social_handle">
                    Handle
                  </label>
                  <input
                    id="edit_social_handle"
                    className={inputBase}
                    value={personValues.social_handle}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, social_handle: event.target.value }))
                    }
                    placeholder="@janedoe"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="edit_social_url">
                    Profile URL
                  </label>
                  <input
                    id="edit_social_url"
                    className={inputBase}
                    value={personValues.social_url}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, social_url: event.target.value }))
                    }
                    placeholder="https://linkedin.com/in/janedoe"
                  />
                </div>
              </div>
            </div>
            <div className="sm:col-span-2 rounded-2xl bg-bay-fog/20 p-4">
              <p className="text-sm font-semibold text-berkeley-blue">Contact Info Upsert</p>
              <div className="mt-3 grid gap-3 sm:grid-cols-3">
                <div>
                  <label className={labelBase} htmlFor="edit_contact_type">
                    Type
                  </label>
                  <input
                    id="edit_contact_type"
                    className={inputBase}
                    value={personValues.contact_type}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, contact_type: event.target.value }))
                    }
                    placeholder="email"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="edit_contact_value">
                    Value
                  </label>
                  <input
                    id="edit_contact_value"
                    className={inputBase}
                    value={personValues.contact_value}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, contact_value: event.target.value }))
                    }
                    placeholder="jane@university.edu"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="edit_contact_label">
                    Label
                  </label>
                  <input
                    id="edit_contact_label"
                    className={inputBase}
                    value={personValues.contact_label}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, contact_label: event.target.value }))
                    }
                    placeholder="work"
                  />
                </div>
              </div>
            </div>
          </div>
        </FormCard>

        <FormCard
          title="Edit Organization"
          description="Resolve the organization by ID and push updates to /api/organizations."
          onSubmit={handleOrganizationSubmit}
          status={orgStatus}
          actions={
            <Button type="submit" leftIcon={Save} loading={orgLoading} disabled={orgDisabled}>
              {orgLoading ? 'Saving...' : 'Update Organization'}
            </Button>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="organization_id">
                Organization ID *
              </label>
              <input
                id="organization_id"
                type="number"
                className={inputBase}
                value={organizationValues.organization_id}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({
                    ...prev,
                    organization_id: event.target.value,
                  }))
                }
                placeholder="77"
                required
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_name">
                Name
              </label>
              <input
                id="edit_org_name"
                className={inputBase}
                value={organizationValues.name}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, name: event.target.value }))
                }
                placeholder="UC Investments"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_slug">
                Slug
              </label>
              <input
                id="edit_org_slug"
                className={inputBase}
                value={organizationValues.slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, slug: event.target.value }))
                }
                placeholder="uc-investments"
              />
            </div>
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="edit_org_description">
                Description
              </label>
              <textarea
                id="edit_org_description"
                className={`${inputBase} min-h-[90px]`}
                value={organizationValues.description}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, description: event.target.value }))
                }
                placeholder="Mission, scope, or charter updates"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_url">
                Main URL
              </label>
              <input
                id="edit_org_url"
                className={inputBase}
                value={organizationValues.main_url}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, main_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_hierarchy">
                Hierarchy Level
              </label>
              <input
                id="edit_org_hierarchy"
                type="number"
                className={inputBase}
                value={organizationValues.hierarchy_level}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({
                    ...prev,
                    hierarchy_level: event.target.value,
                  }))
                }
                placeholder="1"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_full_path">
                Full Path
              </label>
              <input
                id="edit_org_full_path"
                className={inputBase}
                value={organizationValues.full_path}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, full_path: event.target.value }))
                }
                placeholder="leadership/uc-investments"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_directory_path">
                Directory Path
              </label>
              <input
                id="edit_org_directory_path"
                className={inputBase}
                value={organizationValues.directory_path}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, directory_path: event.target.value }))
                }
                placeholder="handlers/ucop/..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_parent_id">
                Parent ID
              </label>
              <input
                id="edit_org_parent_id"
                type="number"
                className={inputBase}
                value={organizationValues.parent_id}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, parent_id: event.target.value }))
                }
                placeholder="12"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_parent_slug">
                Parent Slug
              </label>
              <input
                id="edit_org_parent_slug"
                className={inputBase}
                value={organizationValues.parent_slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, parent_slug: event.target.value }))
                }
                placeholder="uc-trustees"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_parent_directory">
                Parent Directory Path
              </label>
              <input
                id="edit_org_parent_directory"
                className={inputBase}
                value={organizationValues.parent_directory_path}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({
                    ...prev,
                    parent_directory_path: event.target.value,
                  }))
                }
                placeholder="handlers/..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_category_id">
                Category ID
              </label>
              <input
                id="edit_org_category_id"
                type="number"
                className={inputBase}
                value={organizationValues.category_id}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, category_id: event.target.value }))
                }
                placeholder="5"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_category_slug">
                Category Slug
              </label>
              <input
                id="edit_org_category_slug"
                className={inputBase}
                value={organizationValues.category_slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, category_slug: event.target.value }))
                }
                placeholder="investment-office"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_start_date">
                Start Date
              </label>
              <input
                id="edit_org_start_date"
                type="date"
                className={inputBase}
                value={organizationValues.start_date}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, start_date: event.target.value }))
                }
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_end_date">
                End Date
              </label>
              <input
                id="edit_org_end_date"
                type="date"
                className={inputBase}
                value={organizationValues.end_date}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, end_date: event.target.value }))
                }
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="edit_org_is_active">
                Active Status
              </label>
              <select
                id="edit_org_is_active"
                className={inputBase}
                value={organizationValues.is_active}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({
                    ...prev,
                    is_active: event.target.value as BooleanSelect,
                  }))
                }
              >
                <option value="unchanged">Leave unchanged</option>
                <option value="true">Mark active</option>
                <option value="false">Mark inactive</option>
              </select>
            </div>
          </div>
        </FormCard>
      </div>
    </section>
  );
};
