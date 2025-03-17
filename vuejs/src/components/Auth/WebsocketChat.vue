<script setup>
import axios from 'axios';
import { onMounted, onBeforeUnmount, ref, nextTick, watch, computed } from 'vue';
import FollowersSection from './FollowersSection.vue';
import FollowingSection from './FollowingSection.vue';
import { RouterLink, useRoute } from 'vue-router';
import double_check from '@/assets/double_check.png';
import single_check from '@/assets/single_check.png';
import EmojiPicker from 'vue3-emoji-picker'
import 'vue3-emoji-picker/css'


import { useUnreadMessagesStore } from "@/stores/unreadMessages";
const unreadMessagesStore = useUnreadMessagesStore();

import { useChatStore } from "@/stores/useChatStore";


const isNewDay = (index) => {
  if (index === messages.value.length - 1) return true;
  const currentDate = dayjs(messages.value[index].created_at).format('YYYY-MM-DD');
  const previousDate = dayjs(messages.value[index + 1].created_at).format('YYYY-MM-DD');
  return currentDate !== previousDate;
};


const chatStore = useChatStore();

const route = useRoute()

const imageLoaded = ref(false)
const sectionLoaded = ref(false)

import ClipLoader from 'vue-spinner/src/ClipLoader.vue'

const color = ref('red')
const size = ref('100px')

function onSelectEmoji(emoji) {
  message.value += emoji.i
}

const showPicker = ref(false)

const colorMap = {
  red: { track: "#fca5a5", thumb: "#ef4444" }, // bg-red-300 / bg-red-500
  blue: { track: "#93c5fd", thumb: "#3b82f6" }, // bg-blue-300 / bg-blue-500
  lime: { track: "#bef264", thumb: "#84cc16" }, // bg-lime-300 / bg-lime-500
  yellow: { track: "#fde047", thumb: "#eab308" }, // bg-yellow-300 / bg-yellow-500
  purple: { track: "#d8b4fe", thumb: "#a855f7" } // bg-purple-300 / bg-purple-500
};

watch(() => chatStore.bgColor, (newColor) => {
  if (colorMap[newColor]) {
    document.documentElement.style.setProperty("--scrollbar-track-bg", colorMap[newColor].track);
    document.documentElement.style.setProperty("--scrollbar-thumb-bg", colorMap[newColor].thumb);
    document.documentElement.style.setProperty("--selection-bg", colorMap[newColor].thumb); // Добавляем изменение цвета выделения
  }
}, { immediate: true });


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
const isTyping = ref(false)
let typingTimeout = null;

const isSendingMedia = ref(false)

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

// Вычисляем оставшееся время для каждого сообщения
const formattedTimeRemaining = (message) => {
  return computed(() => {
    if (!message.videoDuration) return "0:00"; // Если нет данных о длительности, вернуть "0:00"
    const timeRemaining = Math.max(message.videoDuration - message.currentTime, 0);
    return formatTime(timeRemaining);
  });
};

// Функция обновления текущего времени видео
const onTimeUpdate = (message, event) => {
  message.currentTime = event.target.currentTime;
};

// Функция загрузки видео
const onVideoLoad = (message, event) => {
  message.videoDuration = event.target.duration; // Получаем продолжительность видео
};


watch(message, (newValue, oldValue) => {
  if (newValue.trim() !== '') {
    isTyping.value = true;

    // Сбрасываем предыдущий таймер, если он есть
    if (typingTimeout) clearTimeout(typingTimeout);

    // Устанавливаем новый таймер на 2 секунды
    typingTimeout = setTimeout(() => {
      isTyping.value = false;
    }, 2000);
  } else {
    if (oldValue.trim() !== '') {
      isTyping.value = false;
    }
  }
});

