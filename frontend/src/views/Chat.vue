<template>
  <div id="chat-wrapper">
    <div id="chat-header">
      <div id="chatlist-status">
        <span>안 읽은 대화({{0}})</span>
        <button>+ 새로운 메세지</button>
      </div>
      <div id="chatroom-status">
        <span>{{getRoomName(currentRoomId)}}</span>
      </div>
    </div>
    <div id="chat-content">
      <RoomList @enter-room="enterRoom" v-bind:rooms="this.rooms" />
      <ChatRoom v-bind:room="getRoom(currentRoomId)" />
    </div>
  </div>
</template>

<style scoped>
#chat-wrapper {
  height: 100%;
}

#chat-header {
  height: 10vh;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  border-bottom: 10px #000000;
}

#chatlist-status {
  width: 30%;
  border-right: 1px #000000;
  display:flex;
  justify-content: space-between;
  align-items: center;
}

#chatroom-status {
  padding-left: 5%;
  width: 70%;
}

#chatlist-status + #chatroom-status {
  margin-left: 20px;
}

button {
  background-color: #5b79ff;
  border: none;
  color: white;
  text-align: center;
  display: inline-block;
  font-size: 18px;
  padding: 16px;
  height: 50px;
  border-radius: 25px;
}

#chat-content {
  padding-top: 10vh;
  height: 90vh;
  display: flex;
}
</style>

<script lang="ts">
import Vue from 'vue';
import {Room, Message} from '../data';
import {rooms as roomsApi, lastMessages as messageApi} from '../api';

import RoomList from '../components/RoomList.vue';
import ChatRoom from '../components/ChatRoom.vue';

export default Vue.extend({
  data() {
    return {
      rooms: [] as Room[],
      currentRoomId: null as number | null,
      ws: undefined as WebSocket | undefined
    };
  },

  created() {
    if (this.$route.params.id) {
      const roomId = parseInt(this.$route.params.id, 10);
      // check nan
      if (!isNaN(roomId)) {
        this.currentRoomId = roomId;
      }
    }

    let rooms = [] as Room[];
    roomsApi().then(result => {
      if (result === undefined) {
        // failed to call api.
        throw new Error('failed to fetch data.');
      }

      rooms = result.rooms;
      console.log(rooms);
      const promises: Promise<Message[]>[] = [];

      for (let i = 0; i < rooms.length; i++) {
        const room = rooms[i];
        promises.push((async (): Promise<Message[]> => {
          const result = await messageApi(room.roomId);
          if (result == undefined) {
            throw new Error('failed to fetch data.');
          }
          return result.messages;
        })());
      }
      
      return Promise.all(promises);
    }).then((result: Message[][]) => {
      for (let i = 0; i < result.length; i++) {
        rooms[i].messages = result[i];
      }
      this.rooms = rooms;

      // TODO: seperate ws code form component.
      this.ws = new WebSocket(process.env.VUE_APP_WS_BASE + "/chat/");
      this.ws.onmessage = (ev) => {
        const data = JSON.parse(ev.data);
        switch (data.type) {
          case 'JOIN': {
            Vue.set(this.rooms, data.roomId, data);
          }
          break;

          case 'MSG': {
            const roomId = data.roomId;
            const chat = this.rooms[roomId]; // find chat by roomId;
            chat.messages.push(data.message);
          }
          break;
        }
      };
    });
  },

  beforeDestroy() {
    const ws = this.ws as WebSocket;
    ws.close();
  },

  computed: {
  },

  methods: {
    enterRoom(room: Room) {
      console.log(room);
      this.currentRoomId = room.roomId;
      console.log(this.currentRoomId);
    },

    getRoom(roomId: number) {
      return this.rooms.find(e => e.roomId == roomId);
    },

    getRoomName(roomId: number) {
      const room = this.getRoom(roomId);
      if (room === undefined)
        return '';
      return room.name;
    }
  },

  components: {
    RoomList,
    ChatRoom
  }
});
</script>
