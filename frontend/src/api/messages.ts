import {get} from './common';
import LocalStorage from '../data/LocalStorage'

import {Message} from '../data'

interface MessagesResult {
  messages: Message[];
}

export async function lastMessages(roomId: number):
  Promise<MessagesResult | undefined> {
  try {
    const storage = new LocalStorage();
    // FIXME: create api service and inject token from outside.
    const token = storage.get('apiToken');
    const result = await get<MessagesResult>(`/api/chat/${roomId}/`, token);
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

export async function messagesBefore(roomId: number, since: number):
  Promise<MessagesResult | undefined> {
  try {
    const storage = new LocalStorage();
    const token = storage.get('apiToken');
    const result = await get<MessagesResult>(
      `/api/chat_before/${roomId}/${since}/`, token
    );
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