watch(isTyping, (newValue) => {
  if (newValue) {
    socket.send(JSON.stringify({ 'user_start_typing': true }));
  } else {
    socket.send(JSON.stringify({ 'user_stop_typing': true }));
  }
});



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
          if (cntUnreadMessages.value === 0) {
            socket.send(JSON.stringify({ 'user_read_messages': true }));
          }
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
            messagesTemp.value[i].videPlayer = null
            messagesTemp.value[i].videoLoaded = false
            messagesTemp.value[i].videoDuration = 0
            messagesTemp.value[i].currentTime = 0
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

const typing = ref(false)


const connectWebSocket = () => {
  socket = new WebSocket(`/ws/${props.chat_id}/${props.auth_user_id}`);

  socket.onmessage = async (event) => {
    let showToast = false
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
      if ("user_start_sending_media" in messageObj) {
        isSendingMedia.value = true
        return
      }
      if ("user_stop_sending_media" in messageObj) {
        isSendingMedia.value = false
        return
      }
      if ("user_start_typing" in messageObj) {
        typing.value = true
        return
      }
      if ("user_stop_typing" in messageObj) {
        typing.value = false
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
      if (route.name !== 'messages') {
        showToast = true
      }
    } catch (error) {
      console.error("Ошибка при разборе JSON:", error);
    }
    scrollToBottom();
    emit('updateLastMessage', showToast, props.chat_id)
  };
};

const sendMessage = async () => {
  if (message.value.trim() && socket.readyState === WebSocket.OPEN) {
    showPicker.value = false
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
    emit('updateLastMessage', false, props.chat_id, isOnline.value)
  }
};

const props = defineProps({
  chat_id: Number,
  auth_user_id: Number,
  user_to_load: Number,
  chat: Object,
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
    const response = await axios.get(`/api/subscription/followers/cnt/${props.chat.user.id}`, { withCredentials: true });
    cntUserFollowers.value = response.data;

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/following/cnt/${props.chat.user.id}`, { withCredentials: true });
    cntUserFollowing.value = response.data;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/check_user_follow/${props.chat.user.id}`, { withCredentials: true });
    checkUserFollow.value = response.data;

  } catch (error) {
    console.error(error);
  }
  sectionLoaded.value = true
})


