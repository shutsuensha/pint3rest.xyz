<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'

const props = defineProps({
  user_id: Number,
  cntUserFollowers: Number
})

const users = ref([])

const offset = ref(0);
const limit = ref(7)

const isPinsLoading = ref(false);

async function loadUsers() {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/subscription/followers/${props.user_id}`, { params: { offset: offset.value, limit: limit.value } })
    const data = response.data

    for (let i = 0; i < data.length; i++) {
      let userImage = null
      try {
        const userResponse = await axios.get(`/api/users/upload/${data[i].id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(userResponse.data);
        userImage = blobUrl;
      } catch (error) {
        console.error(error);
      }
      users.value.push({ id: data[i].id, username: data[i].username, image: userImage })
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
  <div class="flex justify-center items-center min-h-screen">
    <div
      class="flex flex-col gap-2 bg-black shadow-2xl h-auto max-h-[600px] text-2xl rounded-3xl text-white z-50 w-[600px] overflow-y-auto py-2"
      style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
      
      <h1 class="text-7xl text-center my-2">{{cntUserFollowers}} Followers</h1>
      <div @scroll="handleScroll" class="overflow-y-auto">
        <RouterLink v-for="user in users" :key="user.id" :to="`/user/${user.username}`"
          class="my-2 ml-6 flex items-center space-x-5 hover:underline cursor-pointer">
          <img :src="user.image" alt="User Image" class="w-20 h-20 rounded-full object-cover" />
          <span class="truncate">{{ user.username }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>