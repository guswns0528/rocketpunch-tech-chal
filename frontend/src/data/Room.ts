import Message from './Message'

interface Room {
  roomId: number
  name: string
  messages: Message[]
};

export default Room;
