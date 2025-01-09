<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'

const props = defineProps({
  pin_id: Number
})

const users = ref([])

const offset = ref(0);
const limit = ref(5);

const isPinsLoading = ref(false);

async function loadUsers() {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/likes/pin/likes/${props.pin_id}`, { params: { offset: offset.value, limit: limit.value } })
    const data = response.data
    for (let i = 0; i < data.length; i++) {
      try {
        const response = await axios.get(`/api/users/user_id/${data[i].user_id}`)
        const userData = response.data
        let userImage = null
        try {
          const userResponse = await axios.get(`/api/users/upload/${userData.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(userResponse.data);
          userImage = blobUrl;
        } catch (error) {
          console.error(error);
        }
        users.value.push({ id: userData.id, username: userData.username, image: userImage })
      } catch (error) {
        console.error(error)
      }
    }
  } catch (error) {
    console.error(error)
  }
  offset.value += limit.value;
  isPinsLoading.value = false;
}

const handleScroll = (event) => {
  const container = event.target;
  if (container.scrollTop + container.clientHeight >= container.scrollHeight - 10) {
    loadUsers();
  }
};

onMounted(() => {
  loadUsers();  // Initial load
});
</script>


<template>
  <div @scroll="handleScroll"
    class="flex flex-col gap-4 bg-white shadow-2xl rounded-xl text-sm font-medium text-gray-700 z-30 h-32 w-60 overflow-y-auto">
    <RouterLink v-for="user in users" :key="user.id" :to="`/user/${user.username}`"
      class="flex items-center space-x-2 hover:underline cursor-pointer">
      <img :src="user.image" alt="User Image" class="w-10 h-10 rounded-full object-cover" />
      <span class="text-gray-700 font-medium">{{ user.username }}</span>
    </RouterLink>
  </div>
</template>