<script setup>
import { onMounted, ref, watch, onActivated, onDeactivated, computed } from 'vue';
import { useRoute, RouterLink, useRouter } from 'vue-router';
import axios from 'axios'
import RelatedPins from '@/components/Auth/RelatedPins.vue';
import PinLikesPopover from '@/components/Auth/PinLikesPopover.vue';
import CommentSection from '@/components/Auth/CommentSection.vue';

const route = useRoute();
const pinId = route.params.id

const videoPlayer = ref(null);
const isPlaying = ref(true);
const volume = ref(0.2);
const oldVolume = ref(null)
const currentTime = ref(0);
const duration = ref(0);

const showLikeAnimation = ref(null)
const showDislikeAnimation = ref(null)

const onVideoLoad = () => {
  pinVideoLoaded.value = true;
  if (videoPlayer.value) {
    videoPlayer.value.volume = volume.value;
    duration.value = videoPlayer.value.duration;
  }
};

const togglePlayPause = () => {
  if (!videoPlayer.value) return;
  if (isPlaying.value) {
    videoPlayer.value.pause();
  } else {
    videoPlayer.value.play();
  }
  isPlaying.value = !isPlaying.value;
};


const changeVolume = () => {
  if (videoPlayer.value) {
    videoPlayer.value.volume = volume.value;
  }
};

const muteUnmute = () => {
  if (videoPlayer.value.volume == 0) {
    volume.value = oldVolume.value
    videoPlayer.value.volume = volume.value
  } else {
    videoPlayer.value.volume = 0;
    oldVolume.value = volume.value;
    volume.value = 0;
  }
};

const updateProgress = () => {
  if (videoPlayer.value) {
    currentTime.value = videoPlayer.value.currentTime;
  }
};

const seek = () => {
  if (videoPlayer.value) {
    videoPlayer.value.currentTime = currentTime.value;
  }
};

const formatTime = (time) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
};

const onVideoEnd = () => {
  isPlaying.value = false;
};

onActivated(() => {
  if (pin.value.title) {
    document.title = 'pinterest.xyz / pin ' + pin.value.title
  } else {
    document.title = 'pinterest.xyz / pin ' + pin.value.id
  }
  if (videoPlayer.value) {
    videoPlayer.value.volume = volume.value;
    videoPlayer.value.play();
    isPlaying.value = true;
  }
});

onDeactivated(() => {
  if (videoPlayer.value) {
    videoPlayer.value.pause();
    isPlaying.value = false;
  }
});




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

const cntComments = ref(null)

const showCommets = ref(false)

const router = useRouter();


const showPopover = ref(false); // State to control the popover visibility

const insidePopover = ref(false)

const bgSave = ref('bg-red-700')
const saveText = ref('Save')


const comment = ref('')

const mediaFile = ref(null)
const mediaPreview = ref(null);
const isImage = ref(false);
const isVideo = ref(false);

const bgColors = ref(['bg-red-200', 'bg-orange-200', 'bg-amber-200', 'bg-lime-200', 'bg-green-200', 'bg-emerald-200', 'bg-teal-200', 'bg-sky-200', 'bg-blue-200', 'bg-indigo-200', 'bg-violet-200', 'bg-purple-200', 'bg-fuchsia-200', 'bg-pink-200', 'bg-rose-200'])
const tags = ref([])


