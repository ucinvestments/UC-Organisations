const DEFAULT_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:5000').replace(
  /\/$/,
  '',
);

const toUrl = (path: string) => {
  if (!path) {
    throw new Error('API path is required');
  }
  return `${DEFAULT_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
};

const parseJsonSafely = async (response: Response) => {
  const text = await response.text();
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

type JsonMethod = 'POST' | 'PUT';

const sendJson = async <TBody extends Record<string, unknown>, TResult>(
  method: JsonMethod,
  path: string,
  body: TBody,
  init?: RequestInit,
): Promise<TResult> => {
  const response = await fetch(toUrl(path), {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    body: JSON.stringify(body),
    ...init,
  });

  const data = await parseJsonSafely(response);
  if (!response.ok) {
    const message =
      (data && typeof data === 'object' && 'error' in data && (data as { error: string }).error) ||
      `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status);
  }

  return data as TResult;
};

export async function postJson<TBody extends Record<string, unknown>, TResult>(
  path: string,
  body: TBody,
  init?: RequestInit,
): Promise<TResult> {
  return sendJson('POST', path, body, init);
}

export async function putJson<TBody extends Record<string, unknown>, TResult>(
  path: string,
  body: TBody,
  init?: RequestInit,
): Promise<TResult> {
  return sendJson('PUT', path, body, init);
}
