<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router';
import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();


import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import "dayjs/locale/en"; // Используем английскую локаль

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("en"); // Устанавливаем английскую локаль

const formatTime = (createdAt) => {
  const now = dayjs();
  const createdTime = dayjs.utc(createdAt).local();
  const diffMinutes = now.diff(createdTime, "minute");

  return diffMinutes < 30 ? "just now" : createdTime.fromNow();
};

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

const emit = defineEmits(['logout'])

const props = defineProps({
  me: Object,
  meImage: String
})


async function logout() {
  try {
    await axios.post('/api/users/logout')
    emit('logout')
  } catch (error) {
    console.log(error)
  }
}

const cntUnreadMessages = ref(null)

const showModal = ref(false)

function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  updates.value = []
  offset.value = 0
  limit.value = 10
  isPinsLoading.value = false
}

const updates = ref([])

const offset = ref(0);
const limit = ref(10);

const isPinsLoading = ref(false);

async function loadUpdates() {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/updates/`, { params: { offset: offset.value, limit: limit.value } })
    const data = response.data

    for (let i = 0; i < data.length; i++) {
      if (!data[i].is_read) {
        try {
          await axios.put(`/api/updates/read/${data[i].id}`)
          unreadUpdatesStore.decrement()
        } catch (error) {
          console.error(error)
        }
      }
      const response = await axios.get(`/api/recommendations/${data[i].id}`, {
        params: { offset: 0, limit: 1 },
        withCredentials: true,
      });

      const pin_id = response.data[0].id
      try {
        const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          data[i].file = blobUrl;
          data[i].isImage = true;
        } else {
          data[i].file = blobUrl;
          data[i].isImage = false;
        }
      } catch (error) {
        console.error(error);
      }

      updates.value.push(data[i])
    }
  } catch (error) {
    console.error(error)
  }
  offset.value += limit.value;
  isPinsLoading.value = false;

  if (limit.value == 10) {
    limit.value = 5
  }
}

const handleScroll = (event) => {
  const container = event.target;
  if (container.scrollTop + container.clientHeight >= container.scrollHeight - 10) {
    loadUpdates();
  }
};

let eventSource = null;

async function addNewUpdate(update) {
  if (showModal.value === false) {
    unreadUpdatesStore.increment()
  } else {
    const response = await axios.get(`/api/recommendations/${update.id}`, {
      params: { offset: 0, limit: 1 },
      withCredentials: true,
    });

    const pin_id = response.data[0].id
    try {
      const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(pinResponse.data);
      const contentType = pinResponse.headers['content-type'];
      if (contentType.startsWith('image/')) {
        update.file = blobUrl;
        update.isImage = true;
      } else {
        update.file = blobUrl;
        update.isImage = false;
      }
    } catch (error) {
      console.error(error);
    }

    updates.value.unshift(update);
    try {
      await axios.put(`/api/updates/read/${update.id}`)
      unreadUpdatesStore.decrement()
    } catch (error) {
      console.error(error)
    }
  }
}

onMounted(async () => {
  try {
    const response = await axios.get('/api/recommendations/check', { withCredentials: true })
    if (response.data.make_recommendations) {
      eventSource = new EventSource(`/api/updates/stream/${props.me.id}`);

      eventSource.onmessage = (event) => {
        const rawData = JSON.parse(event.data);  // Парсим первый раз
        const new_update = JSON.parse(rawData.message); // Парсим вложенный JSON
        addNewUpdate(new_update)
      };

      eventSource.onerror = () => {
        console.error("Ошибка SSE!");
        eventSource.close();
      };
    }
  } catch (error) {
    console.error(error)
  }
})

onBeforeUnmount(() => {
  if (eventSource) {
    eventSource.close();
  }
})
</script>


<template>
  <nav
    class="fixed top-0 left-0 h-full w-20 flex flex-col justify-between items-center z-30 border-r border-gray-300 py-4 ">
    <!-- Icons -->
    <div class="flex flex-col items-center text-xl space-y-6">
      <RouterLink to="/"
        :class="[isActiveLink('/') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-home']"></i>
      </RouterLink>
      <RouterLink :to="`/user/${me.username}`"
        :class="[isActiveLink(`/user/${me.username}`) ? '' : 'transition-transform duration-100 transform hover:scale-125 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <img :src="meImage" alt="me profile"
          :class="[isActiveLink(`/user/${me.username}`) ? 'border-black' : 'border-gray-400', 'w-10', 'h-10', 'object-cover', 'rounded-full', 'border-2']" />
      </RouterLink>
      <RouterLink to="/create-pin"
        :class="[isActiveLink('/create-pin') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-plus-circle']"></i>
      </RouterLink>
      <div @click="showModal = !showModal; loadUpdates()" class="relative"
        :class="[showModal ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-bell"></i>
        <div v-if="unreadUpdatesStore.count"
          class="absolute top-0 right-0 py-0.5 px-2 bg-red-600 rounded-full flex align-center items-center">
          <span class="text-xs text-white"> {{ unreadUpdatesStore.count }}</span>
        </div>
      </div>
      <RouterLink to="/messages" class="relative"
        :class="[isActiveLink('/messages') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-envelope"></i>
        <div v-if="unreadMessagesStore.count"
          class="absolute top-0 right-0 py-0.5 px-2 bg-red-600 rounded-full flex align-center items-center">
          <span class="text-xs text-white"> {{ unreadMessagesStore.count }}</span>
        </div>
      </RouterLink>
      <div @click="logout"
        class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-5 text-xl flex items-center">
        <i class="pi pi-sign-out"></i>
      </div>
    </div>
  </nav>

  <Transition name="fade">
    <div v-if="showModal" class="fixed top-4 left-24 bottom-4 w-1/4 bg-white shadow-2xl z-50 rounded-3xl">
      <!-- Заголовок и кнопка закрытия -->
      <div class="flex justify-between items-center p-6 border-b">
        <h2 class="text-xl font-bold text-black">Updates</h2>
        <button @click="closeModal" class="text-black transition text-4xl">
          ×
        </button>
      </div>

      <!-- Список обновлений -->
      <div class="p-4 space-y-4 overflow-y-auto h-[600px]" @scroll="handleScroll">
        <div class="space-y-4">
          <RouterLink :to="`/recommendations/${update.id}`" v-for="update in updates" :key="update.id"
            class="p-4 bg-gray-100 rounded-lg shadow flex items-center space-x-4 w-full h-24 relative">
            <!-- Файл (изображение/видео) слева -->
            <div class="w-24 h-24 flex-shrink-0">
              <template v-if="update.isImage">
                <img :src="update.file" alt="Update Image" class="w-full h-full object-cover rounded-lg" />
              </template>
              <template v-else>
                <video :src="update.file" autoplay muted class="w-full h-full object-cover rounded-lg"></video>
              </template>
            </div>

            <!-- Сообщение в центре -->
            <p class="text-black text-lg font-semibold flex-grow text-center">{{ update.content }}</p>

            <!-- Дата в верхнем правом углу -->
            <span class="absolute top-2 right-2 font-medium text-gray-600 text-sm">{{ formatTime(update.created_at)
            }}</span>
          </RouterLink>
        </div>
      </div>
    </div>
  </Transition>
</template>


<style>
/* Анимация плавного появления (fade) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>