<script setup>
import axios from 'axios';
import { onMounted, onBeforeUnmount, ref, nextTick } from 'vue';


import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/ru";



dayjs.extend(relativeTime);
dayjs.locale("ru");

let socket;

const chatBox = ref(null);


const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight;
    }
  });
};



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
}

const handleScroll = (event) => {
  const container = event.target;

  // Когда пользователь прокручивает вверх (то есть scrollTop увеличивается)
  if (container.scrollHeight + container.scrollTop < 700) {

    loadMessages(); // Загружаем старые сообщения
  }
};



const connectWebSocket = () => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/${props.chat_id}/${props.auth_user_id}`);

  socket.onmessage = async (event) => {
    try {
      const messageObj = JSON.parse(event.data);
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
    messages.value.unshift(messageResp)
    socket.send(JSON.stringify(messageResp));
    message.value = "";
    scrollToBottom();
  }
};

const props = defineProps({
  chat_id: Number,
  auth_user_id: Number
})


onMounted(async () => {
  connectWebSocket();
  loadMessages()
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
  openSendMedia.value = false
  scrollToBottom();

}

const openSendMedia = ref(false)
</script>


<template>

  <transition name="fade" appear>
    <div v-if="openSendMedia" class="fixed inset-0 bg-black bg-opacity-20 z-50 p-6">

      <div class="flex justify-center">
        <div
          class="flex flex-col  bg-gray-200 h-auto max-h-[670px] text-2xl rounded-3xl  z-50 w-[600px] overflow-y-auto items-center">

          <div v-if="isImage" class="relative mt-4">
            <img :src="mediaPreview" class="h-full w-[400px]  rounded-t-2xl" alt="Media Preview" />
          </div>
          <div v-if="isVideo" class="relative mt-4">
            <video :src="mediaPreview" class="h-full w-[400px]  rounded-t-2xl" autoplay loop muted />
          </div>


          <input id="messageContent" v-model="messageContent" placeholder="Add discription" autocomplete="off"
            class="py-2 px-4 focus:outline-none focus:ring-none focus:ring-none rounded-2xl mt-2 w-[400px]" />
          <button @click="sendMediaMessage"
            class="my-5 w-[400px] py-3 bg-white text-black font-semibold rounded-3xl hover:-translate-y-2">
            Отправить
          </button>
        </div>
      </div>

      <i @click="openSendMedia = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>


  <div class="">


    <!-- Чат -->
    <div ref="chatBox" @scroll="handleScroll" id="chatBox"
      class="w-[1000px] h-[650px] bg-pink-300  overflow-y-auto p-2 flex flex-col-reverse">
      <div v-for="(message, index) in messages" :key="index" class="flex my-1"
        :class="[message.user_id_ === auth_user_id ? 'justify-end' : '']">
        <div class="flex flex-col  max-w-[400px]  rounded-3xl  bg-white">
          <img v-if="message.media && message.isImage" :src="message.media" class="w-auto h-auto rounded-t-2xl">
          <video v-if="message.media && !message.isImage" :src="message.media" class="w-auto h-auto rounded-t-2xl"
            autoplay loop muted></video>
          <div v-if="message.content" class="mt-4 truncate text-wrap px-4">
            <span class="text-sm text-black ">{{ message.content }}</span>
          </div>
          <span class="text-sm text-gray-700 px-4 py-2">{{ dayjs(message.created_at).fromNow() }}</span>
        </div>
      </div>
    </div>

    <!-- Поле ввода -->
    <div class="w-[1000px] flex mt-4 relative">
      <label for="media">
        <i class="absolute top-2 left-0 pi pi-paperclip text-2xl cursor-pointer"></i>
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