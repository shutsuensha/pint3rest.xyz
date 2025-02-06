<script setup>
import axios from 'axios';
import { onMounted, onBeforeUnmount, ref, nextTick } from 'vue';
import FollowersSection from './FollowersSection.vue';
import FollowingSection from './FollowingSection.vue';
import { RouterLink, useRoute } from 'vue-router';
import double_check from '@/assets/double_check.png';
import single_check from '@/assets/single_check.png';

import { useUnreadMessagesStore } from "@/stores/unreadMessages";
const unreadMessagesStore = useUnreadMessagesStore();


import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/ru";



dayjs.extend(relativeTime);
dayjs.locale("ru");


const emit = defineEmits(['updateLastMessage'])

let socket;

const chatBox = ref(null);


const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight;
    }
  });
};

const cntUnreadMessages = ref(null)



const messages = ref([]);
const message = ref("");


const offset = ref(0);
const limit = ref(10);

const isPinsLoading = ref(false);


const messagesTemp = ref(null)

async function loadMessages() {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;

  try {
    const response = await axios.get(`/api/messages/history/${props.chat_id}`, { params: { offset: offset.value, limit: limit.value } })
    messagesTemp.value = response.data
    for (let i = 0; i < messagesTemp.value.length; i++) {
      if (messagesTemp.value[i].user_id_ !== props.auth_user_id && messagesTemp.value[i].is_read === false) {
        try {
          const response = await axios.patch(`/api/messages/read/${messagesTemp.value[i].id}`)
        } catch (error) {
          console.log(error)
        }
        cntUnreadMessages.value -= 1
        props.chat.cntUnreadMessages -= 1
        if (unreadMessagesStore.count > 0) {
          unreadMessagesStore.decrement()
        }
      }
      if (messagesTemp.value[i].image) {
        try {
          const response = await axios.get(`/api/messages/upload/${messagesTemp.value[i].id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          messagesTemp.value[i].media = blobUrl
          const contentType = response.headers['content-type'];
          if (contentType.startsWith('image/')) {
            messagesTemp.value[i].isImage = true;
          } else {
            messagesTemp.value[i].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }
      messages.value.push(messagesTemp.value[i])
    }
  } catch (error) {
    console.error(error)
  }

  offset.value += limit.value;
  isPinsLoading.value = false;
  if (cntUnreadMessages.value !== 0) {
    loadMessages()
  }
}

const handleScroll = (event) => {
  const container = event.target;

  // Когда пользователь прокручивает вверх (то есть scrollTop увеличивается)
  if (container.scrollHeight + container.scrollTop < 700) {

    loadMessages(); // Загружаем старые сообщения
  }
};


const isOnline = ref(false)


const connectWebSocket = () => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/${props.chat_id}/${props.auth_user_id}`);

  socket.onmessage = async (event) => {
    try {
      const messageObj = JSON.parse(event.data);
      if ("online" in messageObj) {
        if (messageObj.online == true) {
          isOnline.value = true
          props.chat.last_message.is_read = true
        } else {
          isOnline.value = false
        }
        for (let i = 0; i < messages.value.length; i++) {
          if (messages.value[i].user_id_ === props.auth_user_id) {
            if (messages.value[i].is_read === false) {
              messages.value[i].is_read = true
            } else {
              break
            }
          }
        }
        return
      }
      try {
        await axios.patch(`/api/messages/read/${messageObj.id}`)
      } catch (error) {
        console.log(error)
      }
      if (messageObj.image) {
        try {
          const response = await axios.get(`/api/messages/upload/${messageObj.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          messageObj.media = blobUrl
        } catch (error) {
          console.error(error);
        }
      }
      messages.value.unshift(messageObj);
    } catch (error) {
      console.error("Ошибка при разборе JSON:", error);
    }
    scrollToBottom();
    emit('updateLastMessage', props.chat_id)
  };
};

const sendMessage = async () => {
  if (message.value.trim() && socket.readyState === WebSocket.OPEN) {
    const response = await axios.post('/api/messages/', {
      content: message.value,
      chat_id: props.chat_id
    }, { withCredentials: true })
    const messageResp = response.data
    const contentType = response.headers['content-type'];
    if (contentType.startsWith('image/')) {
      messageResp.isImage = true;
    } else {
      messageResp.isImage = false;
    }
    if (isOnline.value === true) {
      messageResp.is_read = true
    }
    messages.value.unshift(messageResp)
    socket.send(JSON.stringify(messageResp));
    message.value = "";
    scrollToBottom();
    emit('updateLastMessage', props.chat_id, isOnline.value)
  }
};

const props = defineProps({
  chat_id: Number,
  auth_user_id: Number,
  user_to_load: Number,
  chat: Object
})


const user = ref(null)
const userImage = ref(null)
const cntUserFollowers = ref(null)
const cntUserFollowing = ref(null)
const checkUserFollow = ref(null)
const showFollowers = ref(null)
const showFollowing = ref(null)


onMounted(async () => {
  try {
    const response = await axios.get(`/api/messages/unread/cnt/${props.chat_id}`, { withCredentials: true })
    cntUnreadMessages.value = response.data
  } catch (error) {
    console.log(error)
  }
  connectWebSocket();
  loadMessages();
  try {
    const response = await axios.get(`/api/users/user_id/${props.user_to_load}`);
    user.value = response.data;

    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;

    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    router.push('/not-found');
  }

  try {
    const response = await axios.get(`/api/subscription/followers/cnt/${user.value.id}`, { withCredentials: true });
    cntUserFollowers.value = response.data;

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/following/cnt/${user.value.id}`, { withCredentials: true });
    cntUserFollowing.value = response.data;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/check_user_follow/${user.value.id}`, { withCredentials: true });
    checkUserFollow.value = response.data;

  } catch (error) {
    console.error(error);
  }
})


onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});

const mediaFile = ref(null)
const mediaPreview = ref(null)
const isImage = ref(false)
const isVideo = ref(false)

function handleMediaUpload(event) {
  const file = event.target.files[0];
  if (file) {
    previewFile(file);
  }
}

const previewFile = (file) => {
  mediaFile.value = file;
  const reader = new FileReader();

  reader.onload = (e) => {
    mediaPreview.value = e.target.result;
  };

  reader.readAsDataURL(file);

  if (file.type.startsWith("image/")) {
    isImage.value = true;
    isVideo.value = false;
  } else if (file.type.startsWith("video/")) {
    isImage.value = false;
    isVideo.value = true;
  }
  openSendMedia.value = true
};

const messageContent = ref('')

async function sendMediaMessage() {
  const response = await axios.post('/api/messages/', {
    content: messageContent.value,
    chat_id: props.chat_id
  }, { withCredentials: true })
  const messageResp = response.data
  try {
    const formData = new FormData();
    formData.append('file', mediaFile.value);

    const response = await axios.post(`/api/messages/upload/${messageResp.id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    const data = response.data
    messageResp.image = data.image

    try {
      const response = await axios.get(`/api/messages/upload/${data.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(response.data);
      messageResp.media = blobUrl
      const contentType = response.headers['content-type'];
      if (contentType.startsWith('image/')) {
        messageResp.isImage = true;
      } else {
        messageResp.isImage = false;
      }
    } catch (error) {
      console.error(error);
    }

    messages.value.unshift(messageResp)
    socket.send(JSON.stringify(messageResp));
    messageContent.value = "";
  } catch (error) {
    console.log(error)
  }
  if (isOnline.value === true) {
      messageResp.is_read = true
      props.chat.last_message.is_read = true
  }
  openSendMedia.value = false
  scrollToBottom();
  emit('updateLastMessage', props.chat_id, isOnline.value)
}

const openSendMedia = ref(false)

async function follow() {
  try {
    const response = await axios.post(`/api/subscription/${user.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = true
  cntUserFollowers.value += 1
}

async function unfollow() {
  try {
    const response = await axios.delete(`/api/subscription/${user.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = false
  cntUserFollowers.value -= 1
}
</script>


<template>

  <transition name="fade" appear>
    <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowersSection :user_id="user.id" :cntUserFollowers="cntUserFollowers" />
      <i @click="showFollowers = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowingSection :user_id="user.id" :cntUserFollowing="cntUserFollowing" />
      <i @click="showFollowing = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="openSendMedia" class="fixed inset-0 bg-black bg-opacity-20 z-50 p-6">

      <div class="flex justify-center">
        <div
          class="flex flex-col  bg-gray-200 h-auto max-h-[670px] text-2xl rounded-3xl  z-50 w-[700px] overflow-y-auto items-center scrollbar-hide">

          <div v-if="isImage" class="relative mt-4">
            <img :src="mediaPreview" class="h-full w-[400px]  rounded-t-2xl" alt="Media Preview" />
          </div>
          <div v-if="isVideo" class="relative mt-4">
            <video :src="mediaPreview" class="h-full w-[400px]  rounded-t-2xl" autoplay loop muted />
          </div>


          <h1 class="text-center text-6xl text-black mt-4">Добавить описание</h1>
          <textarea v-model="messageContent" name="messageContent" id="messageContent"
            class="cursor-pointer text-black text-3xl rounded-3xl block w-3/4 min-h-[100px] max-h-[300px] focus:ring-black bg-white focus:border-4 focus:border-white px-5 py-5" />
          <button @click="sendMediaMessage"
            class="my-5 w-[400px] py-3 bg-white text-black font-semibold rounded-3xl hover:-translate-y-2">
            Отправить
          </button>
        </div>
      </div>

      <i @click="openSendMedia = false"
        class="bg-white rounded-3xl p-5  absolute right-20 top-5 pi pi-times text-black text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-110"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>


  <div class="">
    <div class="flex flex-row">
      <div ref="chatBox" @scroll="handleScroll" id="chatBox"
        class="w-[800px] h-[680px] bg-pink-300  overflow-y-auto p-2 flex flex-col-reverse">
        <div v-for="(message, index) in messages" :key="index" class="flex my-1"
          :class="[message.user_id_ === auth_user_id ? 'justify-end' : '']">
          <div class="flex flex-col  max-w-[400px]  rounded-3xl  bg-white">
            <img v-if="message.media && message.isImage" :src="message.media" class="w-auto h-auto rounded-t-2xl">
            <video v-if="message.media && !message.isImage" :src="message.media" class="w-auto h-auto rounded-t-2xl"
              autoplay loop muted></video>
            <div v-if="message.content" class="mt-4 truncate text-wrap px-4">
              <span class="text-sm text-black ">{{ message.content }}</span>
            </div>
            <div class="flex flex-row items-center m-3 gap-2">
              <span class="text-sm text-gray-500">{{ dayjs(message.created_at).fromNow() }}</span>
              <div v-if="message.user_id_ === auth_user_id" class="flex ml-auto justify-end items-center gap-1">
                <img v-if="message.is_read === false" :src="single_check" alt="Single Check" class="h-4 w-4" />
                <img v-if="message.is_read === true" :src="double_check" alt="Double Check" class="h-4 w-4" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="w-[280px] h-[650px] bg-white flex flex-col items-center justify-start">
        <RouterLink v-if="user" :to="`/user/${user.username}`">
          <img v-if="userImage" :src="userImage" class="rounded-full w-40 h-40 object-cover" />
        </RouterLink>
        <RouterLink v-if="user" :to="`/user/${user.username}`">
          <span v-if="user" class="hover:underline text-2xl truncate px-4">{{ user.username }}</span>
        </RouterLink>
        <span v-if="isOnline" class="text-4xl text-pink-300">Online</span>
        <span v-if="!isOnline" class="text-4xl text-gray-400">Offline</span>
        <div class="flex">
          <button @click="showFollowers = true" v-if="cntUserFollowers"
            class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            {{ cntUserFollowers }} Подпищиков
          </button>
          <button @click="showFollowing = true" v-if="cntUserFollowing"
            class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            {{ cntUserFollowing }} Подписок
          </button>
        </div>
        <button v-if="!checkUserFollow" @click="follow"
          class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
          Подписаться
        </button>
        <button v-if="checkUserFollow" @click="unfollow"
          class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
          Отписаться
        </button>
      </div>
    </div>

    <!-- Поле ввода -->
    <div class="w-[800px] h-[50px] flex relative border-r justify-center items-center">
      <label for="media">
        <i class="absolute top-3 left-0 pi pi-paperclip text-2xl cursor-pointer"></i>
      </label>
      <input type="file" id="media" name="media" accept="image/*,video/*" @change="handleMediaUpload" class="hidden">
      <input id="messageInput" v-model="message" @keyup.enter="sendMessage" placeholder="Write a message..."
        autocomplete="off" class="ml-6 flex-1 p-2 focus:outline-none focus:ring-none focus:ring-none" />
    </div>
  </div>
</template>


<style scoped>
/* Define transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  /* Internet Explorer 10+ */
  scrollbar-width: none;
  /* Firefox */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
}

.fade-in-animation {
  opacity: 0;
  transform: scale(0.95);
  animation: fadeIn 0.3s ease-in-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: scale(1);
  }
}



#chatBox::-webkit-scrollbar {
  width: 5px;
  /* Ширина скроллбара */
}

#chatBox::-webkit-scrollbar-track {
  background: #fefefe;
  /* Фон трека */
  border-radius: 10px;
}

#chatBox::-webkit-scrollbar-thumb {
  background: rgba(28, 17, 21, 0.4);
  /* Цвет ползунка */
  border-radius: 10px;
}
</style>