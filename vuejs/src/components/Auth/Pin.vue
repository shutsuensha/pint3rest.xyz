<script setup>
import { onMounted, ref, computed, onActivated, onDeactivated, nextTick } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';
import FollowersSection from '@/components/Auth/FollowersSection.vue';
import FollowingSection from '@/components/Auth/FollowingSection.vue';

import { useSelectedBoard } from "@/stores/userSelectedBoard";

const userSelectedBoardStore = useSelectedBoard();

const popUser = ref(null)
const popImage = ref(null)

const cntUserFollowers = ref(null)
const cntUserFollowing = ref(null)
const checkUserFollow = ref(null)

const showPause = ref(false)

const showFollowers = ref(false)
const showFollowing = ref(false)

const pinUsernameRef = ref(null)
const isTop = ref(null)

onActivated(() => {
  showPause.value = true
})


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
      pinImage.value = "https://i.pinimg.com/736x/6c/a8/05/6ca805efcc51ff2366298781aecde4ae.jpg"
      console.error(error);
    }
  } catch (error) {
    console.error(error);
  }
});

async function loadUser() {
  const element = pinUsernameRef.value;
  if (element) {
    const rect = element.getBoundingClientRect();
    const distanceToBottom = window.innerHeight - rect.bottom;
    if (distanceToBottom < 200) {
      isTop.value = false
    } else {
      isTop.value = true
    }
  }
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
  if (userSelectedBoardStore.selectedBoard == null) {
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
  } else {
    bgSave.value = 'bg-black'
    saveText.value = 'Saving...'
    try {
      const response = await axios.post(`/api/boards/${userSelectedBoardStore.selectedBoard.id}/pins/${props.pin.id}`, {
        withCredentials: true
      })
      saveText.value = 'Saved'

    } catch (error) {
      if (error.response.status === 409) {
        saveText.value = 'U already saved!'
      }
    }
  }
}

const isModalOpen = ref(false);

const boards = ref([])

const loadingBoards = ref(false)

