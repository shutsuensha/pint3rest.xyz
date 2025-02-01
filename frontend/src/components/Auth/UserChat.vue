<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/ru";



dayjs.extend(relativeTime);
dayjs.locale("ru");


const user = ref(null)
const userImage = ref(null)
const userId = ref(null)

const props = defineProps({
  chat: Object,
  auth_user_id: Number,
})


onMounted(async () => {
  userId.value = props.chat.user_1_id === props.auth_user_id ? props.chat.user_2_id : props.chat.user_1_id
  try {
    const response = await axios.get(`/api/users/user_id/${userId.value}`, { withCredentials: true })
    user.value = response.data
  } catch (error) {
    console.error(error)
  }
  try {
    const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
    const blobUrl = URL.createObjectURL(userResponse.data);
    userImage.value = blobUrl;

  } catch (error) {
    console.error(error);
  }
})

const showChat = ref(false)
</script>


<template>
  <div class="flex items-center space-x-2 cursor-pointer"
    :class="[props.chat.selected ? 'bg-pink-300' : 'hover:bg-gray-200']">
    <img v-if="userImage" :src="userImage" alt="User Image"   class="w-[60px] h-[60px] rounded-full object-cover flex-shrink-0 m-2"    />
    <div class="flex flex-col w-full gap-1">
      <div class="flex flex-row justify-between items-center w-full">
        <span v-if="user" class="truncate flex-1">{{ user.username }}</span>
        <span v-if="chat.last_message" class="text-sm text-gray-700 truncate text-nowrap mr-2">{{ dayjs(chat.last_message.created_at).format('HH:mm') }}</span>
      </div>
      <div class="flex flex-row items-center">
        <div>
          <img v-if="chat.last_message && chat.last_message.media && chat.last_message.isImage" :src="chat.last_message.media" class="h-5 w-5"/>
        </div>
        <div>
          <video v-if="chat.last_message && chat.last_message.media && !chat.last_message.isImage" :src="chat.last_message.media" class="h-5 w-5" autoplay muted loop></video>
        </div>
        <span v-if="chat.last_message && chat.last_message.content" :class="[chat.last_message && chat.last_message.media ? 'ml-1':'']" class="text-sm text-gray-700 max-w-[200px] truncate">{{ chat.last_message.content }}</span>
        <span v-if="chat.last_message && !chat.last_message.content && chat.last_message.media && chat.last_message.isImage" class="ml-1 text-sm text-gray-700">Photo</span>
        <span v-if="chat.last_message && !chat.last_message.content && chat.last_message.media && !chat.last_message.isImage" class="ml-1 text-sm text-gray-700">Video</span>
      </div>
    </div>
  </div>
</template>