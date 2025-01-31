<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const user = ref(null)
const userImage = ref(null)
const userId = ref(null)

const props = defineProps({
  chat: Object,
  auth_user_id: Number
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
  <div class="flex items-center space-x-2 cursor-pointer" :class="[props.chat.selected ? 'bg-pink-300' : 'hover:bg-gray-200']">
    <img v-if="userImage" :src="userImage" alt="User Image" class="w-[60px] h-[60px] rounded-full object-cover m-2" />
    <span v-if="user" class="truncate">{{ user.username }}</span>
  </div>
</template>