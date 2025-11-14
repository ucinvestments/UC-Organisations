import { FormEvent, ReactNode, useMemo, useState } from 'react';
import { Button } from '@/src/design-system';
import { AlertCircle, CheckCircle, Plus } from '@/src/design-system/icons';
import { ApiError, postJson } from '@/src/lib/api';

type FormStatus = {
  type: 'success' | 'error';
  message: string;
};

type PersonFormValues = {
  first_name: string;
  last_name: string;
  middle_name: string;
  preferred_name: string;
  bio: string;
  profile_url: string;
  photo_url: string;
  is_active: boolean;
  social_platform: string;
  social_handle: string;
  social_url: string;
  contact_type: string;
  contact_value: string;
  contact_label: string;
};

type OrganizationFormValues = {
  name: string;
  slug: string;
  description: string;
  main_url: string;
  hierarchy_level: string;
  full_path: string;
  directory_path: string;
  parent_id: string;
  parent_slug: string;
  category_id: string;
  category_slug: string;
  start_date: string;
  end_date: string;
  is_active: boolean;
};

type PersonResponse = {
  id: number;
  first_name: string;
  last_name: string;
};

type OrganizationResponse = {
  id: number;
  name: string;
  slug: string;
};

const inputBase =
  'mt-1 block w-full rounded-xl border border-berkeley-blue/20 bg-white/80 px-3 py-2 text-gray-900 shadow-sm focus:border-berkeley-blue focus:ring-2 focus:ring-berkeley-blue/30';
const labelBase = 'text-sm font-semibold text-berkeley-blue';

const initialPersonValues: PersonFormValues = {
  first_name: '',
  last_name: '',
  middle_name: '',
  preferred_name: '',
  bio: '',
  profile_url: '',
  photo_url: '',
  is_active: true,
  social_platform: '',
  social_handle: '',
  social_url: '',
  contact_type: '',
  contact_value: '',
  contact_label: '',
};

const initialOrganizationValues: OrganizationFormValues = {
  name: '',
  slug: '',
  description: '',
  main_url: '',
  hierarchy_level: '',
  full_path: '',
  directory_path: '',
  parent_id: '',
  parent_slug: '',
  category_id: '',
  category_slug: '',
  start_date: '',
  end_date: '',
  is_active: true,
};

const parseNumberField = (value: string) => {
  if (!value.trim()) {
    return undefined;
  }
  const parsed = Number(value);
  return Number.isNaN(parsed) ? undefined : parsed;
};

const buildPersonPayload = (values: PersonFormValues) => {
  const payload: Record<string, unknown> = {
    first_name: values.first_name.trim(),
    last_name: values.last_name.trim(),
    is_active: values.is_active,
  };

  const optionalTextFields: Array<keyof PersonFormValues> = [
    'middle_name',
    'preferred_name',
    'bio',
    'profile_url',
    'photo_url',
  ];

  optionalTextFields.forEach((field) => {
    const value = values[field];
    if (typeof value === 'string' && value.trim()) {
      payload[field] = value.trim();
    }
  });

  if (values.social_platform && values.social_url) {
    payload.social_media = [
      {
        platform: values.social_platform.trim(),
        handle: values.social_handle?.trim() || undefined,
        profile_url: values.social_url.trim(),
      },
    ];
  }

  if (values.contact_type && values.contact_value) {
    payload.contact_info = [
      {
        contact_type: values.contact_type.trim(),
        contact_value: values.contact_value.trim(),
        contact_label: values.contact_label?.trim() || undefined,
      },
    ];
  }

  return payload;
};

