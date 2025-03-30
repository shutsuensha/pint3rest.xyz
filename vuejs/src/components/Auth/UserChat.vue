<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import double_check from '@/assets/double_check.png';
import single_check from '@/assets/single_check.png';

import dayjs from 'dayjs';
import isToday from 'dayjs/plugin/isToday';
import isYesterday from 'dayjs/plugin/isYesterday';
import 'dayjs/locale/en'; // Use the English locale

import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc"; // Adding UTC support
import timezone from "dayjs/plugin/timezone"; // Adding timezone support

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("en"); // Set the English locale

import { useChatStore } from "@/stores/useChatStore";

const chatStore = useChatStore();

dayjs.extend(isToday);
dayjs.extend(isYesterday);

const formattedTime = (timestamp) => {
  const date = dayjs.utc(timestamp).local(); // Convert to local time
  const now = dayjs();

  return date.isToday()
    ? date.format('HH:mm') // Display time in 'HH:mm' format
    : date.isYesterday()
      ? 'Yesterday' // Translation to English
      : now.diff(date.startOf('day'), 'days') > 7
        ? date.format('MMM D') // Format like 'Apr 15'
        : date.format('ddd'); // Shortened day of the week
}



const props = defineProps({
  chat: Object,
  auth_user_id: Number,
})

const showChat = ref(false)
</script>


<template>
  <div class="flex items-center space-x-1 cursor-pointer"
    :class="[props.chat.selected ? `bg-${chatStore.bgColor}-400` : 'hover:bg-gray-200']">

    <!-- Аватар пользователя -->
    <div class="relative flex-none">
      <img :src="chat.userImage" alt="User Image"
        class="w-[60px] h-[60px] min-w-[60px] min-h-[60px] rounded-full object-cover m-2" />
      <div :class="`bg-${chatStore.bgColor}-500`" v-if="chat.online"
        class="absolute bottom-2 right-3  w-3 h-3 rounded-full border-2 border-white">
      </div>
    </div>

    <!-- Информация о чате -->
    <div class="flex flex-col w-full min-w-0 gap-1">
      <div class="flex justify-between items-center w-full min-w-0">
        <!-- Имя пользователя с truncate -->
        <span class="w-0 flex-1 truncate">{{ chat.user.username }}</span>

        <!-- Время последнего сообщения -->
        <span v-if="chat.last_message" class="text-sm text-gray-700 text-nowrap mr-1">
          {{ formattedTime(chat.last_message.created_at) }}
        </span>
      </div>

      <div v-show="!chat.typing && !chat.isSendingMedia" class="flex items-center min-w-0">
        <!-- Миниатюра изображения -->
        <img v-if="chat.last_message?.media && chat.last_message.isImage" :src="chat.last_message.media"
          class="w-5 h-5 min-w-5 min-h-5 flex-none" />

        <!-- Миниатюра видео -->
        <video v-if="chat.last_message?.media && !chat.last_message.isImage" :src="chat.last_message.media"
          class="w-5 h-5 min-w-5 min-h-5 flex-none" autoplay muted loop></video>

        <!-- Текст сообщения с truncate -->
        <span v-if="chat.last_message?.content" :class="chat.last_message?.media ? 'ml-1' : ''"
          class="w-0 flex-1 truncate text-sm text-gray-700">
          {{ chat.last_message.content }}
        </span>

        <!-- Если сообщение - фото -->
        <span
          v-if="chat.last_message?.media && chat.last_message.isImage && !chat.last_message.content && !chat.last_message.isGif"
          class="ml-1 text-sm text-gray-700">Photo</span>

        <span
          v-if="chat.last_message?.media && chat.last_message.isImage && !chat.last_message.content && chat.last_message.isGif"
          class="ml-1 text-sm text-gray-700">Gif</span>

        <!-- Если сообщение - видео -->
        <span v-if="chat.last_message?.media && !chat.last_message.isImage && !chat.last_message.content"
          class="ml-1 text-sm text-gray-700">Video</span>

        <!-- Количество непрочитанных сообщений -->
        <span v-if="chat.cntUnreadMessages" :class="`bg-${chatStore.bgColor}-400`"
          class="ml-auto flex items-center justify-center text-white text-xs font-bold rounded-full h-5 w-5 mr-3">
          {{ chat.cntUnreadMessages }}
        </span>

        <!-- Статус сообщения (прочитано/непрочитано) -->
        <div v-if="chat.last_message?.user_id_ === auth_user_id"
          class="flex ml-auto justify-end items-center gap-1 mr-2">
          <img v-if="chat.last_message.is_read === false" :src="single_check" alt="Single Check"
            class="h-4 w-4 flex-none" />
          <img v-if="chat.last_message.is_read === true" :src="double_check" alt="Double Check"
            class="h-4 w-4 flex-none" />
        </div>
      </div>
      <div v-show="chat.typing && chat.typing === true && !chat.isSendingMedia" class="flex items-center min-w-0">
        <span class="text-gray-700 text-sm typing-animation">typing</span>
      </div>
      <div v-show="chat.isSendingMedia" class="flex items-center min-w-0">
        <span class="text-gray-700 text-sm sending-animation">📤 sending media</span>
      </div>
    </div>
  </div>


</template>

<style scoped>
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


@keyframes sending-file {
  0% {
    transform: translateX(0);
    opacity: 0.5;
  }
  50% {
    transform: translateX(10px);
    opacity: 1;
  }
  100% {
    transform: translateX(0);
    opacity: 0.5;
  }
}

.sending-animation {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  animation: sending-file 1s infinite ease-in-out;
}

.sending-animation::after {
  content: "📤"; /* Иконка отправки */
  animation: sending-file 1s infinite ease-in-out;
}
</style>