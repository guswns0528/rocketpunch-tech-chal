const base = process.env.VUE_APP_API_BASE;

interface Resp<T> extends Response {
  jsonBody: T;
}

export async function apiCall<T>(req: RequestInfo): Promise<Resp<T>> {
  const resp: Response = await fetch(req);
  const parsed = await resp.json();
  if (!resp.ok) {
    throw new Error(parsed.msg);
  }
  return {...resp, jsonBody: parsed};
}

export async function get<T>(
  path: string,
  apiToken?: string,
  args: RequestInit = { method: 'get' }
): Promise<Resp<T>> {
  if (apiToken) {
    args['headers'] = {
      'Authorization': 'Bearer ' + apiToken
    };
  }
  return await apiCall<T>(new Request(base + path, args));
}

export async function post<T, Body>(
  path: string,
  body: FormData,
  apiToken?: string,
  args: RequestInit = {
    method: 'post',
    body: body
  }
): Promise<Resp<T>> {
  if (apiToken) {
    const headers: any = args['headers'] || {}
    headers['Authorization'] = {
      'Authorization': 'Bearer ' + apiToken
    };
    args['headers'] = headers;
  }
  return await apiCall<T>(new Request(base + path, args));
}

