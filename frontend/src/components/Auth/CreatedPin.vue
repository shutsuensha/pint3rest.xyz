<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';


const popUser = ref(null)
const popImage = ref(null)

const emit = defineEmits(['lastPinLoaded'])

const user = ref(null);
const pinImage = ref(null);
const pinVideo = ref(null)
const imageLoaded = ref(false); // Флаг загрузки изображения
const videoLoaded = ref(false); // Флаг загрузки видео

const userImage = ref(null);

const showPopover = ref(false); // State to control the popover visibility

const insidePopover = ref(false)

const bgSave = ref('bg-red-700')
const saveText = ref('Save')

const props = defineProps({
  pin: Object,
  lastPinId: Number,
  showAllPins: Boolean
});

const onImageLoad = () => {
  imageLoaded.value = true;
};

const onVideoLoad = () => {
  videoLoaded.value = true;
}

const showSaveButton = ref(false)

onMounted(async () => {
  try {
    try {
      const pinResponse = await axios.get(`/api/pins/upload/${props.pin.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(pinResponse.data);
      const contentType = pinResponse.headers['content-type'];
      if (contentType.startsWith('image/')) {
        pinImage.value = blobUrl;
      } else {
        pinVideo.value = blobUrl;
      }
      if (props.pin.id === props.lastPinId) {
        emit('lastPinLoaded');
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
    <div class="relative block hover:opacity-90" @mouseover="showSaveButton = true"
      @mouseleave="showSaveButton = false">
      <button v-if="showSaveButton" @click.stop="save"
        :class="`absolute z-50 top-2 right-2 px-6 py-3 text-sm ${bgSave} text-white rounded-3xl transition`">
        {{ saveText }}
      </button>
      <RouterLink :to="`/pin/${pin.id}`">
        <div v-show="!showAllPins" :class="['w-full', 'rounded-3xl']"
          :style="{ backgroundColor: pin.rgb, height: pin.height + 'px' }">
        </div>
        <div v-show="showAllPins">
          <img v-if="pinImage" :src="pinImage" @load="onImageLoad" alt="pin image" class="w-full h-auto rounded-3xl" />
          <video v-if="pinVideo" :src="pinVideo" @loadeddata="onVideoLoad" class="w-full h-auto rounded-3xl" autoplay
            loop muted />
        </div>
        <p v-if="pin.title" class="mt-2 text-sm"> {{ pin.title }}</p>
      </RouterLink>
    </div>
  </div>
</template>