onMounted(async () => {
  try {
    const response = await axios.get(`/api/pins/${pinId}`)
    pin.value = response.data
    if (pin.value.title) {
      document.title = 'pinterest.xyz / pin ' + pin.value.title
    } else {
      document.title = 'pinterest.xyz / pin ' + pin.value.id
    }
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
    router.push('/not-found')
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

  try {
    const response = await axios.get(`/api/tags/pin/tags/${pin.value.id}`, { withCredentials: true })
    tags.value = response.data
    for (let i = 0; i < response.data.length; i++) {
      const tag = response.data[i];
      tag.color = randomBgColor()
    }
  } catch (error) {
    console.log(error)
  }

  try {
    const response = await axios.get(`/api/comments/cnt/comments/${pin.value.id}`)
    cntComments.value = response.data
  } catch (error) {
    console.error(error)
  }

})

const goBack = () => {
  router.back();
};

function goForward() {
  router.go(1);
}

const randomBgColor = () => {
  const randomIndex = Math.floor(Math.random() * bgColors.value.length);
  return bgColors.value[randomIndex];
};

async function likePin() {
  if (checkUserLike.value) {
    showDislikeAnimation.value = true
    showLikeAnimation.value = false
    try {
      await axios.delete(`/api/likes/pin/${pin.value.id}`)
      checkUserLike.value = false
      cntLikes.value -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    showLikeAnimation.value = true
    showDislikeAnimation.value = false
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

function handleMediaUpload(event) {
  const file = event.target.files[0];
  if (file) {
    previewFile(file);
  }
}

const previewFile = (file) => {
  mediaFile.value = file;
  const reader = new FileReader();

  reader.onload = (e) => {
    mediaPreview.value = e.target.result;
  };

  reader.readAsDataURL(file);

  if (file.type.startsWith("image/")) {
    isImage.value = true;
    isVideo.value = false;
  } else if (file.type.startsWith("video/")) {
    isImage.value = false;
    isVideo.value = true;
  }
};

async function addComment() {
  if (comment.value.trim() !== '' || mediaFile.value) {
    try {
      const response = await axios.post(`/api/comments/${pin.value.id}`, {
        content: comment.value.trim()
      })
      comment.value = ''
      const commentId = response.data.id
      if (mediaFile.value) {
        try {
          const formData = new FormData();
          formData.append('file', mediaFile.value);

          const response = await axios.post(`/api/comments/upload/${commentId}`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

        } catch (error) {
          console.log(error)
        }
      }
    } catch (error) {
      console.error(error)
    }
    cntComments.value += 1
  }
}

const showControls = ref(false)

function showTagsPin(tag) {
  router.push(`/?tag=${tag.name}`);
}

function resetFile() {
  mediaPreview.value = null
  mediaFile.value = null
  isImage.value = false
  isVideo.value = false
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
        <div class="relative w-full max-w-2xl mx-auto">
          <img v-if="pinImage" :src="pinImage" alt="Pin Image" class="h-auto w-full rounded-l-3xl"
            @load="pinImageLoaded = true" />
          <div v-if="pinImageLoaded" class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div class="relative flex items-center justify-center w-12 h-12">
              <transition name="flash2">
                <i v-if="showDislikeAnimation"
                  class="absolute pi pi-heart text-8xl text-white glowing-icon opacity-0"></i>
              </transition>
              <transition name="flash2">
                <i v-if="showLikeAnimation"
                  class="absolute pi pi-heart-fill text-8xl text-white glowing-icon opacity-0"></i>
              </transition>
            </div>
          </div>
        </div>
        <div class="relative w-full max-w-2xl mx-auto" @mouseover="showControls = true"
          @mouseleave="showControls = false">
          <!-- Video Element -->
          <video @click="togglePlayPause" v-if="pinVideo" :src="pinVideo" ref="videoPlayer"
            class="w-full rounded-l-3xl block" autoplay loop @loadeddata="onVideoLoad" @timeupdate="updateProgress"
            @ended="onVideoEnd"></video>

          <!-- Gradient Overlay (cloud-like fade effect) -->
          <div v-if="pinVideoLoaded && showControls"
            class="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-red-900 to-transparent rounded-l-3xl">
          </div>

          <!-- Custom Controls -->
          <div v-if="pinVideoLoaded && showControls"
            class="absolute bottom-10 left-4 right-4 flex items-center justify-between text-white">
            <!-- Left Controls (Play/Pause and Time Info) -->
            <div class="flex items-center gap-3">
              <i v-if="isPlaying" @click="togglePlayPause" class="pi pi-pause cursor-pointer text-xl"></i>
              <i v-if="!isPlaying" @click="togglePlayPause" class="pi pi-play cursor-pointer text-xl"></i>
              <span class="text-md">
                {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
              </span>
            </div>

            <!-- Right Controls (Mute/Unmute and Volume Slider) -->
            <div class="flex items-center gap-3 text-white">
              <i v-if="volume == 0" @click="muteUnmute" class="pi pi-volume-off  text-xl"></i>
              <i v-if="volume != 0" @click="muteUnmute" class="pi pi-volume-up  text-xl"></i>
              <input type="range" class="w-20 h-0.5 bg-black rounded-lg cursor-pointer accent-white " min="0" max="1"
                step="0.0005" v-model="volume" @input="changeVolume" />
            </div>
          </div>

          <!-- Progress Bar -->
          <div v-if="showControls && pinVideoLoaded" class="absolute bottom-4 left-4 right-4">
            <input type="range" class="w-full h-0.5 bg-black rounded-lg cursor-pointer accent-white" :max="duration"
              min="0" step="0.01" v-model="currentTime" @input="seek" />
          </div>

          <!-- Center Play/Pause Button with Gradient Overlay -->
          <div v-if="showControls && pinVideoLoaded"
            class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div class="relative flex items-center justify-center w-12 h-12">
              <transition name="flash">
                <i v-if="isPlaying" @click="togglePlayPause"
                  class="absolute pi pi-pause text-5xl text-white glowing-icon"></i>
              </transition>
              <transition name="flash">
                <i v-if="!isPlaying" @click="togglePlayPause"
                  class="absolute pi pi-play text-5xl text-white glowing-icon"></i>
              </transition>
            </div>
          </div>

          <div v-if="pinVideoLoaded" @click="togglePlayPause"
            class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div class="relative flex items-center justify-center w-12 h-12">
              <transition name="flash2">
                <i v-if="showDislikeAnimation"
                  class="absolute pi pi-heart text-8xl text-white glowing-icon opacity-0"></i>
              </transition>
              <transition name="flash2">
                <i v-if="showLikeAnimation"
                  class="absolute pi pi-heart-fill text-8xl text-white glowing-icon opacity-0"></i>
              </transition>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: User Information -->
      <div class="flex flex-col">
        <div class="flex items-center justify-between w-full p-2">
          <!-- Icon and Likes -->
          <div class="flex items-center space-x-4">
            <!-- Icon -->
            <i v-if="checkUserLike" @click="likePin"
              class="text-rose-500 pi pi-heart-fill text-2xl cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>
            <i v-if="!checkUserLike" @click="likePin"
              class="text-rose-500 pi pi-heart text-2xl cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>
            <!-- Number of Likes -->
            <div v-if="cntLikes != 0" class="font-bold text-2xl relative cursor-pointer" @mouseover="showPopover = true"
              @mouseleave="if (!insidePopover) showPopover = false;">
              <div>
                <span>{{ cntLikes }}</span>
              </div>
              <div v-if="showPopover" @mouseover="insidePopover = true"
                @mouseleave="insidePopover = false; showPopover = false" class="absolute top-[30px] left-[-50px] z-50">
                <PinLikesPopover :pin_id="pin.id" />
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <button @click="save"
            :class="`px-6 py-3 text-sm ${bgSave} hover:bg-red-700 text-white rounded-3xl transition`">
            {{ saveText }}
          </button>
        </div>
        <div v-if="pin.title">
          <span class="font-bold text-2xl">{{ pin.title }}</span>
        </div>
        <div class="mt-2" v-if="pin.description">
          {{ pin.description }}
        </div>
        <div class="mt-4" v-if="pin.href">
          <a target="_blank" :href="pin.href" class="underline hover:text-rose-600 text-orange-400">{{ pin.href }}</a>
        </div>
        <div class="flex flex-wrap gap-2 my-2" v-auto-animate>
          <div v-for="tag in tags" :key="tag.id" @click="showTagsPin(tag)"
            :class="[`${tag.color}`, 'text-sm', 'font-medium', 'rounded-3xl', 'px-3', 'py-2', 'cursor-pointer', 'transition-transform', 'duration-200', 'transform', 'hover:scale-110']">
            {{ tag.name }}
          </div>
        </div>
        <RouterLink v-if="pinUser" :to="`/user/${pinUser.username}`"
          class="flex items-center mt-2 hover:underline cursor-pointer">
          <img v-if="pinUserImage" :src="pinUserImage" alt="User Profile" class="w-8 h-8 rounded-full" />
          <span class="ml-2 text-sm font-medium">@{{ pinUser.username }}</span>
        </RouterLink>
        <div class="mt-5" v-if="cntComments != 0" @click="showCommets = !showCommets">
          <h1> {{ cntComments }} Comments</h1>
        </div>
        <CommentSection v-if="showCommets" :pin_id="pin.id" class="mb-5"/>
        <div v-if="isImage" class="relative">
          <div class="absolute top-0 left-[-10px]" @click="resetFile">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <img :src="mediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" alt="Media Preview" />
        </div>
        <div v-if="isVideo" class="relative">
          <div class="absolute top-0 left-[-10px] z-20" @click="resetFile">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <video :src="mediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" autoplay loop
            muted />
        </div>
        <div class="flex items-center space-x-2 mb-4 mr-6 mt-2">
          <!-- Add Button -->
          <button type="button" @click="addComment"
            class="bg-red-500 hover:bg-red-600 transition duration-300 text-white font-medium rounded-xl text-sm px-4 py-2">
            Add
          </button>

          <!-- Tags Input -->
          <input v-model="comment" type="text" name="comment" id="comment" autocomplete="off"
            class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl flex-grow py-3 px-5 focus:ring-red-500 focus:border-red-500"
            placeholder="Введите комментарий" />

          <label for="media">
            <i class="pi pi-images text-4xl cursor-pointer text-red-500 hover:text-red-700 transition duration-300"></i>
          </label>
          <input type="file" id="media" name="media" accept="image/*,video/*" @change="handleMediaUpload"
            class="hidden hover:bg-red-100 transition duration-300 w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
        </div>
      </div>
    </div>
  </div>
  <RelatedPins v-if="pinImageLoaded || pinVideoLoaded" :pin_id="pin.id" />
</template>


<style scoped>
/* Анимация вспышки */
.flash-enter-active,
.flash-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.flash-enter-from,
.flash-leave-to {
  opacity: 0;
  transform: scale(3);
}

.flash-enter-to,
.flash-leave-from {
  opacity: 1;
  transform: scale(1);
}




.glowing-icon {
  text-shadow: 0 0 15px rgba(255, 0, 0, 0.7), 0 0 25px rgba(255, 0, 0, 0.6), 0 0 35px rgba(255, 0, 0, 0.5);
}




.flash2-enter-active,
.flash2-leave-active {
  transition: opacity 0.5s ease-out, transform 0.5s cubic-bezier(0.3, 0.8, 0.2, 1);
}

.flash2-enter-from,
.flash2-leave-to {
  opacity: 0;
  transform: scale(3);
}

.flash2-enter-to,
.flash2-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>