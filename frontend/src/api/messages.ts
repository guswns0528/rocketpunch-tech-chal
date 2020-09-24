import {get} from './common';
import LocalStorage from '../data/LocalStorage'

import {Message} from '../data'

interface LastMessagesResult {
  messages: Message[];
}

export async function lastMessages(roomId: number):
  Promise<LastMessagesResult | undefined> {
  try {
    const storage = new LocalStorage();
    // FIXME: create api service and inject token from outside.
    const token = storage.get('apiToken');
    const result = await get<LastMessagesResult>('/api/chat/' + roomId.toString() + '/', token);
    const messages = result.jsonBody.messages;
    return {messages: messages.map(e => {
      const messageId = e.messageId;
      const sender = e.sender;
      const content = e.content;
      const createdAt = new Date(e.createdAt);
      return {messageId, sender, content, createdAt};
    })};
  }
  catch (ex) {
    console.log(ex);
    return undefined;
  }
  return undefined;
}
