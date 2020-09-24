<template>
  <div class="chatroom-wrapper">
    <div class="chatroom-view">
      <div v-if="isValid" class="chatroom-messages">
        <div v-for="message in room.messages" v-bind:key="message.messageId" class="message">
          <span class="message-sender">{{message.sender}}</span>
          <p class="message-content">
            {{message.content}}
          </p>
          <span class="message-time">{{dateToString(message.createdAt)}}</span>
        </div>
      </div>
    </div>
    <div class="chatroom-input">
      <form v-on:submit.prevent="sendChat">
        <textarea v-model=chatInput placeholder="내용을 작성해주세요." :disabled="!isValid"></textarea>
        <div>
          <input class="button" type="submit" value="보내기" :disabled="!isValid">
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.chatroom-wrapper {
  width: 70%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-left: 10%;
  padding-right: 50px;
}

.chatroom-view {
  width: 100%;
  height: 80%;
}

.chatroom-messages {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.chatroom-input {
  width: 100%;
  height: 150px;
  padding-top: 30px;
}

.message {
  display: flex;
  flex-direction: column;
  color: #555555;
  margin: 10px 0;
}

.message-sender {
  color: #000000;
}

.message-time {
  color: #888888;
}

.button {
  background-color: #5b79ff;
  border: none;
  color: white;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  height: 30px;
  padding: 0 30px;
  border-radius: 15px;
}

.button:disabled {
  background-color: #555555;
}

</style>

<script lang="ts">
import Vue from 'vue';

import {Room} from '../data';
import {dateToPresentationString} from '../util/date';

export default Vue.extend({
  data() {
    return {
      chatInput: ''
    }
  },

  props: {
    room: {
      type: Object as () => Room | undefined,
    }
  },

  computed: {
    isValid() {
      return this.room !== undefined;
    }
  },

  methods: {
    sendChat(ev: Event) {
      if (this.room === undefined)
        return;
      this.$emit("send-chat", this.room.roomId, this.chatInput);
      this.chatInput = '';
    },

    dateToString(date: Date): string {
      // FIXME: this is not reactive.
      return dateToPresentationString(date, new Date());
    }
  },

  watch: {
    // NOTE: this is a adhoc.
    room(_newVal, _oldVal) {
      this.chatInput = '';
    }
  }
});
</script>