const showBoards = async () => {
  loadingBoards.value = true
  isModalOpen.value = true;
  try {
    const response = await axios.get(`/api/boards/me`, { withCredentials: true });
    boards.value = response.data;
  } catch (error) {
    console.error(error)
  }
  for (let i = 0; i < boards.value.length; i++) {
    try {
      const response = await axios.get(`/api/boards/${boards.value[i].id}`, {
        params: { offset: 0, limit: 5 },
        withCredentials: true,
      });
      boards.value[i].pins = response.data
      for (let j = 0; j < boards.value[i].pins.length; j++) {
        try {
          const pinResponse = await axios.get(`/api/pins/upload/${boards.value[i].pins[j].id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            boards.value[i].pins[j].file = blobUrl;
            boards.value[i].pins[j].isImage = true;
          } else {
            boards.value[i].pins[j].file = blobUrl;
            boards.value[i].pins[j].isImage = false;
          }
        } catch (error) {
          console.error(error);
        }
      }
    } catch (error) {
      console.error(error)
    }
  }
  loadingBoards.value = false
};

const closeModal = () => {
  isModalOpen.value = false;
};

const selectBoard = (board) => {
  userSelectedBoardStore.setBoard(board)
  closeModal();
};

function chooseProfile() {
  userSelectedBoardStore.setBoard(null)
  closeModal();
}

</script>

<template>
  <div class="w-1/5 p-2">
    <transition name="fade" appear>
      <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
        <div class="flex justify-center items-center min-h-screen" @click.self="showFollowers = false">
          <FollowersSection :user_id="user.id" :cntUserFollowers="cntUserFollowers" />
          <i @click="showFollowers = false"
            class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
            style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
        </div>
      </div>
    </transition>



    <transition name="fade" appear>
      <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
        <div class="flex justify-center items-center min-h-screen" @click.self="showFollowing = false">
          <FollowingSection :user_id="user.id" :cntUserFollowing="cntUserFollowing" />
          <i @click="showFollowing = false"
            class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
            style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
        </div>
      </div>
    </transition>
    <div v-if="isModalOpen" class="z-50 fixed inset-0 bg-black/50 flex items-center justify-center px-4"
      @click.self="closeModal">
      <div v-if="loadingBoards"
        class="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-lg max-w-2xl w-full relative backdrop-blur-lg overflow-auto max-h-screen min-h-[300px] flex items-center justify-center">
        <span class="text-center loader2"></span>
      </div>
      <div v-else
        class="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-lg max-w-2xl w-full relative backdrop-blur-lg overflow-auto max-h-screen">

        <!-- Кнопка Profile -->
        <h2 class="text-xl font-semibold mb-4 text-center text-black">Choose where to save</h2>
        <div class="flex justify-center">
          <button @click="chooseProfile"
            class="w-1/2 px-6 py-3 text-md bg-gray-800 hover:bg-black text-white rounded-3xl transition cursor-pointer">
            Profile
          </button>
        </div>

        <!-- Заголовок для бордов -->
        <h2 class="text-xl font-semibold mb-4 mt-4 text-center text-black">Boards</h2>

        <!-- Сетка бордов -->
        <div class="columns-2 gap-4">
          <div v-for="board in boards" :key="board.id"
            class="mb-4 break-inside-avoid relative rounded-md cursor-pointer min-h-24 overflow-hidden transform transition-transform hover:scale-105"
            @click="selectBoard(board)">

            <!-- Центрированный заголовок с тёмным фоном только вокруг текста -->
            <div class="absolute inset-0 flex items-center justify-center z-10 pointer-events-none">
              <h3 class="text-3xl font-semibold text-white text-center px-4 py-2 bg-black/70 rounded-lg shadow-lg">
                {{ board.title }}
              </h3>
            </div>

            <!-- Витрина пинов -->
            <div class="columns-2 gap-1 relative z-0">
              <div v-for="(pin, index) in board.pins" :key="index" class="mb-2 break-inside-avoid">
                <img v-if="pin.isImage" :src="pin.file" :alt="pin.title || 'Pin'"
                  class="w-full object-cover rounded-md">
                <video v-else :src="pin.file" :alt="pin.title || 'Pin'" class="w-full object-cover rounded-md" autoplay
                  loop muted></video>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="relative block transition-transform transform hover:scale-105"
      @mouseover="showSaveButton = true;" @mouseleave="showSaveButton = false;">
      <button v-if="showSaveButton" @click.stop="save"
        :class="`absolute z-10 top-2 right-2 px-6 py-3 text-sm ${bgSave} hover:bg-red-800 text-white rounded-3xl transition`">
        {{ saveText }}
      </button>
      <span v-if="showSaveButton" @click.stop="showBoards"
        :class="`absolute z-10 top-14 right-2 px-6 py-3 text-sm bg-gray-800 hover:bg-black text-white rounded-3xl transition cursor-pointer`">
        {{ userSelectedBoardStore.selectedBoard ? `${userSelectedBoardStore.selectedBoard.title}` : "Profile" }}
      </span>
      <RouterLink :to="`/pin/${pin.id}`">
        <div v-show="!showAllPins" :class="['w-full', 'rounded-3xl']"
          :style="{ backgroundColor: pin.rgb, height: pin.height + 'px' }">
        </div>
        <div class="relative">
          <div v-if="imageGif && showAllPins"
            class="absolute top-2 left-2 bg-gray-100 text-black rounded-2xl px-3 py-1 text-sm">Gif
          </div>
          <img v-show="showAllPins && pinImage" :src="pinImage" @load="onImageLoad" alt="pin image"
            class="w-full h-auto rounded-3xl" />
        </div>
        <div class="relative">
          <div v-if="showAllPins && videoDuration"
            class="absolute top-2 left-2 bg-gray-100 text-black rounded-2xl px-3 py-1 text-sm">
            {{ formattedTimeRemaining }}
          </div>
          <video v-show="showAllPins && pinVideo" :src="pinVideo" @loadeddata="onVideoLoad" ref="videoPlayer"
            @mouseover="videoPlayer.play(); showPause = false" @timeupdate="onTimeUpdate"
            class="w-full h-auto rounded-3xl" autoplay loop muted />
          <div v-if="pinVideo && showPause"
            class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div class="relative flex items-center justify-center w-12 h-12">
              <transition name="flash2">
                <i v-if="!showPause" class="absolute pi pi-pause text-5xl text-white glowing-icon"></i>
              </transition>
              <transition name="flash2">
                <i v-if="showPause" class="absolute pi pi-play text-5xl text-white glowing-icon"></i>
              </transition>
            </div>
          </div>
        </div>
      </RouterLink>
    </div>

    <p v-if="pin.title" class="mt-2 text-sm"> {{ pin.title }}</p>

    <div class="relative">
      <div v-if="user" :to="`/user/${user.username}`" class="flex items-center mt-2 hover:underline relative ">
        <div v-if="!showAllPins" class="bg-gray-300 w-8 h-8 rounded-full"></div>
        <img v-else :src="userImage" alt="user profile" class="w-8 h-8 rounded-full object-cover" />
        <span ref="pinUsernameRef"
          @click="if (showPopover) { showPopover = false } else { showPopover = true; loadUser() }"
          v-if="user && showAllPins" class="ml-2 text-sm font-medium cursor-pointer"> {{ user.username }}</span>
        <transition name="flash">
          <div v-if="showPopover"
            class="absolute left-0 bg-white bg-opacity-20 backdrop-blur-md rounded-3xl font-medium text-white z-20 h-[200px] w-[271px]"
            :style="{ top: isTop ? '30px' : 'auto', bottom: isTop ? 'auto' : '30px' }">
            <div class="relative flex flex-col top-7 items-center justify-center">
              <RouterLink v-if="popUser" :to="`/user/${popUser.username}`"
                class="relative transition-transform duration-200transform hover:scale-110">
                <i v-if="popUser && popUser.verified" class="absolute top-0 left-16 pi pi-verified text-2xl"></i>
                <img v-if="popImage" :src="popImage"
                  class="mb-2 rounded-full w-20 h-20 object-cover border-2 border-red-500" />
              </RouterLink>
              <RouterLink v-if="popUser" :to="`/user/${popUser.username}`"
                style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                class="text-center text-xl font-bold hover:underline">{{ popUser.username }}</RouterLink>
              <div class="flex space-x-4">
                <span v-if="cntUserFollowers > 0" @click="showFollowers = true"
                  style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                  :class="`text-white cursor-pointer transition-transform duration-200 transform hover:scale-110 `">
                  {{ cntUserFollowers }} followers
                </span>
                <span v-if="cntUserFollowing > 0" @click="showFollowing = true"
                  style="text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);"
                  :class="`text-white cursor-pointer transition-transform duration-200 transform hover:scale-110  `">
                  {{ cntUserFollowing }} following
                </span>
              </div>
              <div
                class="absolute top-[-15px] right-2 cursor-pointer transition-transform duration-200 transform hover:scale-110">
                <button v-if="!checkUserFollow && !itsMe" @click="follow"
                  class=" px-3 py-2 bg-red-600  text-white  rounded-3xl  text-xs">
                  Follow
                </button>
                <button v-if="checkUserFollow && !itsMe" @click="unfollow"
                  class=" px-3 py-2 bg-red-600  text-white  rounded-3xl  text-xs">
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

.glowing-icon {
  text-shadow: 0 0 15px rgba(255, 0, 0, 0.7), 0 0 25px rgba(255, 0, 0, 0.6), 0 0 35px rgba(255, 0, 0, 0.5);
}


.loader2 {
  width: 48px;
  height: 48px;
  background: #FFF;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

.loader2::after {
  content: '';
  box-sizing: border-box;
  position: absolute;
  left: 6px;
  top: 10px;
  width: 12px;
  height: 12px;
  color: #FF3D00;
  background: currentColor;
  border-radius: 50%;
  box-shadow: 25px 2px, 10px 22px;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>