<script setup>
import { onMounted, ref, nextTick, onActivated } from 'vue';
import axios from 'axios'
import UserChat from '@/components/Auth/UserChat.vue';
import WebsocketChat from '@/components/Auth/WebsocketChat.vue';
import { useRoute } from 'vue-router';

const route = useRoute();


const chats = ref(null)
const auth_user_id = ref(null)


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const chat_id_redirect = ref(null)

onMounted(async () => {
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

  } catch (error) {
    console.error(error)
  }

  chat_id_redirect.value = route.query.chat_id || '';
  let index = 0;
  let chatObj = null;
  for (let i = 0; i < chats.value.length; i++) {
    if (chats.value[i].id == chat_id_redirect.value) {
      index = i;
      chatObj = chats.value[i]
      break;
    }
  }
  loadChat(chatObj, index)
})

const showChat = ref(false)
const chat_id = ref(null)
const chat_selected = ref(null)


async function loadChat(chat, index) {
  let id = chat.id
  if (id !== chat_id.value) {
    if (chat_selected.value !== null) {
      chats.value[chat_selected.value].selected = false
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
</script>

<template>
  <div v-if="showChat" class="fixed top-0 left-[465px] h-full w-full z-50">
    <WebsocketChat :chat_id="chat_id" :auth_user_id="auth_user_id" />
  </div>
  <div v-else class="fixed top-0 left-[465px] h-full w-[1000px] z-50 bg-pink-300 flex items-center justify-center">
    <span class="text-xs  text-white bg-black bg-opacity-20 px-2 py-1 rounded-3xl">Select chat to start messaging</span>
  </div>
  <div class="ml-20">
    <div id="chats" 
     class="fixed top-0 left-20 h-full w-96 flex flex-col z-30" 
     :class="[showOverflow ? 'overflow-y-auto' : 'overflow-y-hidden']"
     @mouseover="showOverflow = true" 
     @mouseleave="showOverflow = false">
      <UserChat v-for="(chat, index) in chats" :key="chat.id" :chat="chat" :auth_user_id="auth_user_id"
        @click="loadChat(chat, index)" />
    </div>
  </div>
</template>

<style scoped>


#chats::-webkit-scrollbar {
  width: 5px; /* Ширина скроллбара */
}

#chats::-webkit-scrollbar-track {
  background: #fefefe; /* Фон трека */
  border-radius: 10px;
}

#chats::-webkit-scrollbar-thumb {
  background: rgba(28, 17, 21, 0.4); /* Цвет ползунка */
  border-radius: 10px;
}
</style>