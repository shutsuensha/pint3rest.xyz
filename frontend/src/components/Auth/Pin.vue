<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';

const user = ref(null);

const pinFile = ref(null)
const pinIsVideo = ref(false)
const pinIsImage = ref(false)

const userImage = ref(null)

const imagesLoading = ref(true)

const props = defineProps({
  pin: Object,
});

onMounted(async () => {
  try {
    const response = await axios.get(`/api/users/user_id/${props.pin.user_id}`);
    user.value = response.data;

    console.log(user.value)

    try {
      const response = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' })
      const blobUrl = URL.createObjectURL(response.data);
      userImage.value = blobUrl
    } catch (error) {
      console.error(error)
    }

    try {
      const response = await axios.get(`/api/pins/upload/${props.pin.id}`, { responseType: 'blob' })
      const blobUrl = URL.createObjectURL(response.data);
      pinFile.value = blobUrl
      const contentType = response.headers['content-type'];
      if (contentType.startsWith('image/')) {
        pinIsImage.value = true
      } else {
        pinIsVideo.value = true
      }
    } catch (error) {
      console.error(error)
    }

    imagesLoading.value = false
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <div class="col-span-1">
    <RouterLink :to="`/pin/${pin.id}`" class="block">
      <!-- Set background color dynamically using pin.rgb -->
      <div v-if="imagesLoading" class="w-full h-96 rounded-3xl" :style="{ backgroundColor: pin.rgb }"></div>
      <div v-else>
        <img v-if="pinIsImage":src="pinFile" alt="pin image" class="w-full h-96 rounded-3xl object-cover"/>
        <video v-if="pinIsVideo" :src="pinFile" class="w-full h-96 rounded-3xl object-cover" autoplay loop muted />
      </div>
      <p v-if="pin.title" class="mt-2 text-sm font-semibold"> {{ pin.title }} Image</p>
    </RouterLink>
    <RouterLink v-if="user" :to="`/user/${user.username}`"
      class="flex items-center mt-2 hover:underline cursor-pointer">
      <div v-if="imagesLoading" class="bg-gray-300 w-8 h-8 rounded-full"></div>
      <img v-else :src="userImage" alt="user profile" class="w-8 h-8 rounded-full object-cover"/>
      <span class="ml-2 text-sm font-medium"> {{ user.username }}</span>
    </RouterLink>
    <div v-else class="flex items-center mt-2 hover:underline cursor-pointer">
      <div class="bg-gray-300 w-8 h-8 rounded-full"></div>
      <span class="ml-2 text-sm font-medium"></span>
    </div>
  </div>
</template>
