import { createRouter, createWebHashHistory } from 'vue-router'

import Menu from '@/components/Menu.vue'
import Orders from '@/components/Orders.vue'
import UserAuth from "@/components/UserAuth.vue";
import store from '../store/index.js'
import Cart from "@/components/Cart.vue";
import Chat from "@/components/Chat.vue";
import Plate from "@/components/Plate.vue";

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: '/', component: Menu, meta: {requiresAuth: true} },
  { path: '/orders', component: Orders, meta: {requiresAuth: true} },
  { path: '/auth', component: UserAuth, meta: {requiresUnauth: true} },
  { path: '/cart', component: Cart, meta: {requiresAuth: true} },
  {path: '/plate/:plate_id', component: Plate, meta: {requiresAuth: true}},
  {path: '/chat', component: Chat, meta: {requiresAuth: true}}
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})

// global navigation guard
router.beforeEach(function(to, _ ,next) {
  if(to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next('/auth');
  } else if (to.meta.requiresUnauth && store.getters.isAuthenticated){
    next('/orders')
  }
  next();
})

export default router;
