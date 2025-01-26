<script setup>
import { onMounted, ref, computed, onActivated, onDeactivated, nextTick } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';
import FollowersSection from '@/components/Auth/FollowersSection.vue';
import FollowingSection from '@/components/Auth/FollowingSection.vue';


const popUser = ref(null)
const popImage = ref(null)

const cntUserFollowers = ref(null)
const cntUserFollowing = ref(null)
const checkUserFollow = ref(null)

const showFollowers = ref(false)
const showFollowing = ref(false)


const itsMe = ref(null)


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


const videoDuration = ref(0)
const currentTime = ref(0)

const videoPlayer = ref(null);


onActivated(() => {
  if (videoPlayer.value) {
    var playPromise = videoPlayer.value.play()
    if (playPromise !== undefined) {
      playPromise.then(_ => {
        // Automatic playback started!
        // Show playing UI.
      })
        .catch(error => {
          // Auto-play was prevented
          // Show paused UI.
        });
    }
  }
});

onDeactivated(() => {
  if (videoPlayer.value) {
    // Можно остановить видео или выполнить другие действия
    videoPlayer.value.pause();
  }
});


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



function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}


const props = defineProps({
  pin: Object,
  showAllPins: Boolean
});

const onImageLoad = () => {
  imageLoaded.value = true;
  emit('pinLoaded')
};

const onVideoLoad = () => {
  if (videoPlayer.value) {
    videoDuration.value = videoPlayer.value.duration; // Получаем длительность
  }
  emit('pinLoaded')
  videoLoaded.value = true;
}

const showSaveButton = ref(false)

const imageGif = ref(false)

onMounted(async () => {
  try {
    const response = await axios.get(`/api/users/user_id/${props.pin.user_id}`);
    user.value = response.data;

    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;
    } catch (error) {
      console.error(error);
    }

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
  if (popUser.value) return
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
  try {
    const response = await axios.get(`/api/subscription/followers/cnt/${popUser.value.id}`, { withCredentials: true })
    cntUserFollowers.value = response.data
  } catch (error) {
    console.error(error)
  }

  try {
    const response = await axios.get(`/api/subscription/following/cnt/${popUser.value.id}`, { withCredentials: true })
    cntUserFollowing.value = response.data
  } catch (error) {
    console.error(error)
  }

  try {
    const response = await axios.get(`/api/subscription/check_user_follow/${popUser.value.id}`, { withCredentials: true })
    checkUserFollow.value = response.data
  } catch (error) {
    console.error(error)
  }

  const accessToken = getCookie('access_token');
  // Decode the JWT (assuming the access_token is a JWT)
  const base64Url = accessToken.split('.')[1]; // Get the payload part
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );

  const payload = JSON.parse(jsonPayload);

  // Log user_id to the console
  let auth_user_id = payload.user_id;

  itsMe.value = auth_user_id === popUser.value.id
}

