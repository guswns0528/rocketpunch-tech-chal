import LocalStorage from '../data/LocalStorage'

const authCheck = (): boolean => {
  // NOTE: this function just checks that 'apiToken' key does exist whatever its content.
  // Do I need make a request to verify token valid?
  const storage = new LocalStorage();
  console.log(storage.has('apiToken'));
  return storage.has('apiToken');
}

export {authCheck}
