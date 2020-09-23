// NOTE: currently handles plain objects.
// TODO: seperate JSON serializer from storage
export default class LocalStorage {
  set(key: string, value: any) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  get(key: string): any {
    return localStorage.getItem(key);
  }

  has(key: string): boolean {
    return this.get(key) !== null;
  }
}
