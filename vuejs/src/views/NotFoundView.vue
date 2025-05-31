<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import { useRoute, useRouter } from 'vue-router';


import SearchBar from '@/components/Auth/SearchBar.vue';

import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();


import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

const loading = ref(true)
const color = ref('red')
const size = ref('100px')

const router = useRouter();

const goBack = () => {
  router.push('/');
};

onMounted(() => {
  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest Clone`; // Если есть непрочитанные уведомления
  } else {
    document.title = 'Pinterest Clone'; // Если уведомлений нет
  }
})

</script>

<template>
  <SearchBar />
  <section class="text-center flex flex-col justify-center items-center relative">
    <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <h1 class="text-4xl font-bold mb-4 mt-20">not found</h1>
    <ClipLoader v-show="loading" :size="size" :color="color" />
    <img v-show="!loading" class="h-96 rounded-xl"
      src="https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg" @load="loading = false"
      alt="not found image">
  </section>
</template>