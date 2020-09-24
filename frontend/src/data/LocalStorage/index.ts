// NOTE: currently handles plain objects.
// TODO: seperate JSON serializer from storage
export default class LocalStorage {
  set(key: string, value: any) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  get(key: string): any {
    const item = localStorage.getItem(key);
    if (item === null) {
      throw new Error('key does not exist.') 
    }
    return JSON.parse(item);
  }

  has(key: string): boolean {
    return this.get(key) !== null;
  }
}
