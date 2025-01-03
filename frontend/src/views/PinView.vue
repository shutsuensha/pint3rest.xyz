<script setup>
import { onMounted, ref, watch  } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';
import axios from 'axios'
import RelatedPins from '@/components/Auth/RelatedPins.vue';


const route = useRoute();
const pinId = route.params.id



const pin = ref(null)
const pinImage = ref(null)
const pinImageLoaded = ref(false)
const pinVideoLoaded = ref(false)
const pinVideo = ref(null)
const pinUser = ref(null)
const pinUserImage = ref(null)

const router = useRouter(); 


onMounted(async () => {
  console.log('pin view')
  try {
    const response = await axios.get(`/api/pins/${pinId}`)
    pin.value = response.data
    try {
      const response = await axios.get(`/api/pins/upload/${pinId}`, { responseType: 'blob' })
      const blobUrl = URL.createObjectURL(response.data);
      const contentType = response.headers['content-type'];
      if (contentType.startsWith('image/')) {
        pinImage.value = blobUrl;
      } else {
        pinVideo.value = blobUrl;
      }
    } catch (error) {
      console.error(error)
    }
    try {
      const response = await axios.get(`/api/users/user_id/${pin.value.user_id}`)
      pinUser.value = response.data
      try {
        const response = await axios.get(`/api/users/upload/${pinUser.value.id}`, { responseType: 'blob' })
        const blobUrl = URL.createObjectURL(response.data);
        pinUserImage.value = blobUrl
      } catch (error) {
        console.log(error)
      }
    } catch (error) {
      console.log(error)
    }
  } catch (error) {
    console.error(error)
  }
})

const goBack = () => {
  router.back();
};
</script>


<template>
  <div class="mt-20 ml-20">
    <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <div v-show="pinImageLoaded || pinVideoLoaded" class="grid grid-cols-2 gap-6 mx-60 bg-gray-100 rounded-3xl shadow-lg">
      <!-- Left Column: Image or Video -->
      <div>
        <img 
          v-if="pinImage" 
          :src="pinImage" 
          alt="Pin Image" 
          class="h-full w-full rounded-l-3xl"
          @load="pinImageLoaded = true"
        />
        <video 
          v-if="pinVideo" 
          :src="pinVideo" 
          alt="Pin Video" 
          class="w-full h-auto rounded-l-3xl" 
          autoplay 
          loop 
          muted
          @loadeddata="pinVideoLoaded = true"
        />
      </div>

      <!-- Right Column: User Information -->
      <div class="flex flex-col">
        <RouterLink 
          v-if="pinUser" 
          :to="`/user/${pinUser.username}`" 
          class="flex items-center mt-2 hover:underline cursor-pointer"
        >
          <img 
            v-if="pinUserImage" 
            :src="pinUserImage" 
            alt="User Profile" 
            class="w-8 h-8 rounded-full" 
          />
          <span class="ml-2 text-sm font-medium">@{{ pinUser.username }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
  <RelatedPins v-if="pinImageLoaded || pinVideoLoaded" :pin_id="pin.id"/>
</template>
