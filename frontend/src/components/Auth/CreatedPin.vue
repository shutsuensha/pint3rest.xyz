<script setup>
import { onMounted, ref, computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';


const popUser = ref(null)
const popImage = ref(null)

const emit = defineEmits(['pinLoaded'])

const user = ref(null);
const pinImage = ref(null);
const pinVideo = ref(null)
const imageLoaded = ref(false); // Флаг загрузки изображения
const videoLoaded = ref(false); // Флаг загрузки видео

const userImage = ref(null);

const showPopover = ref(false); // State to control the popover visibility

const insidePopover = ref(false)

const bgSave = ref('bg-red-600')
const saveText = ref('Save')

const props = defineProps({
  pin: Object,
  showAllPins: Boolean
});

const videoDuration = ref(0)
const currentTime = ref(0)

const videoPlayer = ref(null);


const onTimeUpdate = () => {
  if (videoPlayer.value) {
    currentTime.value = videoPlayer.value.currentTime; // Получаем текущее время
  }
};

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${String(minutes).padStart(1, '0')}:${String(secs).padStart(2, '0')}`;
};

const formattedTimeRemaining = computed(() => {
  const timeRemaining = Math.max(videoDuration.value - currentTime.value, 0);
  return formatTime(timeRemaining);
});

const onImageLoad = () => {
  imageLoaded.value = true;
  emit('pinLoaded')
};

const imageGif = ref(false)

const onVideoLoad = () => {
  if (videoPlayer.value) {
    videoDuration.value = videoPlayer.value.duration; // Получаем длительность
  }
  videoLoaded.value = true;
  emit('pinLoaded')
}

const showSaveButton = ref(false)

onMounted(async () => {
  try {
    try {
      const pinResponse = await axios.get(`/api/pins/upload/${props.pin.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(pinResponse.data);
      const contentType = pinResponse.headers['content-type'];
      if (contentType === 'image/gif') {
        imageGif.value = true
      }
      if (contentType.startsWith('image/')) {
        pinImage.value = blobUrl;
      } else {
        pinVideo.value = blobUrl;
      }
    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    console.error(error);
  }
});

async function loadUser() {
  try {
    const response = await axios.get(`/api/users/user_id/${props.pin.user_id}`)
    popUser.value = response.data
    try {
      const response = await axios.get(`/api/users/upload/${props.pin.user_id}`, { responseType: 'blob' })
      const blobUrl = URL.createObjectURL(response.data);
      popImage.value = blobUrl
    } catch (error) {
      console.error(error)
    }
  } catch (error) {
    console.error(error)
  }
}

async function save() {
  bgSave.value = 'bg-black'
  saveText.value = 'Saving...'
  try {
    const response = await axios.post(`/api/pins/user_saved_pins/${props.pin.id}`, {
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
  <div class="w-1/5 p-2">
    <div class="relative block transition-transform duration-100 transform hover:scale-105" @mouseover="showSaveButton = true; "
      @mouseleave="showSaveButton = false; ">
      <button v-if="showSaveButton" @click.stop="save"
        :class="`absolute z-50 top-2 right-2 px-6 py-3 text-sm ${bgSave} hover:bg-red-800 text-white rounded-3xl transition`">
        {{ saveText }}
      </button>
      <RouterLink :to="`/pin/${pin.id}`">
        <div v-show="!showAllPins" :class="['w-full', 'rounded-3xl']"
          :style="{ backgroundColor: pin.rgb, height: pin.height + 'px' }">
        </div>
        <div class="relative">
          <div v-if="imageGif" class="absolute top-2 left-2 bg-gray-200 text-black rounded-2xl px-3 py-1 text-sm">Gif
          </div>
          <img v-show="showAllPins && pinImage" :src="pinImage" @load="onImageLoad" alt="pin image"
            class="w-full h-auto rounded-3xl" />
        </div>
        <div class="relative">
          <div v-if="videoDuration" class="absolute top-2 left-2 bg-gray-200 text-black rounded-2xl px-3 py-1 text-sm">
            {{ formattedTimeRemaining }}
          </div>
          <video v-show="showAllPins && pinVideo" :src="pinVideo" @loadeddata="onVideoLoad" ref="videoPlayer"
            @timeupdate="onTimeUpdate" class="w-full h-auto rounded-3xl" autoplay loop muted />
        </div>
      </RouterLink>
    </div>

    <p v-if="pin.title" class="mt-2 text-sm"> {{ pin.title }}</p>
  </div>
</template>