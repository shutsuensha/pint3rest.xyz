<script setup>
import { onMounted, ref, nextTick } from 'vue';
import axios from 'axios'
import UserChat from '@/components/Auth/UserChat.vue';
import WebsocketChat from '@/components/Auth/WebsocketChat.vue';


const chats = ref(null)
const auth_user_id = ref(null)


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}


onMounted(async () => {
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
})

const showChat = ref(false)
const chat_id = ref(null)

async function loadChat(id) {
  if (id !== chat_id.value) {
    showChat.value = false
    await nextTick()
    chat_id.value = id
    showChat.value = true
  }
}
</script>

<template>
  <div v-if="showChat" class="fixed top-0 left-[400px] h-full w-full flex flex-col items-center z-30 py-4">
    <WebsocketChat :chat_id="chat_id" :auth_user_id="auth_user_id"/>
  </div>  
  <div class="mt-5 ml-20">
    <div class="fixed top-0 left-20 h-full w-96 flex flex-col items-center z-30 border-r border-gray-300 py-4">
      <UserChat v-for="chat in chats" :key="chat.id" :chat="chat" :auth_user_id="auth_user_id"
        @click="loadChat(chat.id)" />
    </div>
  </div>
</template>