import {post} from './common';

export interface LoginResult {
  apiToken: string;
}

interface LoginBody {
  username: string;
  password: string;
}

export async function login(
  username: string,
  password: string
): Promise<LoginResult | undefined> {
  try {
    const data = new FormData();
    data.append('username', username);
    data.append('password', password);
    const token = await post<{api_token: string}, LoginBody>('/api/login/', data);

    return {apiToken: token.jsonBody.api_token};
  }
  catch (ex) {
    console.log(ex);
    // FIXME: just swallows error.
    // need to return error or re-throw.
    return undefined;
  }
  return undefined;
}
