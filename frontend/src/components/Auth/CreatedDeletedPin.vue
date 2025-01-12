<script setup>
import { onMounted, ref } from 'vue';
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

const bgSave = ref('bg-red-700')
const saveText = ref('Save')

const bgDelete = ref('bg-black')
const deleteText = ref('Delete')

const props = defineProps({
  pin: Object,
  showAllPins: Boolean
});

const onImageLoad = () => {
  imageLoaded.value = true;
  emit('pinLoaded')
};

const onVideoLoad = () => {
  videoLoaded.value = true;
  emit('pinLoaded')
}

const showSaveButton = ref(false)
const showDeleteButton = ref(false)

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

async function deletePin() {
  bgDelete.value = 'bg-black'
  deleteText.value = 'Deleting...'
  try {
    const response = await axios.delete(`/api/pins/${props.pin.id}`, {
      withCredentials: true
    })
    deleteText.value = 'Deleted'

  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="w-1/5 p-2">
    <div class="relative block hover:opacity-90" @mouseover="showSaveButton = true; showDeleteButton = true"
      @mouseleave="showSaveButton = false; showDeleteButton = false">
      <button v-if="showSaveButton" @click.stop="save"
        :class="`absolute z-50 top-2 right-2 px-6 py-3 text-sm ${bgSave} text-white rounded-3xl transition`">
        {{ saveText }}
      </button>
      <button v-if="showDeleteButton" @click.stop="deletePin"
        :class="`absolute z-50 top-16 right-2 px-6 py-3 text-sm ${bgDelete} text-white rounded-3xl transition`">
        {{ deleteText }}
      </button>
      <RouterLink :to="`/pin/${pin.id}`">
        <div v-show="!showAllPins" :class="['w-full', 'rounded-3xl']"
          :style="{ backgroundColor: pin.rgb, height: pin.height + 'px' }">
        </div>
        <img v-show="showAllPins && pinImage" :src="pinImage" @load="onImageLoad" alt="pin image"
          class="w-full h-auto rounded-3xl" />
        <video v-show="showAllPins && pinVideo" :src="pinVideo" @loadeddata="onVideoLoad"
          class="w-full h-auto rounded-3xl" autoplay loop muted />

        <p v-if="pin.title && showAllPins" class="mt-2 text-sm"> {{ pin.title }}</p>
      </RouterLink>
    </div>
  </div>
</template>