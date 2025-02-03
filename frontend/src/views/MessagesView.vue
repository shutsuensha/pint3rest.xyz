<script setup>
import { onMounted, ref, nextTick, onActivated, computed, onBeforeUnmount } from 'vue';
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

onBeforeUnmount(() => {
  for (let i = 0; i < chats.value.length; i++) {
    if (chats.value[i].socket) {
      chats.value[i].socket.close()
    }
  }
});

onMounted(async () => {
  showLoading.value = true
  document.title = 'pinterest.xyz / chats'
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
      chats.value[i].online = false
      chats.value[i].socket = new WebSocket(`ws://127.0.0.1:8000/ws/${chats.value[i].id}/${auth_user_id.value}?chat_connection=true`);
      chats.value[i].socket.onmessage = async (event) => {
        const message = JSON.parse(event.data);
        if ("online" in message) {
          if (message.online == true) {
            chats.value[i].online = true
          } else {
            chats.value[i].online = false
          }
          return
        }
        updateChat2(message.chat_id)
      }
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
const user_to_load = ref(null)


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
    user_to_load.value = chat.user_1_id === auth_user_id.value ? chat.user_2_id : chat.user_1_id
    showChat.value = true
  }
}


const scrollToTop = () => {
  nextTick(() => {
    if (chatsContainer.value) {
      chatsContainer.value.scrollTop = 0;
    }
  });
};

const chatsContainer = ref(null);



async function updateChat2(chat_id) {
  try {
    const response = await axios.get(`/api/messages/last/${chat_id}`, { withCredentials: true })
    const chatObj = sortedChats.value.find(el => el.id === chat_id);
    const chatIndex = sortedChats.value.findIndex(el => el.id === chat_id);
    if (chat_selected.value !== null && chatIndex > chat_selected.value) {
      chat_selected.value += 1
    }
    chatObj.last_message = response.data
    if (chatObj.last_message.image !== null) {
      try {
        const response = await axios.get(`/api/messages/upload/${chatObj.last_message.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        chatObj.last_message.media = blobUrl
        const contentType = response.headers['content-type'];
        if (contentType.startsWith('image/')) {
          chatObj.last_message.isImage = true;
        } else {
          chatObj.last_message.isImage = false;
        }
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.error(error)
  }
}

async function updateChat(chat_id) {
  scrollToTop()
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
    <WebsocketChat :chat_id="chat_id" :auth_user_id="auth_user_id" :user_to_load="user_to_load"
      @updateLastMessage="(chat_id_) => updateChat(chat_id_)" />
  </div>
  <div v-else class="fixed top-0 left-[465px] h-full w-[800px] z-50 bg-pink-300 flex items-center justify-center">
    <span class="text-xs  text-white bg-black bg-opacity-20 px-2 py-1 rounded-3xl">Select chat to start messaging</span>
  </div>
  <div class="ml-20">
    <div id="chats" ref="chatsContainer" class="fixed top-0 left-20 h-full w-96 flex flex-col z-30 overflow-y-auto"
      v-auto-animate>
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