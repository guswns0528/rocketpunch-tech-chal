<template>
  <div class="roomlist-wrapper">
    <div v-for="room in rooms" v-bind:key="room.roomId" v-on:click="selectRoom(room)" v-bind:class="{ selected: selectedRoom && selectedRoom.roomId === room.roomId }" class="room-wrapper">
      <div class="room">
        <span>{{room.name}}</span>
        <span class="last-message-time" v-if="lastMessage(room)">{{dateToString(lastMessage(room).createdAt)}}</span>
        <div class="last-message" v-if="lastMessage(room)">{{lastMessage(room).content}}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.roomlist-wrapper {
  width: 30%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.room-wrapper {
  height: 12.5%;
  padding: 0 20px;
  display: flex;
  border-bottom: 3px #000000;
}

.room {
  width: 100%;
  margin: auto 0;
}

.room:hover {
  cursor: pointer;
}

.selected {
  background-color: #cccccc;
}

.last-message-time {
  color: #888888;
}

.last-message {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow:hidden;
  color: #555555;
}

span + span {
  margin-left: 20px;
}

</style>

<script lang="ts">
import Vue from 'vue';
import {Room} from '../data';
import {dateToPresentationString} from '../util/date';

export default Vue.extend({
  data() {
    return {
      selectedRoom: undefined as Room | undefined
    };
  },

  props: {
    rooms: {
      type: Array as () => Room[],
      required: true
    }
  },

  methods: {
    selectRoom(room: Room) {
      if (this.selectedRoom && this.selectedRoom.roomId === room.roomId)
        return;
      this.selectedRoom = room;
      this.$emit("enter-room", room);
    },

    lastMessage(room: Room) {
      const messages = room.messages;
      if (messages.length === 0)
        return undefined;
      return messages[messages.length - 1];
    },

    dateToString(date: Date): string {
      // FIXME: this is not reactive.
      return dateToPresentationString(date, new Date());
    }
  },
});
</script>
