import { createRouter, createWebHistory } from "vue-router";
import { nextTick } from "vue";
import HomeView from '@/views/HomeView.vue';
import CreatePinView from '@/views/CreatePinView.vue';
import PinView from '@/views/PinView.vue';
import UserView from '@/views/UserView.vue';  
import NotFoundView from '@/views/NotFoundView.vue';
import MessagesView from '@/views/MessagesView.vue';
import RecommendationsView from '@/views/RecommendationsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/create-pin', name: 'create-pin', component: CreatePinView },
    { path: '/pin/:id', name: 'pin', component: PinView },
    { path: '/user/:username', name: 'user', component: UserView },
    { path: '/messages', name: 'messages', component: MessagesView },
    { path: '/recommendations/:id', name: 'recommendations', component: RecommendationsView },
    { path: '/:catchAll(.*)', name: 'not-found', component: NotFoundView },
  ],
});


export default router;