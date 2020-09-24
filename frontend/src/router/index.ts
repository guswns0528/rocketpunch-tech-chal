import Vue from 'vue'
import VueRouter, { RouteConfig, NavigationGuard } from 'vue-router'

import Login from '../views/Login.vue'
import Chat from '../views/Chat.vue'

import {authCheck} from './utils'

Vue.use(VueRouter)

const requireAuth: NavigationGuard = (to, from, next) => {
  if (authCheck()) {
    next();
  }
  else {
    next({
      path: '/login'
    });
  }
}

const notLogined: NavigationGuard = (to, from, next) => {
  if (!authCheck()) {
    next();
  }
  else {
    next({
      path: '/'
    });
  }
}

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: Chat,
    beforeEnter: requireAuth
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    beforeEnter: notLogined
  },
  {
    path: '/chat/:id',
    name: 'chat',
    component: Chat,
    beforeEnter: requireAuth
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