const buildOrganizationPayload = (values: OrganizationFormValues) => {
  const payload: Record<string, unknown> = {
    name: values.name.trim(),
    is_active: values.is_active,
  };

  const optionalStrings: Array<keyof OrganizationFormValues> = [
    'slug',
    'description',
    'main_url',
    'full_path',
    'directory_path',
    'parent_slug',
    'category_slug',
    'start_date',
    'end_date',
  ];

  optionalStrings.forEach((field) => {
    const value = values[field];
    if (value && value.trim()) {
      payload[field] = value.trim();
    }
  });

  const numericFieldMap: Record<string, number | undefined> = {
    hierarchy_level: parseNumberField(values.hierarchy_level),
    parent_id: parseNumberField(values.parent_id),
    category_id: parseNumberField(values.category_id),
  };

  Object.entries(numericFieldMap).forEach(([key, value]) => {
    if (typeof value === 'number') {
      payload[key] = value;
    }
  });

  return payload;
};

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

export const CreateEntitiesPanel = () => {
  const [personValues, setPersonValues] = useState<PersonFormValues>(initialPersonValues);
  const [organizationValues, setOrganizationValues] = useState<OrganizationFormValues>(
    initialOrganizationValues,
  );

  const [personStatus, setPersonStatus] = useState<FormStatus | null>(null);
  const [orgStatus, setOrgStatus] = useState<FormStatus | null>(null);

  const [personLoading, setPersonLoading] = useState(false);
  const [orgLoading, setOrgLoading] = useState(false);

  const personDisabled = useMemo(
    () => !personValues.first_name.trim() || !personValues.last_name.trim(),
    [personValues.first_name, personValues.last_name],
  );
  const orgDisabled = useMemo(
    () => !organizationValues.name.trim(),
    [organizationValues.name],
  );

  const handlePersonSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (personDisabled) {
      setPersonStatus({ type: 'error', message: 'First and last name are required.' });
      return;
    }

    setPersonStatus(null);
    setPersonLoading(true);
    try {
      const payload = buildPersonPayload(personValues);
      const created = await postJson<typeof payload, PersonResponse>('/api/people', payload);
      setPersonStatus({
        type: 'success',
        message: `Created ${created.first_name} ${created.last_name} (ID ${created.id}).`,
      });
      setPersonValues(initialPersonValues);
    } catch (error) {
      const message = error instanceof ApiError ? error.message : 'Unable to create person.';
      setPersonStatus({ type: 'error', message });
    } finally {
      setPersonLoading(false);
    }
  };

  const handleOrganizationSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (orgDisabled) {
      setOrgStatus({ type: 'error', message: 'Organization name is required.' });
      return;
    }

    setOrgStatus(null);
    setOrgLoading(true);
    try {
      const payload = buildOrganizationPayload(organizationValues);
      const created = await postJson<typeof payload, OrganizationResponse>(
        '/api/organizations',
        payload,
      );
      setOrgStatus({
        type: 'success',
        message: `Created ${created.name} (ID ${created.id}, slug ${created.slug}).`,
      });
      setOrganizationValues(initialOrganizationValues);
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : 'Unable to create organization.';
      setOrgStatus({ type: 'error', message });
    } finally {
      setOrgLoading(false);
    }
  };

  return (
    <section className="mt-12 rounded-3xl border-2 border-berkeley-blue/20 bg-white/60 p-6 shadow-lg backdrop-blur">
      <div className="flex flex-col gap-2 pb-6">
        <p className="text-sm uppercase tracking-wide text-berkeley-blue/70">Data Entry</p>
        <h2 className="text-2xl font-bold text-berkeley-blue">
          Push new people and organizations to the source database
        </h2>
        <p className="text-sm text-gray-600">
          These forms call the Flask API directly. Make sure your backend is running locally (or
          configure <code className="rounded bg-gray-100 px-1">NEXT_PUBLIC_API_BASE_URL</code>) so
          submissions can be persisted.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <FormCard
          title="Create Person"
          description="Send a POST request to /api/people with the core profile data and optional contact metadata."
          onSubmit={handlePersonSubmit}
          status={personStatus}
          actions={
            <Button type="submit" leftIcon={Plus} loading={personLoading} disabled={personDisabled}>
              {personLoading ? 'Creating...' : 'Create Person'}
            </Button>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-1">
              <label className={labelBase} htmlFor="first_name">
                First Name *
              </label>
              <input
                id="first_name"
                name="first_name"
                className={inputBase}
                value={personValues.first_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, first_name: event.target.value }))
                }
                placeholder="Jane"
                required
              />
            </div>
            <div className="sm:col-span-1">
              <label className={labelBase} htmlFor="last_name">
                Last Name *
              </label>
              <input
                id="last_name"
                name="last_name"
                className={inputBase}
                value={personValues.last_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, last_name: event.target.value }))
                }
                placeholder="Doe"
                required
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="middle_name">
                Middle Name
              </label>
              <input
                id="middle_name"
                name="middle_name"
                className={inputBase}
                value={personValues.middle_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, middle_name: event.target.value }))
                }
                placeholder="A."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="preferred_name">
                Preferred Name
              </label>
              <input
                id="preferred_name"
                name="preferred_name"
                className={inputBase}
                value={personValues.preferred_name}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, preferred_name: event.target.value }))
                }
                placeholder="Janey"
              />
            </div>
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="bio">
                Bio
              </label>
              <textarea
                id="bio"
                name="bio"
                className={`${inputBase} min-h-[100px]`}
                value={personValues.bio}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, bio: event.target.value }))
                }
                placeholder="Short biography or background"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="profile_url">
                Profile URL
              </label>
              <input
                id="profile_url"
                name="profile_url"
                className={inputBase}
                value={personValues.profile_url}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, profile_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="photo_url">
                Photo URL
              </label>
              <input
                id="photo_url"
                name="photo_url"
                className={inputBase}
                value={personValues.photo_url}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, photo_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div className="sm:col-span-2 rounded-2xl bg-bay-fog/20 p-4">
              <p className="text-sm font-semibold text-berkeley-blue">Social Media</p>
              <div className="mt-3 grid gap-3 sm:grid-cols-3">
                <div>
                  <label className={labelBase} htmlFor="social_platform">
                    Platform
                  </label>
                  <input
                    id="social_platform"
                    name="social_platform"
                    className={inputBase}
                    value={personValues.social_platform}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, social_platform: event.target.value }))
                    }
                    placeholder="LinkedIn"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="social_handle">
                    Handle
                  </label>
                  <input
                    id="social_handle"
                    name="social_handle"
                    className={inputBase}
                    value={personValues.social_handle}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, social_handle: event.target.value }))
                    }
                    placeholder="@janedoe"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="social_url">
                    Profile URL
                  </label>
                  <input
                    id="social_url"
                    name="social_url"
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
              <p className="text-sm font-semibold text-berkeley-blue">Contact Info</p>
              <div className="mt-3 grid gap-3 sm:grid-cols-3">
                <div>
                  <label className={labelBase} htmlFor="contact_type">
                    Type
                  </label>
                  <input
                    id="contact_type"
                    name="contact_type"
                    className={inputBase}
                    value={personValues.contact_type}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, contact_type: event.target.value }))
                    }
                    placeholder="email"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="contact_value">
                    Value
                  </label>
                  <input
                    id="contact_value"
                    name="contact_value"
                    className={inputBase}
                    value={personValues.contact_value}
                    onChange={(event) =>
                      setPersonValues((prev) => ({ ...prev, contact_value: event.target.value }))
                    }
                    placeholder="jane@university.edu"
                  />
                </div>
                <div>
                  <label className={labelBase} htmlFor="contact_label">
                    Label
                  </label>
                  <input
                    id="contact_label"
                    name="contact_label"
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
            <label className="flex items-center gap-2 text-sm font-medium text-berkeley-blue">
              <input
                type="checkbox"
                checked={personValues.is_active}
                onChange={(event) =>
                  setPersonValues((prev) => ({ ...prev, is_active: event.target.checked }))
                }
                className="h-4 w-4 rounded border-berkeley-blue/30 text-berkeley-blue focus:ring-berkeley-blue/40"
              />
              Active profile
            </label>
          </div>
        </FormCard>

        <FormCard
          title="Create Organization"
          description="Send a POST request to /api/organizations with hierarchy metadata."
          onSubmit={handleOrganizationSubmit}
          status={orgStatus}
          actions={
            <Button type="submit" leftIcon={Plus} loading={orgLoading} disabled={orgDisabled}>
              {orgLoading ? 'Creating...' : 'Create Organization'}
            </Button>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="org_name">
                Organization Name *
              </label>
              <input
                id="org_name"
                name="org_name"
                className={inputBase}
                value={organizationValues.name}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, name: event.target.value }))
                }
                placeholder="UC Investments"
                required
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_slug">
                Slug
              </label>
              <input
                id="org_slug"
                name="org_slug"
                className={inputBase}
                value={organizationValues.slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, slug: event.target.value }))
                }
                placeholder="uc-investments"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_main_url">
                Main URL
              </label>
              <input
                id="org_main_url"
                name="org_main_url"
                className={inputBase}
                value={organizationValues.main_url}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, main_url: event.target.value }))
                }
                placeholder="https://..."
              />
            </div>
            <div className="sm:col-span-2">
              <label className={labelBase} htmlFor="org_description">
                Description
              </label>
              <textarea
                id="org_description"
                name="org_description"
                className={`${inputBase} min-h-[100px]`}
                value={organizationValues.description}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, description: event.target.value }))
                }
                placeholder="What does this group do?"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_hierarchy_level">
                Hierarchy Level
              </label>
              <input
                id="org_hierarchy_level"
                name="org_hierarchy_level"
                type="number"
                className={inputBase}
                value={organizationValues.hierarchy_level}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, hierarchy_level: event.target.value }))
                }
                placeholder="1"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_full_path">
                Full Path
              </label>
              <input
                id="org_full_path"
                name="org_full_path"
                className={inputBase}
                value={organizationValues.full_path}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, full_path: event.target.value }))
                }
                placeholder="leadership/uc-investments"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_directory_path">
                Directory Path
              </label>
              <input
                id="org_directory_path"
                name="org_directory_path"
                className={inputBase}
                value={organizationValues.directory_path}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, directory_path: event.target.value }))
                }
                placeholder="handlers/ucop/..."
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_parent_id">
                Parent ID
              </label>
              <input
                id="org_parent_id"
                name="org_parent_id"
                type="number"
                className={inputBase}
                value={organizationValues.parent_id}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, parent_id: event.target.value }))
                }
                placeholder="123"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_parent_slug">
                Parent Slug
              </label>
              <input
                id="org_parent_slug"
                name="org_parent_slug"
                className={inputBase}
                value={organizationValues.parent_slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, parent_slug: event.target.value }))
                }
                placeholder="uc-investments"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_category_id">
                Category ID
              </label>
              <input
                id="org_category_id"
                name="org_category_id"
                type="number"
                className={inputBase}
                value={organizationValues.category_id}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, category_id: event.target.value }))
                }
                placeholder="45"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_category_slug">
                Category Slug
              </label>
              <input
                id="org_category_slug"
                name="org_category_slug"
                className={inputBase}
                value={organizationValues.category_slug}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, category_slug: event.target.value }))
                }
                placeholder="investment-office"
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_start_date">
                Start Date
              </label>
              <input
                id="org_start_date"
                name="org_start_date"
                type="date"
                className={inputBase}
                value={organizationValues.start_date}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, start_date: event.target.value }))
                }
              />
            </div>
            <div>
              <label className={labelBase} htmlFor="org_end_date">
                End Date
              </label>
              <input
                id="org_end_date"
                name="org_end_date"
                type="date"
                className={inputBase}
                value={organizationValues.end_date}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, end_date: event.target.value }))
                }
              />
            </div>
            <label className="flex items-center gap-2 text-sm font-medium text-berkeley-blue">
              <input
                type="checkbox"
                checked={organizationValues.is_active}
                onChange={(event) =>
                  setOrganizationValues((prev) => ({ ...prev, is_active: event.target.checked }))
                }
                className="h-4 w-4 rounded border-berkeley-blue/30 text-berkeley-blue focus:ring-berkeley-blue/40"
              />
              Active organization
            </label>
          </div>
        </FormCard>
      </div>
    </section>
  );
};
