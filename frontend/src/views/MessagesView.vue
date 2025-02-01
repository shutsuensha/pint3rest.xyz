<script setup>
import { onMounted, ref, nextTick, onActivated, computed } from 'vue';
import axios from 'axios'
import UserChat from '@/components/Auth/UserChat.vue';
import WebsocketChat from '@/components/Auth/WebsocketChat.vue';
import { useRoute } from 'vue-router';

import ClipLoader from 'vue-spinner/src/ClipLoader.vue'

const color = ref('red')
const size = ref('100px')

const route = useRoute();


const chats = ref(null)
const auth_user_id = ref(null)

const sortedChats = computed(() => {
  return chats.value ? [...chats.value].sort((a, b) => b.last_message.id - a.last_message.id) : [];
});



function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const chat_id_redirect = ref(null)

const showLoading = ref(null)

onMounted(async () => {
  showLoading.value = true
  document.title = 'Telegram'
  const accessToken = getCookie('access_token');
  // Decode the JWT (assuming the access_token is a JWT)
  const base64Url = accessToken.split('.')[1]; // Get the payload part
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );

  const payload = JSON.parse(jsonPayload);

  // Log user_id to the console
  auth_user_id.value = payload.user_id;
  try {
    const response = await axios.get('/api/messages/user_chats', { withCredentials: true })
    chats.value = response.data
    for (let i = 0; i < chats.value.length; i++) {
      try {
        const response = await axios.get(`/api/messages/last/${chats.value[i].id}`, { withCredentials: true })
        chats.value[i].last_message = response.data
        if (chats.value[i].last_message.image !== null) {
          try {
            const response = await axios.get(`/api/messages/upload/${chats.value[i].last_message.id}`, { responseType: 'blob' });
            const blobUrl = URL.createObjectURL(response.data);
            chats.value[i].last_message.media = blobUrl
            const contentType = response.headers['content-type'];
            if (contentType.startsWith('image/')) {
              chats.value[i].last_message.isImage = true;
            } else {
              chats.value[i].last_message.isImage = false;
            }
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error)
      }
    }
  } catch (error) {
    console.error(error)
  }

  showLoading.value = false

  chat_id_redirect.value = route.query.chat_id || null;
  if (chat_id_redirect.value !== null) {
    let index = 0;
    let chatObj = null;
    for (let i = 0; i < sortedChats.value.length; i++) {
      if (sortedChats.value[i].id == chat_id_redirect.value) {
        index = i;
        chatObj = sortedChats.value[i]
        break;
      }
    }
    loadChat(chatObj, index)
  }
})

const showChat = ref(false)
const chat_id = ref(null)
const chat_selected = ref(null)


async function loadChat(chat, index) {
  let id = chat.id
  if (id !== chat_id.value) {
    if (chat_selected.value !== null) {
      sortedChats.value[chat_selected.value].selected = false
    }
    chat.selected = true
    chat_selected.value = index
    showChat.value = false
    await nextTick()
    chat_id.value = id
    showChat.value = true
  }
}

const showOverflow = ref(false)

async function updateChat(chat_id) {
  try {
    const response = await axios.get(`/api/messages/last/${chat_id}`, { withCredentials: true })
    sortedChats.value[chat_selected.value].last_message = response.data
    chat_selected.value = 0
    if (sortedChats.value[chat_selected.value].last_message.image !== null) {
      try {
        const response = await axios.get(`/api/messages/upload/${sortedChats.value[chat_selected.value].last_message.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        sortedChats.value[chat_selected.value].last_message.media = blobUrl
        const contentType = response.headers['content-type'];
        if (contentType.startsWith('image/')) {
          sortedChats.value[chat_selected.value].last_message.isImage = true;
        } else {
          sortedChats.value[chat_selected.value].last_message.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div v-if="showChat" class="fixed top-0 left-[465px] h-full w-full z-50">
    <WebsocketChat :chat_id="chat_id" :auth_user_id="auth_user_id"
      @updateLastMessage="(chat_id_) => updateChat(chat_id_)" />
  </div>
  <div v-else class="fixed top-0 left-[465px] h-full w-[1000px] z-50 bg-pink-300 flex items-center justify-center">
    <span class="text-xs  text-white bg-black bg-opacity-20 px-2 py-1 rounded-3xl">Select chat to start messaging</span>
  </div>
  <div class="ml-20">
    <div id="chats" class="fixed top-0 left-20 h-full w-96 flex flex-col z-30 overflow-y-auto" v-auto-animate>
      <UserChat v-if="!showLoading" v-for="(chat, index) in sortedChats" :key="chat.id" :chat="chat"
        :auth_user_id="auth_user_id" @click="loadChat(chat, index)" />
      <ClipLoader v-if="showLoading" :color="color" :size="size"
        class="flex items-center justify-center h-96 font-extrabold" />
    </div>
  </div>
</template>

<style scoped>
#chats::-webkit-scrollbar {
  width: 5px;
  /* Ширина скроллбара */
}

#chats::-webkit-scrollbar-track {
  background: #fefefe;
  /* Фон трека */
  border-radius: 10px;
}

#chats::-webkit-scrollbar-thumb {
  background: rgba(28, 17, 21, 0.1);
  /* Цвет ползунка */
  border-radius: 10px;
}
</style>