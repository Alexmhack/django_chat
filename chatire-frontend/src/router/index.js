import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld';
import Chat from '@/components/Chat';
import UserAuth from '@/components/UserAuth';

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/chats',
      name: 'Chat',
      component: Chat
    },

    {
  	  path: '/auth',
  	  name: 'UserAuth',
  	  component: UserAuth
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (sessionStorage.getItem('authToken') !== null || to.path === '/auth') {
    next();
  }
  else {
    next('/auth');
  }
})

export default router;
