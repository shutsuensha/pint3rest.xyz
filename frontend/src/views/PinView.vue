<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';
import axios from 'axios'
import RelatedPins from '@/components/Auth/RelatedPins.vue';
import PinLikesPopover from '@/components/Auth/PinLikesPopover.vue';

const route = useRoute();
const pinId = route.params.id



const pin = ref({
  id: null,
  user_id: null,
  title: '',
  description: '',
  href: '',
  image: '',
  rgb: '',
  height: '',
});


const pinImage = ref(null)
const pinImageLoaded = ref(false)
const pinVideoLoaded = ref(false)
const pinVideo = ref(null)
const pinUser = ref(null)
const pinUserImage = ref(null)

const cntLikes = ref(null)
const checkUserLike = ref(null)

const router = useRouter();


const showPopover = ref(false); // State to control the popover visibility

const insidePopover = ref(false)

const bgSave = ref('bg-red-700')
const saveText = ref('Save')


onMounted(async () => {
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

  try {
    const response = await axios.get(`/api/likes/pin/likes/cnt/${pin.value.id}`)
    cntLikes.value = response.data
  } catch (error) {
    console.error(error)
  }

  try {
    const response = await axios.get(`/api/likes/pin/user_like/${pin.value.id}`)
    checkUserLike.value = response.data
  } catch (error) {
    console.error(error)
  }
})

const goBack = () => {
  router.back();
};

async function likePin() {
  if (checkUserLike.value) {
    try {
      await axios.delete(`/api/likes/pin/${pin.value.id}`)
      checkUserLike.value = false
      cntLikes.value -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    try {
      await axios.post(`/api/likes/pin/${pin.value.id}`)
      checkUserLike.value = true
      cntLikes.value += 1
    } catch (error) {
      console.log(error)
    }
  }
}

async function save() {
  bgSave.value = 'bg-black'
  saveText.value = 'Saving...'
  try {
    const response = await axios.post(`/api/pins/user_saved_pins/${pin.value.id}`, {
      withCredentials: true
    })
    saveText.value = 'Saved'

  } catch (error) {
    if (error.response.status === 409) {
      saveText.value = 'U already saved!'
    }
  }
}
</script>


<template>
  <div class="mt-4 ml-20">
    <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <div v-show="pinImageLoaded || pinVideoLoaded"
      class="grid grid-cols-2 gap-6 mx-60 bg-gray-100 rounded-3xl shadow-lg">
      <!-- Left Column: Image or Video -->
      <div>
        <img v-if="pinImage" :src="pinImage" alt="Pin Image" class="h-auto w-auto rounded-l-3xl"
          @load="pinImageLoaded = true" />
        <video v-if="pinVideo" :src="pinVideo" alt="Pin Video" class="w-auto h-auto rounded-l-3xl" autoplay loop muted
          @loadeddata="pinVideoLoaded = true" />
      </div>

      <!-- Right Column: User Information -->
      <div class="flex flex-col">
        <div class="flex items-center justify-between w-full p-2">
          <!-- Icon and Likes -->
          <div class="flex items-center space-x-2">
            <!-- Icon -->
            <i @click="likePin" :class="`pi ${checkUserLike ? 'pi-heart-fill' : 'pi-heart'} text-2xl`"></i>
            <!-- Number of Likes -->
            <div v-if="cntLikes != 0" class="font-medium text-2xl relative" @mouseover="showPopover = true"
              @mouseleave="if (!insidePopover) showPopover = false;">
              <span>{{ cntLikes }}</span>
              <div v-if="showPopover" @mouseover="insidePopover = true"
                @mouseleave="insidePopover = false; showPopover = false"
                class="absolute top-[30px] left-[-50px]">
                <PinLikesPopover :pin_id="pin.id"/>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <button @click="save" :class="`px-6 py-3 text-sm ${bgSave} hover:bg-red-700 text-white rounded-3xl transition`">
            {{ saveText }}
          </button>
        </div>
        <div v-if="pin.title">
          {{ pin.title }}
        </div>
        <div v-if="pin.description">
          {{ pin.description }}
        </div>
        <div v-if="pin.href">
          {{ pin.href }}
        </div>
        <RouterLink v-if="pinUser" :to="`/user/${pinUser.username}`"
          class="flex items-center mt-2 hover:underline cursor-pointer">
          <img v-if="pinUserImage" :src="pinUserImage" alt="User Profile" class="w-8 h-8 rounded-full" />
          <span class="ml-2 text-sm font-medium">@{{ pinUser.username }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
  <RelatedPins v-if="pinImageLoaded || pinVideoLoaded" :pin_id="pin.id" />
</template>
