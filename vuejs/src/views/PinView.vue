<script setup>
import { onMounted, ref, watch, onActivated, onDeactivated, computed, nextTick, onBeforeUnmount } from 'vue';
import { useRoute, RouterLink, useRouter, onBeforeRouteUpdate } from 'vue-router';
import axios from 'axios'
import RelatedPins from '@/components/Auth/RelatedPins.vue';
import PinLikesPopover from '@/components/Auth/PinLikesPopover.vue';
import CommentSection from '@/components/Auth/CommentSection.vue';
import PinLikesSection from '@/components/Auth/PinLikesSection.vue';

import EmojiPicker from 'vue3-emoji-picker'

import SearchBar from '@/components/Auth/SearchBar.vue';

import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();

const relatedObserverTarget = ref(null)
const showMoreExplore = ref(true)

const showExplore = ref(false)



import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

import { useSelectedBoard } from "@/stores/userSelectedBoard";

const userSelectedBoardStore = useSelectedBoard();

const route = useRoute();
const router = useRouter();

const pinId = route.params.id


function simulateHover() {
  showViewLarge.value = true;
  setTimeout(() => {
    showViewLarge.value = false;
  }, 2000);
}




const showPicker = ref(false)

const videoPlayer = ref(null);
const isPlaying = ref(true);
const volume = ref(0);
const oldVolume = ref(null)
const currentTime = ref(0);
const duration = ref(0);

const showLikeAnimation = ref(null)
const showDislikeAnimation = ref(null)


const isLoading = ref(null);


const sendComment = ref(false)


// onBeforeRouteUpdate(async (to, from, next) => {
//   if (to.name !== 'home') {
//     // Переход сначала на HomeView
//     await router.push({ name: 'home' });

//     // Ждем рендеринга HomeView
//     await nextTick();

//     // Переход обратно на целевой маршрут
//     router.push(to.fullPath);
//   } else {
//     next();
//   }
// });



const onVideoLoad = () => {
  pinVideoLoaded.value = true;
  if (videoPlayer.value) {
    videoPlayer.value.volume = volume.value;
    duration.value = videoPlayer.value.duration;
    videoPlayer.value.play();
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

const inputAddComment = ref(null)

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
  createObserver()
  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;
  let name = null
  if (pin.value.title) {
    name = pin.value.title
  } else {
    name = 'Pin page'
  }
  if (totalUnread > 0) {
    document.title = `(${totalUnread}) ${name}`; // Если есть непрочитанные уведомления
  } else {
    document.title = name; // Если уведомлений нет
  }

  if (videoPlayer.value) {
    videoPlayer.value.volume = volume.value;
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
    isPlaying.value = true;
    showControls.value = true
    timeoutWorking.value = true
    timeoutId.value = setTimeout(() => {
      showControls.value = false
      timeoutWorking.value = false
    }, 2000);
  }
});