async function follow() {
  try {
    const response = await axios.post(`/api/subscription/${popUser.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = true
  cntUserFollowers.value += 1
}

async function unfollow() {
  try {
    const response = await axios.delete(`/api/subscription/${popUser.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = false
  cntUserFollowers.value -= 1
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
  <div class="w-1/5 p-2 ">
    <transition name="fade" appear>
      <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
        <FollowersSection :user_id="user.id" :cntUserFollowers="cntUserFollowers" />
        <i @click="showFollowers = false"
          class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
      </div>
    </transition>

    <transition name="fade" appear>
      <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
        <FollowingSection :user_id="user.id" :cntUserFollowing="cntUserFollowing" />
        <i @click="showFollowing = false"
          class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
      </div>
    </transition>

    <div class="relative block transition-transform duration-100 transform hover:scale-105"
      @mouseover="showSaveButton = true;" @mouseleave="showSaveButton = false;">
      <button v-if="showSaveButton" @click.stop="save"
        :class="`absolute z-10 top-2 right-2 px-6 py-3 text-sm ${bgSave} hover:bg-red-800 text-white rounded-3xl transition`">
        {{ saveText }}
      </button>
      <RouterLink :to="`/pin/${pin.id}`">
        <div v-show="!showAllPins" :class="['w-full', 'rounded-3xl']"
          :style="{ backgroundColor: pin.rgb, height: pin.height + 'px' }">
        </div>
        <div class="relative">
          <div v-if="imageGif && showAllPins" class="absolute top-2 left-2 bg-gray-200 text-black rounded-2xl px-3 py-1 text-sm">Gif
          </div>
          <img v-show="showAllPins && pinImage" :src="pinImage" @load="onImageLoad" alt="pin image"
            class="w-full h-auto rounded-3xl" />
        </div>
        <div class="relative">
          <div v-if="showAllPins && videoDuration"
            class="absolute top-2 left-2 bg-gray-200 text-black rounded-2xl px-3 py-1 text-sm">
            {{ formattedTimeRemaining }}
          </div>
          <video v-show="showAllPins && pinVideo" :src="pinVideo" @loadeddata="onVideoLoad" ref="videoPlayer"
            @timeupdate="onTimeUpdate" class="w-full h-auto rounded-3xl" autoplay loop muted />
        </div>
      </RouterLink>
    </div>

    <p v-if="pin.title" class="mt-2 text-sm"> {{ pin.title }}</p>

    <div class="relative">
      <div v-if="user" :to="`/user/${user.username}`"
        class="flex items-center mt-2 hover:underline relative ">
        <div v-if="!showAllPins" class="bg-gray-300 w-8 h-8 rounded-full"></div>
        <img v-else :src="userImage" alt="user profile" class="w-8 h-8 rounded-full object-cover" />
        <span @click="if(showPopover) {showPopover = false} else { showPopover = true; loadUser()}" v-if="user && showAllPins" class="ml-2 text-sm font-medium cursor-pointer"> {{ user.username }}</span>
        <transition name="flash">
          <div v-if="showPopover"
            class="absolute top-[30px] left-0 bg-white   bg-opacity-20 backdrop-blur-md rounded-3xl font-medium text-white z-20 h-[200px] w-[271px]">
            <div class="relative flex flex-col top-7 items-center justify-center">
               <RouterLink :to="`/user/${popUser.username}`"
                class="relative transition-transform duration-200transform hover:scale-110">
                <i v-if="popUser && popUser.verified" class="absolute top-0 left-16 pi pi-verified text-2xl"></i>
                <img v-if="popImage" :src="popImage"
                  class="mb-2 rounded-full w-20 h-20 object-cover border-2 border-red-500" />
              </RouterLink>
              <RouterLink v-if="popUser" :to="`/user/${popUser.username}`" style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                class="text-center text-xl font-bold hover:underline">{{ popUser.username }}</RouterLink>
              <div class="flex space-x-4">
                <span v-if="cntUserFollowers > 0" @click="showFollowers = true" style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                  :class="`text-white cursor-pointer transition-transform duration-200 transform hover:scale-110 `">
                  {{ cntUserFollowers }} followers
                </span>
                <span v-if="cntUserFollowing > 0" @click="showFollowing = true" style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                  :class="`text-white cursor-pointer transition-transform duration-200 transform hover:scale-110  `">
                  {{ cntUserFollowing }} following
                </span>
              </div>
              <div
                class="absolute top-0 right-2 cursor-pointer transition-transform duration-200 transform hover:scale-110">
                <button v-if="!checkUserFollow && !itsMe" @click="follow"
                  class=" px-4 py-2 bg-red-600  text-white  rounded-3xl  text-xs">
                  Follow
                </button>
                <button v-if="checkUserFollow && !itsMe" @click="unfollow"
                  class=" px-4 py-2 bg-red-600  text-white  rounded-3xl  text-xs">
                  Unfollow
                </button>
              </div>
            </div>
          </div>
        </transition>
      </div>
      <div v-else class="flex items-center mt-2 hover:underline cursor-pointer">
        <div class="bg-gray-300 w-8 h-8 rounded-full"></div>
        <span class="ml-2 text-sm font-medium"></span>
      </div>
    </div>
  </div>
</template>


<style scoped>
.flash-enter-active {
  animation: flashEffect 0.5s ease-out;
}


@keyframes flashEffect {
  0% {
    opacity: 0;
    transform: scale(0.1);
  }

  50% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>


<style scoped>
/* Define transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  /* Internet Explorer 10+ */
  scrollbar-width: none;
  /* Firefox */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
}

.fade-in-animation {
  opacity: 0;
  transform: scale(0.95);
  animation: fadeIn 0.3s ease-in-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>