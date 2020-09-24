import {post} from './common';

interface LoginResult {
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
    const token = await post<LoginResult, LoginBody>('/api/login/', data);

    return token.jsonBody;
  }
  catch (ex) {
    console.log(ex);
    // FIXME: just swallows error.
    // need to return error or re-throw.
    return undefined;
  }
  return undefined;
}