onDeactivated(() => {
  destroyObserver()
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
watch(pinImageLoaded, (newValue) => {
  if (newValue) {
    simulateHover();
  }
});
const pinVideoLoaded = ref(false)
const pinVideo = ref(null)
const pinUser = ref(null)
const pinUserImage = ref(null)

const cntLikes = ref(null)
const checkUserLike = ref(null)

const cntComments = ref(null)

const showCommets = ref(false)


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

const timeoutId = ref(null)
const timeoutWorking = ref(false)

const auth_user_id = ref(null)



let observer

const createObserver = () => {
  observer = new IntersectionObserver(
    ([entry]) => {
      showMoreExplore.value = entry.intersectionRatio < 0.2
    },
    { threshold: [0, 0.2, 1] }
  )

  if (relatedObserverTarget.value) {
    observer.observe(relatedObserverTarget.value)
  }
}

const destroyObserver = () => {
  if (observer && relatedObserverTarget.value) {
    observer.unobserve(relatedObserverTarget.value)
    observer.disconnect()
    observer = null
  }
}

onMounted(async () => {

  createObserver()


  try {
    const response = await axios.get(`/api/pins/${pinId}`);
    pin.value = response.data;


    let unreadMessagesCount = unreadMessagesStore.count;
    let unreadUpdatesCount = unreadUpdatesStore.count;
    let totalUnread = unreadMessagesCount + unreadUpdatesCount;
    let name = null
    if (pin.value.title) {
      name = pin.value.title
    } else {
      name = 'Pin page'
    }
    if (totalUnread > 0) {
      document.title = `(${totalUnread}) ${name}`; // Если есть непрочитанные уведомления
    } else {
      document.title = name; // Если уведомлений нет
    }

    try {
      const response = await axios.get(`/api/pins/upload/${pinId}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(response.data);
      const contentType = response.headers['content-type'];
      if (contentType.startsWith('image/')) {
        pinImage.value = blobUrl;
      } else {
        pinVideo.value = blobUrl;
      }

    } catch (error) {
      console.error(error);
    }

    isLoading.value = true;

    try {
      const response = await axios.get(`/api/users/user_id/${pin.value.user_id}`);
      pinUser.value = response.data;


      try {
        const response = await axios.get(`/api/users/upload/${pinUser.value.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(response.data);
        pinUserImage.value = blobUrl;
      } catch (error) {
        console.log(error);
      }
    } catch (error) {
      console.log(error);
    }
  } catch (error) {
    router.push('/not-found');
  }


  showControls.value = true;
  timeoutWorking.value = true;
  timeoutId.value = setTimeout(() => {
    showControls.value = false;
    timeoutWorking.value = false;
  }, 2000);

  try {
    const response = await axios.get(`/api/likes/pin/likes/cnt/${pin.value.id}`);
    cntLikes.value = response.data;

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/likes/pin/user_like/${pin.value.id}`);
    checkUserLike.value = response.data;

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/tags/pin/tags/${pin.value.id}`, { withCredentials: true });
    tags.value = response.data;
    for (let i = 0; i < response.data.length; i++) {
      const tag = response.data[i];
      tag.color = randomBgColor();
    }

  } catch (error) {
    console.log(error);
  }

  try {
    const response = await axios.get(`/api/comments/cnt/comments/${pin.value.id}`);
    cntComments.value = response.data;

  } catch (error) {
    console.error(error);
  }

  if (cntComments.value) {
    showCommets.value = true;
  }

  // End the loading process
  isLoading.value = false;
});

onBeforeUnmount(() => {
  destroyObserver()
})


const isTop = ref(false)

function loadPicker() {
  if (showPicker.value === false) {
    const element = inputAddComment.value;
    if (element) {
      const rect = element.getBoundingClientRect();
      const distanceToBottom = window.innerHeight - rect.bottom;
      if (distanceToBottom < 320) {
        isTop.value = false
      } else {
        isTop.value = true
      }
    }
  }
}


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
    try {
      await axios.delete(`/api/likes/pin/${pin.value.id}`)
      showDislikeAnimation.value = true
      showLikeAnimation.value = false
      checkUserLike.value = false
      cntLikes.value -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    try {
      await axios.post(`/api/likes/pin/${pin.value.id}`)
      showLikeAnimation.value = true
      showDislikeAnimation.value = false
      checkUserLike.value = true
      cntLikes.value += 1
    } catch (error) {
      console.log(error)
    }
  }
}

async function save() {
  if (userSelectedBoardStore.selectedBoard == null) {
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
  } else {
    bgSave.value = 'bg-black'
    saveText.value = 'Saving...'
    try {
      const response = await axios.post(`/api/boards/${userSelectedBoardStore.selectedBoard.id}/pins/${pin.value.id}`, {
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
        params: { offset: 0, limit: 4 },
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



function handleMediaUpload(event) {
  const file = event.target.files[0];

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm'];
  if (file) {

    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid media file (.jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm).', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
      return;
    }
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

const sendCommentError = ref(false)

async function addComment() {
  if (comment.value.trim() !== '' && !mediaFile.value) {
    sendComment.value = true
    showPicker.value = false
    try {
      const response = await axios.post(`/api/comments/${pin.value.id}`, {
        content: comment.value.trim()
      })
      comment.value = ''

      cntComments.value += 1
      showCommets.value = false
      await nextTick()
      showCommets.value = true
      sendComment.value = false
      return;

    } catch (error) {
      console.error(error)
    }
  }

  if (mediaFile.value) {

    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm'];

    if (!allowedTypes.includes(mediaFile.value.type)) {
      toast.warning('Please select a valid media file (.jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm).', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
      return;
    }

    sendComment.value = true
    showPicker.value = false
    try {
      const formData = new FormData();
      formData.append("file", mediaFile.value); // Файл

      const jsonData = JSON.stringify({
        content: comment.value.trim()
      });

      formData.append("comment_model", jsonData); // Передаем строку, а не Blob

      const response = await axios.post(`/api/comments/create-comment-on-pin-entity/${pin.value.id}`, formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      comment.value = ''
      cntComments.value += 1
      showCommets.value = false
      await nextTick()
      showCommets.value = true
      resetFile()
      sendComment.value = false

    } catch (error) {
      if (error.response.status === 415) {
        sendComment.value = false
        sendCommentError.value = true
      }
    }
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

function onSelectEmoji(emoji) {
  comment.value += emoji.i
}

async function showVideoControls() {
  if (timeoutWorking.value) {
    clearTimeout(timeoutId.value)
  }
  showControls.value = true;
}

const pinImageRef = ref(null)

const showFollowing = ref(false)

const showViewLarge = ref(false)

const fullscreen = ref(false)

const zoom = ref(1)



function openImageFullScreen() {
  fullscreen.value = true
}

function closeFullscreen() {
  fullscreen.value = false
}

function increaseZoom() {
  zoom.value += 0.1
}

function decreaseZoom() {
  if (zoom.value > 0.2) { // Минимальное значение зума
    zoom.value -= 0.1
  }
}

const scrollToRelated = () => {
  relatedObserverTarget.value?.scrollIntoView({ behavior: 'smooth' })
}

const hoverImage = ref(false)
</script>


<template>

  <div v-if="showExplore === true && showMoreExplore" class="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-30">
    <button @click="scrollToRelated"
      class="flex items-center gap-2 px-3 py-3 bg-white/60 backdrop-blur text-black rounded-full hover:bg-white transition-all duration-300 text-sm font-medium">
      More to explore
      <svg class="w-4 h-4 text-black transition-transform group-hover:translate-y-1" fill="none" stroke="currentColor"
        stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
  </div>

  <div v-if="sendCommentError" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp,
            .png, .bmp, .mp4, .webm </h3>
          <button @click="sendCommentError = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="isModalOpen" class="z-[60] fixed inset-0 bg-black/50 flex items-center justify-center px-4"
    @click.self="closeModal">
    <div v-if="loadingBoards"
      class="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-lg max-w-2xl w-full relative backdrop-blur-lg overflow-auto max-h-screen min-h-[300px] flex items-center justify-center">
      <span class="text-center loader3"></span>
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
              <img v-if="pin.isImage" :src="pin.file" :alt="pin.title || 'Pin'" class="w-full object-cover rounded-md">
              <video v-else :src="pin.file" :alt="pin.title || 'Pin'" class="w-full object-cover rounded-md" autoplay
                loop muted></video>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <transition name="fade" appear>
    <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-50 p-6">
      <div class="flex justify-center items-center min-h-screen" @click.self="showFollowing = false">
        <PinLikesSection :pin_id="pin.id" :cnt_likes="cntLikes" />
        <i @click="showFollowing = false"
          class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
      </div>
    </div>
  </transition>
  <div v-if="fullscreen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80"
    @click.self="closeFullscreen">
    <!-- Кнопка закрытия в левом верхнем углу -->
    <button @click="closeFullscreen"
      class="absolute top-4 left-4 bg-white bg-opacity-80 rounded-full p-2 focus:outline-none justify-center text-center items-center flex">
      <i class="pi pi-times text-3xl font-bold"></i>
    </button>


    <div class="absolute top-4 right-4 flex flex-row gap-1">
      <span @click.stop="showBoards"
        :class="`px-6 py-3 text-sm bg-gray-800 hover:bg-black text-white rounded-3xl transition cursor-pointer`">
        {{ userSelectedBoardStore.selectedBoard ? `${userSelectedBoardStore.selectedBoard.title}` : "Profile" }}
      </span>

      <!-- Save Button -->
      <button @click="save" :style="{
        backgroundColor: pin.rgb,
      }" :class="`px-6 py-3 text-sm text-white rounded-3xl transition transform hover:scale-105`">
        {{ saveText }}
      </button>
    </div>

    <!-- Изображение с динамическим масштабом -->
    <img :src="pinImage" alt="Full screen image"
      class="max-h-full max-w-full rounded-3xl transition-transform duration-300"
      :style="{ transform: 'scale(' + zoom + ')' }" />


    <button @click="increaseZoom"
      class="absolute bottom-16 right-4 bg-white bg-opacity-80 rounded-full p-2 focus:outline-none justify-center text-center items-center flex">
      <i class="pi pi-plus text-2xl font-bold"></i>
    </button>

    <!-- Кнопка уменьшения (минус) -->
    <button @click="decreaseZoom"
      class="absolute bottom-4 right-4 bg-white bg-opacity-80 rounded-full p-2 focus:outline-none justify-center text-center items-center flex">
      <i class="pi pi-minus text-2xl font-bold "></i>
    </button>
  </div>
  <SearchBar />
  <div class="ml-20 mt-20">
    <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <div v-show="pinImageLoaded || pinVideoLoaded" class="grid grid-cols-2 gap-10 mx-60 bg-gray-100 rounded-3xl" :style="{
      boxShadow: `0 0 30px 15px ${pin.rgb}`
    }">
      <!-- Left Column: Image or Video -->
      <div>
        <div class="relative w-full max-w-2xl mx-auto" @mouseover="hoverImage = true"
        @mouseleave="hoverImage = false">
          <img ref="pinImageRef" v-if="pinImage" :src="pinImage" alt="Pin Image" class="h-auto w-full rounded-3xl"
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
          <div v-if="pinImageLoaded" class="absolute right-2 bottom-2 cursor-pointer" @mouseover="showViewLarge = true"
            @click="openImageFullScreen" @mouseleave="showViewLarge = false">
            <div :class="[
              'bg-white rounded-2xl bg-opacity-80 hover:bg-opacity-100 p-4 flex items-center justify-center transition-all duration-200 ease-in origin-right h-12',
              showViewLarge ? 'w-40' : 'w-12'
            ]" class="min-w-[3rem]">
              <span v-if="showViewLarge"
                class="mr-2 transition-opacity duration-300 ease-in-out text-md text-nowrap truncate">
                View larger
              </span>
              <i class="pi pi-arrow-up-right-and-arrow-down-left-from-center rotate-90"></i>
            </div>
          </div>

          <div v-if="!isLoading && pin.href && hoverImage" class="absolute left-2 bottom-2 cursor-pointer font-bold">
            <a :href="pin.href" target="_blank" class="w-full inline-block">
              <div
                :class="[
                  'bg-white rounded-full bg-opacity-80 hover:bg-opacity-100 p-4 flex items-center justify-center transition-all duration-200 ease-in origin-right h-12']">
                <i class="pi pi-arrow-up-right mr-2"></i>
                <span class="mr-2 transition-opacity duration-300 ease-in-out text-md text-nowrap truncate">
                  Visit site
                </span>
              </div>
            </a>
          </div>

        </div>
        <div class="relative w-full max-w-2xl mx-auto" @mouseover="showVideoControls"
          @mouseleave="showControls = false">
          <!-- Video Element -->
          <video @click="togglePlayPause" v-if="pinVideo" :src="pinVideo" ref="videoPlayer"
            class="w-full rounded-3xl block" loop @loadeddata="onVideoLoad" @timeupdate="updateProgress"
            @ended="onVideoEnd">
          </video>

          <!-- Gradient Overlay (cloud-like fade effect) -->
          <div v-if="pinVideoLoaded && showControls"
            class="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-red-900 to-transparent rounded-3xl">
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

      <div v-if="pinImageLoaded || pinVideoLoaded" v-show="isLoading" class="flex flex-col">
        <div class="flex items-center justify-center w-full h-full p-2">
          <span class="text-center loader2"></span>
        </div>
      </div>

      <div v-show="!isLoading" class="flex flex-col">
        <div class="flex items-center justify-between w-full p-2">
          <!-- Icon and Likes -->
          <div class="flex items-center space-x-4 relative">
            <!-- Icon -->
            <i v-if="checkUserLike" @click="likePin" :style="{ color: pin.rgb }"
              class="pi pi-heart-fill text-2xl cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>
            <i v-if="!checkUserLike" @click="likePin" :style="{ color: pin.rgb }"
              class="pi pi-heart text-2xl cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>
            <!-- Number of Likes -->

            <div @click="showFollowing = !showFollowing" v-if="cntLikes != 0"
              class="font-bold text-2xl relative cursor-pointer" @mouseover="showPopover = true"
              @mouseleave="if (!insidePopover) showPopover = false;">
              <div>
                <span :style="{ color: pin.rgb }">{{ cntLikes }}</span>
              </div>
              <div v-if="showPopover" @mouseover="insidePopover = true"
                @mouseleave="insidePopover = false; showPopover = false" class="absolute top-[30px] left-[-50px] z-50">
                <PinLikesPopover :pin_id="pin.id" />
              </div>
            </div>
          </div>

          <div class="flex flex-row gap-1">
            <span @click.stop="showBoards"
              :class="`px-6 py-3 text-sm bg-gray-800 hover:bg-black text-white rounded-3xl transition cursor-pointer`">
              {{ userSelectedBoardStore.selectedBoard ? `${userSelectedBoardStore.selectedBoard.title}` : "Profile" }}
            </span>

            <!-- Save Button -->
            <button @click="save" :style="{
              backgroundColor: pin.rgb,
            }" :class="`px-6 py-3 text-sm text-white rounded-3xl transition transform hover:scale-105`">
              {{ saveText }}
            </button>
          </div>

        </div>
        <div v-if="pin.title">
          <span :style="{ color: pin.rgb }" class="font-bold text-2xl">{{ pin.title }}</span>
        </div>
        <div class="mt-2" v-if="pin.description">
          <span class="">
            {{ pin.description }}
          </span>
        </div>
        <div class="mt-4 mr-5" v-if="pin.href">
          <a target="_blank" :href="pin.href"
            class="w-full inline-block text-center  py-3 bg-neutral-200  text-black font-medium rounded-full hover:bg-neutral-300 transition duration-300">
            Visit site
          </a>
        </div>
        <div class="flex flex-wrap gap-2 my-2" v-auto-animate>
          <div v-for="tag in tags" :key="tag.id" @click="showTagsPin(tag)"
            :class="[`${tag.color}`, 'text-sm', 'font-medium', 'rounded-3xl', 'px-3', 'py-2', 'cursor-pointer', 'transition-transform', 'duration-200', 'transform', 'hover:scale-110']">
            {{ tag.name }}
          </div>
        </div>
        <div>
          <RouterLink v-if="pinUser" :to="`/user/${pinUser.username}`"
            class="inline-flex items-center mt-2 hover:underline cursor-pointer">
            <img v-if="pinUserImage" :src="pinUserImage" alt="User Profile"
              class="w-10 h-10 rounded-full object-cover" />
            <span class="ml-2 text-md font-medium">@{{ pinUser.username }}</span>
          </RouterLink>
        </div>

        <div class="mt-5 mb-2 flex items-center justify-between cursor-pointer" v-if="cntComments != 0"
          @click="showCommets = !showCommets">
          <h1 class="text-xl">
            {{ cntComments }} Comments
          </h1>
          <span class="transition-transform duration-300 mr-5" :class="{ 'rotate-180': showCommets }">
            <i class="pi pi-angle-down text-xl"></i>
          </span>
        </div>
        <div v-else class="mt-5 mb-1">
          <h1 class="text-md  text-black ml-1">Your opinion?</h1>
        </div>
        <CommentSection v-if="showCommets" :pin_id="pin.id" class="mb-5" />
        <div v-if="isImage && !sendComment" class="relative">
          <div class="absolute top-0 left-[-10px]" @click="resetFile">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <img :src="mediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" alt="Media Preview" />
        </div>
        <div v-if="isVideo && !sendComment" class="relative">
          <div class="absolute top-0 left-[-10px] z-20" @click="resetFile">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <video :src="mediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" autoplay loop muted />
        </div>
        <div v-if="sendComment" class="flex items-center space-x-2 mb-4 mr-6 mt-2 justify-center">
          <span class="loader"></span>
        </div>
        <div v-if="!sendComment" class="flex items-center justify-center space-x-2 mb-4 mr-6 mt-2">
          <!-- Input for Comment -->
          <div ref="inputAddComment" class="relative w-full">
            <input v-model="comment" type="text" name="comment" id="comment" autocomplete="off"
              @keydown.enter="addComment"
              class="transition cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl py-3 px-5 pr-20 w-full focus:ring-black focus:border-black"
              placeholder="Add Comment" />

            <!-- Emoji Picker Button -->
            <button @click="loadPicker(); showPicker = !showPicker"
              class="absolute bottom-0.5 right-12 p-1 transition transform hover:scale-105">
              <i class="pi pi-face-smile text-2xl" :style="{ color: pin.rgb }"></i>
            </button>

            <!-- Media Upload Icon -->
            <label for="media" class="absolute bottom-0.5 right-4 p-1">
              <i :style="{ color: pin.rgb }"
                class="pi pi-images text-2xl cursor-pointer transition transform hover:scale-105"></i>
            </label>

            <input type="file" id="media" name="media" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp,.mp4,.webm"
              @change="handleMediaUpload" class="hidden" />

            <EmojiPicker v-show="showPicker" :theme="'dark'" :hide-search="true" :native="true" @select="onSelectEmoji"
              class="absolute right-0 z-40"
              :style="{ top: isTop ? '50px' : 'auto', bottom: isTop ? 'auto' : '50px' }" />
          </div>

          <!-- Emoji Picker -->
        </div>
      </div>
    </div>
  </div>
  <div ref="relatedObserverTarget">
    <RelatedPins v-if="pinImageLoaded || pinVideoLoaded" :pin_id="pin.id" @hasRelated="showExplore = true" />
  </div>
</template>


<style scoped>
.loader {
  width: 48px;
  height: 48px;
  display: inline-block;
  position: relative;
  border-width: 3px 2px 3px 2px;
  border-style: solid dotted solid dotted;
  border-color: #c50000 rgba(10, 255, 39, 0.3) #1c589e rgba(255, 101, 101, 0.836);
  border-radius: 50%;
  box-sizing: border-box;
  animation: 1s rotate linear infinite;
}

.loader:before,
.loader:after {
  content: '';
  top: 0;
  left: 0;
  position: absolute;
  border: 10px solid transparent;
  border-bottom-color: #a309d27a;
  transform: translate(-10px, 19px) rotate(-35deg);
}

.loader:after {
  border-color: #de3500 #670e6d00 #7b090900 #0000;
  transform: translate(32px, 3px) rotate(-35deg);
}

@keyframes rotate {
  100% {
    transform: rotate(360deg)
  }
}


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




.loader2 {
  width: 48px;
  height: 48px;
  background: #f3f4f6;
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

.loader3 {
  width: 48px;
  height: 48px;
  background: #ffffff;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

.loader3::after {
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