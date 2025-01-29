<script setup>
import axios from 'axios';
import { onMounted, onBeforeUnmount, ref } from 'vue';

let socket; 


const messages = ref([]); 
const message = ref(""); 

const connectWebSocket = () => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/${props.chat_id}/${props.auth_user_id}`);

  socket.onmessage = (event) => {
    messages.value.push(event.data); // Добавление нового сообщения
  };

  socket.onerror = (error) => {
    console.error("WebSocket Error:", error);
  };

  socket.onclose = () => {
    console.warn("WebSocket connection closed.");
  };
};

const sendMessage = async () => {
  if (message.value.trim() && socket.readyState === WebSocket.OPEN) {
    socket.send(message.value);
    const response = await axios.post('/api/messages/', {
      content: message.value,
      chat_id: props.chat_id
    }, {withCredentials: true})
    message.value = ""; 
  }
};



const props = defineProps({
  chat_id: Number,
  auth_user_id: Number
})


onMounted(async ()=> {
  try {
    const response = await axios.get(`/api/messages/history/${props.chat_id}`, {withCredentials: true})
    console.log(response.data)
  } catch (error) {
    console.error(error)
  }
  connectWebSocket(); 
})


onBeforeUnmount(() => {
  if (socket) {
    socket.close(); 
  }
});
</script>


<template>
  <div class="flex flex-col items-center p-6">
    <!-- Чат -->
    <div
      id="chatBox"
      class="w-full max-w-lg h-80 bg-gray-100 border border-gray-300 rounded-lg overflow-y-auto p-4"
    >
      <div v-for="(message, index) in messages" :key="index" class="mb-2">
        <span class="text-sm text-gray-700">{{ message }}</span>
      </div>
    </div>

    <!-- Поле ввода -->
    <div class="w-full max-w-lg flex mt-4">
      <input
        id="messageInput"
        v-model="message"
        @keyup.enter="sendMessage"
        placeholder="Введите сообщение"
        class="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="sendMessage"
        class="ml-2 px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition"
      >
        Отправить
      </button>
    </div>
  </div>
</template>