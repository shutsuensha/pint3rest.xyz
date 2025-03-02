<script setup>
import dayjs from 'dayjs';
import isToday from 'dayjs/plugin/isToday';
import isYesterday from 'dayjs/plugin/isYesterday';
import 'dayjs/locale/ru';

import { useChatStore } from "@/stores/useChatStore";

const chatStore = useChatStore();


const emit = defineEmits(['MyClick']);

dayjs.extend(isToday);
dayjs.extend(isYesterday);

const formattedTime = (timestamp) => {
    const date = dayjs(timestamp);
    const now = dayjs();

    return date.isToday()
        ? date.format('HH:mm')
        : date.isYesterday()
            ? 'Вчера'
            : now.diff(date.startOf('day'), 'days') > 7
                ? date.format('DD.MM') 
                : date.format('dddd');
};

const props = defineProps({
  chat: Object
});


</script>

<template>
  <div class="flex items-center space-x-1 cursor-pointer" @click="emit('MyClick')"
  :class="`bg-${chatStore.bgColor}-400`">

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

      <div v-show="!chat.typing" class="flex items-center min-w-0">
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
        <span v-if="chat.cntUnreadMessages" :class="`bg-${chatStore.bgColor}-500`"
          class="ml-auto flex items-center justify-center text-white text-xs font-bold rounded-full h-5 w-5 mr-3">
          {{ chat.cntUnreadMessages }}
        </span>
      </div>
    </div>
  </div>
</template>