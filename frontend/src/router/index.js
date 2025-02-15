import { createRouter, createWebHistory } from "vue-router";
import { nextTick } from "vue";
import HomeView from '@/views/HomeView.vue';
import CreatePinView from '@/views/CreatePinView.vue';
import PinView from '@/views/PinView.vue';
import UserView from '@/views/UserView.vue';  
import NotFoundView from '@/views/NotFoundView.vue';
import MessagesView from '@/views/MessagesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/create-pin', name: 'create-pin', component: CreatePinView },
    { path: '/pin/:id', name: 'pin', component: PinView },
    { path: '/user/:username', name: 'user', component: UserView },
    { path: '/messages', name: 'messages', component: MessagesView },
    { path: '/:catchAll(.*)', name: 'not-found', component: NotFoundView },
  ],
});

let hasVisitedMessages = false;
let pendingRoute = null; // Храним изначально запрошенный маршрут

router.beforeEach((to, from, next) => {
  if (!hasVisitedMessages && to.path !== '/messages') {
    hasVisitedMessages = true;
    pendingRoute = to; // Сохраняем запрашиваемый маршрут
    next('/messages'); // Перенаправляем на /messages
  } else {
    next();
  }
});

router.afterEach(async (to) => {
  if (to.path === '/messages' && pendingRoute) {
    await nextTick(); // Ждём, пока обновится DOM
    const routeToGo = pendingRoute;
    pendingRoute = null; // Сбрасываем временный маршрут
    router.push(routeToGo); // Перенаправляем на изначально запрошенный маршрут
  }
});

export default router;