onBeforeUnmount(() => {
  if (socket) {
    socket.send(JSON.stringify({ 'user_stop_typing': true }));
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

  socket.send(JSON.stringify({ 'user_start_sending_media': true }));

  const formData = new FormData();
  formData.append("file", mediaFile.value); // Файл

  const jsonData = JSON.stringify({
    content: messageContent.value,
    chat_id: props.chat_id
  });

  formData.append("message", jsonData); // Передаем строку, а не Blob

  const response = await axios.post("/api/messages/create-message-entity", formData, {
    withCredentials: true,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  const messageResp = response.data


  // const response = await axios.post('/api/messages/', {
  //   content: messageContent.value,
  //   chat_id: props.chat_id
  // }, { withCredentials: true })

  // const messageResp = response.data

  // const formData = new FormData();
  // formData.append('file', mediaFile.value);

  // const response = await axios.post(`/api/messages/upload/${messageResp.id}`, formData, {
  //   headers: {
  //     'Content-Type': 'multipart/form-data',
  //   },
  // });


  // const data = response.data
  // messageResp.image = data.image

  try {
    const response = await axios.get(`/api/messages/upload/${messageResp.id}`, { responseType: 'blob' });
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
  socket.send(JSON.stringify({ 'user_stop_sending_media': true }));
  messageContent.value = "";

  openSendMedia.value = false
  mediaPreview.value = null;
  showPreview.value = false

  if (isOnline.value === true) {
    messageResp.is_read = true
    props.chat.last_message.is_read = true
  }
  scrollToBottom();
  emit('updateLastMessage', false, props.chat_id, isOnline.value)
}

const openSendMedia = ref(false)

async function follow() {
  try {
    const response = await axios.post(`/api/subscription/${props.chat.user.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = true
  cntUserFollowers.value += 1
}

async function unfollow() {
  try {
    const response = await axios.delete(`/api/subscription/${props.chat.user.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = false
  cntUserFollowers.value -= 1
}

async function updateColor(color) {
  try {
    await axios.patch(`/api/chats/color?color=${color}`)
    chatStore.setChatColor(color)
  } catch (error) {
    console.log(error)
  }
}

const startResize = (event) => {
  const startX = event.clientX;
  const startWidth = chatStore.size;

  // Отключаем выделение текста
  document.body.style.userSelect = "none";

  const onMouseMove = (moveEvent) => {
    let newWidth = startWidth + (moveEvent.clientX - startX);
    newWidth = Math.max(200, Math.min(newWidth, 800));

    if (newWidth === 200) {
      newWidth = 80;
    }

    chatStore.size = newWidth;
  };

  const onMouseUp = async () => {
    try {
      await axios.patch(`/api/chats/size?size=${chatStore.size}`)
    } catch (error) {
      console.log(error)
    }
    window.removeEventListener("mousemove", onMouseMove);
    window.removeEventListener("mouseup", onMouseUp);

    document.body.style.userSelect = "";
  };

  window.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
};

async function updateSide(side) {
  try {
    await axios.patch(`/api/chats/side?side=${side}`)
    chatStore.side = side
  } catch (error) {
    console.log(error)
  }
}

const showPreview = ref(false)

const fullscreenImage = ref(null);

const videoElement = ref(null);

const openFullscreen = (imageSrc) => {
  fullscreenImage.value = imageSrc;
};


const closeFullscreen = () => {
  fullscreenImage.value = null;
};


const fullscreenVideo = ref(null);

const openFullscreenVideo = (videoSrc) => {
  fullscreenVideo.value = videoSrc;
};

const closeFullscreenVideo = () => {
  fullscreenVideo.value = null;
};

const setVolume = () => {
  if (videoElement.value) {
    videoElement.value.volume = 0.5;
  }
};

function showVideo(message) {
  message.loaded = true
}


</script>


<template>

  <transition name="fade" appear>
    <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowersSection :user_id="chat.user.id" :cntUserFollowers="cntUserFollowers" />
      <i @click="showFollowers = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowingSection :user_id="chat.user.id" :cntUserFollowing="cntUserFollowing" />
      <i @click="showFollowing = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>

  <transition name="fade2" appear>
    <div v-if="openSendMedia" class="fixed inset-0 bg-black bg-opacity-50 z-50">

      <div
        class="flex items-center justify-center flex-col bg-white mx-[540px] rounded-xl mt-2 max-h-screen overflow-y-auto">
        <div v-if="isImage" class=" ">
          <img v-show="showPreview === true" :src="mediaPreview"
            class="h-full w-[400px] max-h-[570px] object-contain rounded-t-xl mt-4" @load="showPreview = true"
            alt="Media Preview" />
          <div v-show="showPreview === false" class="h-[500px] w-[400px] max-h-[570px] rounded-t-xl mt-4 bg-white">
          </div>
        </div>
        <div v-if="isVideo" class=" ">
          <video v-show="showPreview === true" :src="mediaPreview"
            class="h-full w-[400px] max-h-[570px] object-contain  rounded-t-xl mt-4" @loadeddata="showPreview = true"
            autoplay loop muted />
          <div v-show="showPreview === false" class="h-[500px] w-[400px] max-h-[570px] rounded-t-xl mt-4 bg-white">
          </div>
        </div>
        <input id="messageInput" v-model="messageContent" placeholder="Add caption..." autofocus autocomplete="off"
          :class="`border-${chatStore.bgColor}-600`"
          class="mt-4 py-2 focus:outline-none focus:ring-none focus:ring-none w-[400px] border-b-2" />
        <div class="w-[400px]">
          <div class="flex flex-row items-center justify-end w-full mt-4 gap-4 mb-2">
            <button @click="openSendMedia = false; mediaPreview = null; showPreview = false"
              :class="`text-${chatStore.bgColor}-600 hover:bg-${chatStore.bgColor}-200`"
              class="bg-white   rounded-xl py-2 px-3">Cancel</button>
            <button @click="sendMediaMessage" :class="`text-${chatStore.bgColor}-600 hover:bg-${chatStore.bgColor}-200`"
              class="bg-white   rounded-xl py-2 px-3">Send</button>
          </div>
        </div>
      </div>
    </div>
  </transition>

  <div v-if="fullscreenImage" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
    @click="closeFullscreen">

    <!-- Изображение: предотвращаем закрытие при клике на него -->
    <img :src="fullscreenImage" class="max-w-full max-h-full" @click.stop />

    <!-- Кнопка закрытия -->
    <button @click="closeFullscreen"
      class="absolute top-4 right-4 text-gray-300 text-3xl font-bold cursor-pointer hover:text-white">
      ✕
    </button>
  </div>

  <div v-if="fullscreenVideo" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
    @click="closeFullscreenVideo">

    <!-- Видео: предотвращаем закрытие при клике на него -->
    <video ref="videoElement" :src="fullscreenVideo" class="w-auto h-auto max-w-full max-h-full rounded-lg" autoplay
      loop controls @click.stop>
    </video>

    <!-- Кнопка закрытия -->
    <button @click="closeFullscreenVideo"
      class="absolute top-4 right-4 text-gray-300 text-3xl font-bold cursor-pointer hover:text-white">
      ✕
    </button>
  </div>

  <div id="websocket-chat" class="">
    <div class="flex flex-row">
      <div class="absolute left-[-10px] bottom-0 top-0 w-5 cursor-ew-resize bg-transparen" @mousedown="startResize">
      </div>
      <div
        class="absolute z-30 top-0 left-0 transform h-[50px] flex items-center justify-between shadow-sm bg-white border-x border-gray-300 px-4"
        :style="{ width: !chatStore.side ? `calc(100vw - ${chatStore.size + 80}px)` : `calc(83vw - ${chatStore.size + 80}px)` }">
        <div class="flex flex-col">
          <span class="text-md"> {{ chat.user.username }}</span>
          <span v-show="!typing && !isSendingMedia" v-if="isOnline" class="text-md" :class="`text-${chatStore.bgColor}-500`">online</span>
          <span v-show="!typing && !isSendingMedia" v-if="!isOnline" class="text-gray-500 text-md">last seen recently</span>
          <span v-show="typing === true && !isSendingMedia" :class="`text-${chatStore.bgColor}-500`"
            class="text-md typing-animation">typing</span>
          <span v-show="isSendingMedia" :class="`text-${chatStore.bgColor}-500`"
            class="text-md typing-animation">sending media</span>
        </div>
        <i v-show="!chatStore.side" @click="updateSide(true)"
          class="pi pi-angle-left w-5 h-5 text-gray-400 hover:text-gray-600 cursor-pointer text-2xl"></i>
        <i v-show="chatStore.side" @click="updateSide(false)"
          class="pi pi-angle-right w-5 h-5 text-gray-400 hover:text-gray-600 cursor-pointer text-2xl"></i>
      </div>

      <div ref="chatBox" @scroll="handleScroll" id="chatBox"
        class="w-[800px] h-[630px]  overflow-y-auto p-1 flex flex-col-reverse mt-[50px] relative"
        :class="`bg-${chatStore.bgColor}-300`"
        :style="{ width: !chatStore.side ? `calc(100vw - ${chatStore.size + 80}px)` : `calc(83vw - ${chatStore.size + 80}px)` }">


        <div v-for="(message, index) in messages" :key="message.id" class="w-full">
          <!-- Если новый день, выводим разделитель с датой -->
          <div v-if="isNewDay(index)" class="text-center my-2 z-10">
            <span class="bg-white px-2 py-1 rounded-full text-xs inline-block">
              {{ dayjs(message.created_at).format('D MMM') }}
            </span>
          </div>

          <!-- Само сообщение -->
          <div class="flex my-1" :class="[message.user_id_ === auth_user_id ? 'justify-end' : 'justify-start']">
            <div class="relative flex flex-col max-w-[400px] bg-white"
              :class="message.user_id_ === auth_user_id ? 'rounded-t-3xl rounded-l-3xl' : 'rounded-t-3xl rounded-r-3xl'">
              <!-- Изображение -->
              <img v-if="message.media && message.isImage" :src="message.media"
                class="w-auto h-auto max-h-[500px] rounded-t-2xl cursor-pointer"
                @click="openFullscreen(message.media)" />

              <!-- Видео -->
              <div class="relative">
                <div v-if="message.videoDuration"
                  class="absolute top-2 left-2 bg-gray-100 text-black rounded-2xl px-3 py-1 text-sm">
                  {{ formattedTimeRemaining(message).value }}
                </div>
                <video :ref="el => { if (el) message.videoPlayer = el; }" @loadeddata="onVideoLoad(message, $event)"
                  @timeupdate="onTimeUpdate(message, $event)" v-if="message.media && !message.isImage"
                  :src="message.media" class="w-auto h-auto max-h-[500px] rounded-t-2xl cursor-pointer" autoplay loop
                  muted @click="openFullscreenVideo(message.media)">
                </video>
              </div>


              <!-- Текст сообщения -->
              <div v-if="message.content" class="mt-2 text-wrap px-2">
                <span class="text-sm text-black">{{ message.content }}</span>
              </div>

              <!-- Время и статус сообщения -->
              <div class="flex flex-row items-center ml-4 gap-1">
                <span class="text-sm text-gray-500 flex ml-auto justify-end">{{
                  dayjs(message.created_at).format('HH:mm') }}</span>
                <div v-if="message.user_id_ === auth_user_id" class="items-center gap-1 mr-1">
                  <img v-if="message.is_read === false" :src="single_check" alt="Single Check" class="h-4 w-4" />
                  <img v-if="message.is_read === true" :src="double_check" alt="Double Check" class="h-4 w-4" />
                </div>
                <div v-else class="mr-4"></div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div v-show="chatStore.side" id="user-info" class="w-[280px] h-[650px] bg-white flex flex-col">
        <div class="flex items-center space-x-2 justify-center ml-2 mr-4">
          <!-- Аватар -->
          <RouterLink :to="`/user/${chat.user.username}`">
            <img :src="chat.userImage" class="rounded-full w-24 h-24 object-cover flex-shrink-0" />
          </RouterLink>

          <!-- Информация о пользователе -->
          <div class="flex flex-col flex-1 min-w-0">
            <RouterLink :to="`/user/${chat.user.username}`">
              <span class="hover:underline text-xl truncate block">{{ chat.user.username }}</span>
            </RouterLink>

            <span v-if="isOnline" class="text-md" :class="`text-${chatStore.bgColor}-500`">online</span>
            <span v-if="!isOnline" class="text-gray-500 text-md">last seen recently</span>
          </div>
        </div>

        <!-- Подписчики и подписки -->
        <div v-show="sectionLoaded" v-if="cntUserFollowers || cntUserFollowing"
          class="flex items-center justify-start space-x-2 text-sm mt-3 ml-2">
          <i class="pi pi-users text-xl"></i>
          <button :class="`hover:text-${chatStore.bgColor}-500`" class="hover:underline" @click="showFollowers = true"
            v-if="cntUserFollowers">{{ cntUserFollowers }} Followers</button>
          <button :class="`hover:text-${chatStore.bgColor}-500`" class="hover:underline" @click="showFollowing = true"
            v-if="cntUserFollowing">{{ cntUserFollowing }} Following</button>
        </div>

        <!-- Описание (переместил ниже подписчиков) -->
        <span v-show="sectionLoaded" v-if="chat.user.description"
          class="text-gray-800 text-sm line-clamp-2 mr-4 mt-3 ml-2">
          {{ chat.user.description }}
        </span>

        <!-- Кнопки Follow/Unfollow -->
        <button v-show="sectionLoaded" v-if="!checkUserFollow" @click="follow"
          :class="[`bg-${chatStore.bgColor}-300`, `hover:bg-${chatStore.bgColor}-400`]"
          class="px-6 py-2 text-black   transition mt-3">
          follow
        </button>
        <button v-if="checkUserFollow" @click="unfollow"
          :class="[`bg-${chatStore.bgColor}-300`, `hover:bg-${chatStore.bgColor}-400`]"
          class="px-6 py-2 text-black   transition mt-3">
          unfollow
        </button>

        <ClipLoader v-show="!sectionLoaded" :color="color" :size="size"
          class="flex items-center justify-center h-96 font-extrabold" />

        <!-- Выбор цвета -->
        <div class="flex space-x-2 mt-auto pb-4 justify-center">
          <div @click="updateColor('red')" class="w-6 h-6 rounded-full bg-red-300 cursor-pointer"></div>
          <div @click="updateColor('blue')" class="w-6 h-6 rounded-full bg-blue-300 cursor-pointer"></div>
          <div @click="updateColor('lime')" class="w-6 h-6 rounded-full bg-lime-300 cursor-pointer"></div>
          <div @click="updateColor('yellow')" class="w-6 h-6 rounded-full bg-yellow-300 cursor-pointer"></div>
          <div @click="updateColor('purple')" class="w-6 h-6 rounded-full bg-purple-300 cursor-pointer"></div>
        </div>
      </div>
    </div>



    <!-- Поле ввода -->
    <div class=" h-[50px] flex relative justify-center items-center border-x border-gray-300"
      :style="{ width: !chatStore.side ? `calc(100vw - ${chatStore.size + 80}px)` : `calc(83vw - ${chatStore.size + 80}px)` }">
      <label for="media">
        <i class="absolute top-0 left-0 pi pi-paperclip text-2xl cursor-pointer px-2 py-3"></i>
      </label>
      <input type="file" id="media" name="media" accept="image/*,video/*" @change="handleMediaUpload" class="hidden">
      <input id="messageInput" v-model="message" @keyup.enter="sendMessage" placeholder="Write a message..." autofocus
        autocomplete="off" class="ml-10 flex-1 py-2 focus:outline-none focus:ring-none focus:ring-none" />
      <EmojiPicker v-show="showPicker" :native="true" @select="onSelectEmoji" class="absolute bottom-10 right-0" />
      <button @click="showPicker = !showPicker" class="p-5">
        <!-- Смайлик в SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6">
          <circle cx="12" cy="12" r="10" fill="#FFEB3B" />
          <circle cx="9" cy="9" r="1.5" fill="black" />
          <circle cx="15" cy="9" r="1.5" fill="black" />
          <path d="M8 15c1.5 1 4.5 1 6 0" stroke="black" />
        </svg>
      </button>
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

.fade2-enter-active,
.fade2-leave-active {
  transition: opacity 0.4s ease;
}

.fade2-enter-from,
.fade2-leave-to {
  opacity: 0;
}


#chatBox::-webkit-scrollbar {
  width: 5px;
}

#chatBox::-webkit-scrollbar-track {
  background: var(--scrollbar-track-bg);
  /* ✅ Работает с Tailwind */
  border-radius: 10px;
}

#chatBox::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb-bg);
  /* ✅ Работает с Tailwind */
  border-radius: 10px;
}


#user-info {
  user-select: none;
  /* Отключает выделение */
}

/* Для Firefox */
#user-info ::-moz-selection {
  background: transparent;
  color: inherit;
}

/* Для Chrome, Edge, Safari */
#user-info ::selection {
  background: transparent;
  color: inherit;
}

#websocket-chat ::selection {
  background: var(--selection-bg);
  /* Цвет фона выделения */
  color: white;
  /* Цвет текста */
}

#websocket-chat ::-moz-selection {
  background: var(--selection-bg);
  /* Для Firefox */
  color: white;
}

.typing-animation::after {
  content: ' .';
  animation: dots 1.5s infinite steps(3);
}

@keyframes dots {
  0% {
    content: ' .';
  }

  33% {
    content: ' ..';
  }

  66% {
    content: ' ...';
  }

  100% {
    content: ' .';
  }
}
</style>
