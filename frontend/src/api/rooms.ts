import {get} from './common';
import {Room} from '../data'
import LocalStorage from '../data/LocalStorage';

interface RoomsResult {
  rooms: Room[];
}

export async function rooms(): Promise<RoomsResult | undefined> {
  try {
    const storage = new LocalStorage();
    // FIXME: create api service and inject token from outside.
    const token = storage.get('apiToken');
    const result = await get<RoomsResult>('/api/rooms/', token);
    return result.jsonBody;
  }
  catch (ex) {
    console.log(ex);
    return undefined;
  }
  return undefined;
}
