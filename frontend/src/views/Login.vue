<template>
  <div id="wrapper">
    <form v-on:submit.prevent="handleLogin">
      <label for="username">Username</label>
      <input name="username" type="text" v-model="username">
      <label for="password">Password</label>
      <input name="password" type="password" v-model="password">
      <input type="submit">
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {login} from '../api';
import LocalStorage from '../data/LocalStorage'

export default Vue.extend({
  data() {
    return {
      username: '',
      password: '',
    }
  },

  methods: {
    handleLogin(ev: Event) {
      login(this.username, this.password).then(result => {
        if (result === undefined) {
          alert('failed to login');
        }
        else {
          const storage = new LocalStorage();
          storage.set('apiToken', result.apiToken);
          this.$router.push('/');
        }
      });
    }
  }
});
</script>
