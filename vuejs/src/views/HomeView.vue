<script setup>
import { onMounted, ref, onBeforeUnmount, nextTick, watch, computed, onActivated, onDeactivated } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

import JSConfetti from 'js-confetti'

// import confetti from 'canvas-confetti'



import Pin from '@/components/Auth/Pin.vue';

import PinsByTag from '@/components/Auth/PinsByTag.vue';
import PinsBySearch from '@/components/Auth/PinsBySearch.vue';

const confetti = new JSConfetti()


import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();

const preLoadTags = ref(false)

import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();


const tagsContainer = ref(null)


const route = useRoute();
const router = useRouter()

const redirecting = ref(false)

const emit = defineEmits(['createPinModelClose'])


const lottieLoaded = ref(false)

const pins = ref([]);
const offset = ref(0);
const limit = ref(15);

const stagged = ref('0.03s')
const duration = ref('0.4s')

const cntLoading = ref(0)

const isPinsLoading = ref(false);

const cntTagLoading = ref(0)
const limitTagLoading = ref(null)

const tagFromUrl = ref(null)
const registerQuery = ref(null)

const available_tags = ref(null)
const bgColors = ref(['bg-red-200', 'bg-orange-200', 'bg-amber-200', 'bg-lime-200', 'bg-green-200', 'bg-emerald-200', 'bg-teal-200', 'bg-sky-200', 'bg-blue-200', 'bg-indigo-200', 'bg-violet-200', 'bg-purple-200', 'bg-fuchsia-200', 'bg-pink-200', 'bg-rose-200'])

const props = defineProps({
  register: Boolean
})

const showCreatePin = ref(false)

const loadPins = async () => {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;

  try {
    const response = await axios.get('/api/pins/', {
      params: { offset: offset.value, limit: limit.value },
      withCredentials: true,
    });

    // Append new pins to the existing ones

    const pinsObj = { pins: response.data, showAllPins: false }
    pinsObj.limitCntLoading = response.data.length
    pinsObj.cntLoading = 0
    pins.value.push(pinsObj);

    // Увеличиваем прогресс в зависимости от количества загруженных пинов

    // Increment the offset
    offset.value += limit.value;

    if (pinsObj.limitCntLoading == limit.value) {
      isPinsLoading.value = false
    }
    if (limit.value === 15) {
      limit.value = 5;
    }
  } catch (error) {
    console.log(error);
  } finally {
  }
};


const handleScroll = () => {
  const scrollableHeight = document.documentElement.scrollHeight;
  const currentScrollPosition = window.innerHeight + window.scrollY;

  // Загружаем новые пины только если пользователь достиг самого низа
  if (currentScrollPosition + 400 >= scrollableHeight) {
    loadPins();
  }
};


const randomBgColor = () => {
  const randomIndex = Math.floor(Math.random() * bgColors.value.length);
  return bgColors.value[randomIndex];
};

onMounted(async () => {

  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest`;
  } else {
    document.title = 'Pinterest';
  }

  loadPins();
  window.addEventListener('scroll', handleScroll);

  try {
    const response = await axios.get('/api/tags/tags-with-first-pin', { withCredentials: true });
    available_tags.value = response.data;
    limitTagLoading.value = available_tags.value.length;
  } catch (error) {
    console.log(error);
  }

  for (let i = 0; i < available_tags.value.length; i++) {
    available_tags.value[i].color = randomBgColor();
  }

  preLoadTags.value = true

  for (let i = 0; i < available_tags.value.length; i++) {


    available_tags.value[i].file = null
    available_tags.value[i].isImage = null
    available_tags.value[i].videoPlayer = null

    if (!available_tags.value[i].pinId) {
      available_tags.value[i].file = 'https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg';
      available_tags.value[i].isImage = true
    } else {
      try {
        const pinResponse = await axios.get(`/api/tags/tags-with-first-pin/upload/${available_tags.value[i].pinId}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          available_tags.value[i].file = blobUrl;
          available_tags.value[i].isImage = true;
        } else {
          available_tags.value[i].file = blobUrl;
          available_tags.value[i].isImage = false;
          available_tags.value[i].videoPlayer = null;
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});

function closeCreatePin() {
  showCreatePin.value = false
  document.body.style.overflowY = 'auto'
  emit('createPinModelClose')
}

const clearQuery = () => {
  router.replace({ path: route.path, query: {} });
};

onActivated(() => {
  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest`; // Если есть непрочитанные уведомления
  } else {
    document.title = 'Pinterest'; // Если уведомлений нет
  }
  if (selectedTag.value === 'Everything' && searchValue.value === '') {
    window.addEventListener('scroll', handleScroll);
  }

  registerQuery.value = route.query.register || '';

  if (registerQuery.value) {
    setTimeout(() => {
      confetti.addConfetti({
        emojis: ['🌈', '⚡️', '💥', '✨', '💫', '🦄'],
        confettiColors: ['#ff0a54', '#ff477e', '#ff7096', '#ff85a1', '#fbb1bd', '#f9bec7'],
        confettiRadius: 6,
        confettiNumber: 100,
        emojiSize: 40,
        emojiNumber: 50,
        shapes: ['circle', 'square'],
        confettiGravity: 0.5,
        confettiDrift: 0.1,
        confettiStartVelocity: 30,
        confettiAngle: 90,
        confettiSpread: 180,
        confettiDuration: 5000
      });
    }, 2000);
    clearQuery()
  }



  if (available_tags.value) {
    tagFromUrl.value = route.query.tag || '';
    if (tagFromUrl.value) {
      if (available_tags.value.some(tagObj => tagObj.name === tagFromUrl.value)) {
        loadPinsByTag(tagFromUrl.value);
        clearQuery()
      }
    }
    let searchFromUrl = route.query.search || '';
    if (searchFromUrl) {
      searchValue.value = searchFromUrl
      clearQuery()
    }
  }
  if (!tagsLoaded.value) {
    tagFromUrl.value = route.query.tag || '';
    let searchFromUrl = route.query.search || '';
    if (tagFromUrl.value || searchFromUrl) {
      redirecting.value = true
    }
  }
});

onDeactivated(() => {
  window.removeEventListener('scroll', handleScroll);
});



const selectedTag = ref('Everything')
const showPinsBytag = ref(false)

async function loadPinsByTag(name) {
  if (showSearchPins.value) {
    showSearchPins.value = false
  }
  if (name !== selectedTag.value) {
    showPinsBytag.value = false
    selectedTag.value = null
    if (name === 'Everything') {
      window.addEventListener('scroll', handleScroll);
      showPinsBytag.value = false
      selectedTag.value = 'Everything'
      searchValue.value = ''
    } else {
      window.removeEventListener('scroll', handleScroll);
      await nextTick();
      selectedTag.value = name
      showPinsBytag.value = true
    }
  }
}


const canScrollLeft = ref(false);
const canScrollRight = ref(false);


const scrollAmount = 400;

// Ссылка на контейнер с тегами
const containerRef = ref(null);


function updateScrollState() {
  if (!containerRef.value) return;

  const { scrollLeft, scrollWidth, clientWidth } = containerRef.value;
  canScrollLeft.value = scrollLeft > 0;
  // Если разница между полным размером содержимого и видимой областью больше 1 пикселя, считаем, что можно прокручивать вправо
  canScrollRight.value = scrollLeft < (scrollWidth - clientWidth - 1);
}


function customScroll(container, amount, duration = 300) {
  const start = container.scrollLeft;
  const startTime = performance.now();

  // Функция плавного перехода (easeInOutQuad)
  function ease(t) {
    return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
  }

  function scrollStep(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeValue = ease(progress);

    container.scrollLeft = start + amount * easeValue;

    if (elapsed < duration) {
      requestAnimationFrame(scrollStep);
    }
  }

  requestAnimationFrame(scrollStep);
}

// Функция для прокрутки влево
const scrollLeft = () => {
  if (containerRef.value) {
    // containerRef.value.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    customScroll(containerRef.value, -scrollAmount, 300);
  }
};

// Функция для прокрутки вправо
const scrollRight = () => {
  if (containerRef.value) {
    // containerRef.value.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    customScroll(containerRef.value, scrollAmount, 300);
  }
};


const tagsLoaded = ref(false)

function onTagLoad() {
  cntTagLoading.value += 1
  if (cntTagLoading.value === limitTagLoading.value) {
    tagsLoaded.value = true
  }
}

watch(tagsLoaded, (newTags) => {
  if (newTags) {
    redirecting.value = false
    tagFromUrl.value = route.query.tag || '';
    if (tagFromUrl.value) {
      if (available_tags.value.some(tagObj => tagObj.name === tagFromUrl.value)) {
        loadPinsByTag(tagFromUrl.value);
        clearQuery()
      }
    }
    let searchFromUrl = route.query.search || '';
    if (searchFromUrl) {
      searchValue.value = searchFromUrl
      clearQuery()
    }
  }
});

const showSearchPins = ref(false)
const searchValue = ref('')

watch(searchValue, async (newValue, oldValue) => {
  if (newValue.trim() !== '') {
    selectedTag.value = ''
    showSearchPins.value = false
    showPinsBytag.value = false
    window.removeEventListener('scroll', handleScroll);
    await nextTick()
    searchValue.value = newValue
    showSearchPins.value = true
  } else {
    if (oldValue.trim() !== '') {
      showSearchPins.value = false
      loadPinsByTag('Everything')
    }
  }
});


const filteredTags = computed(() => {
  const trimmedValue = searchValue.value.trim().toLowerCase();
  let filtered = [];

  if (trimmedValue === '') {
    // Если строка поиска пустая, возвращаем все теги
    filtered = available_tags.value;
  } else {
    // Разбиваем поисковую строку на слова
    const searchWords = trimmedValue.split(/\s+/); // Разделяем по пробелам
    filtered = available_tags.value.filter(tag =>
      searchWords.some(word => tag.name.toLowerCase().includes(word))
    );
  }

  // Убедимся, что тег "Everything" всегда присутствует
  const everythingTag = (available_tags.value || []).find(tag => tag.name.toLowerCase() === 'everything');

  if (everythingTag && !filtered.some(tag => tag.name.toLowerCase() === 'everything')) {
    filtered.unshift(everythingTag); // Добавляем "Everything" в начало
  }

  return filtered;
});

const isActive = ref(false)

</script>

<template>
  <nav :class="['fixed top-0 left-20 w-full  z-30', 'backdrop-blur-sm']">
    <div class="flex items-center justify-between px-6 py-2">
      <div class="relative flex-1 mr-20">
        <input v-model="searchValue" type="text" placeholder="Search" class="transition-all duration-300 cursor-text
               bg-white bg-opacity-20 backdrop-blur-sm text-black
               text-md rounded-3xl block w-full py-3 pl-12 pr-10
               outline-none border border-black
               focus:shadow-lg focus:shadow-blue-500/50" />
        <div class="absolute left-1 top-4 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-black"></i>
        </div>
      </div>
    </div>
  </nav>

  <div v-if="redirecting"
    class="fixed inset-0 bg-black bg-opacity-40 z-50 items-center justify-center flex flex-col gap-20">
    <img src="/logo.png" alt="Logo" class="w-24 h-24 logo bg-white rounded-full" />
  </div>

  <!-- Контейнер с тегами -->
  <div ref="tagsContainer" class="mt-16 ml-20 group fixed top-0 right-0 left-0 z-30 backdrop-blur-sm">
    <!-- Левая стрелка -->
    <button
      class="absolute left-5 top-1/2 transform -translate-y-1/2 z-20 bg-white rounded-full px-3 py-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 active:scale-75"
      @click="scrollLeft(containerRef)">
      <i class="pi pi-chevron-left text-xl"></i>
    </button>

    <!-- Контейнер с градиентами -->
    <div v-if="preLoadTags" class="relative overflow-hidden">
      <!-- Градиенты для эффекта свечения -->
      <div
        class="absolute top-0 left-0 w-32 h-full bg-gradient-to-r from-white via-white/50 to-transparent pointer-events-none z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      </div>
      <div
        class="absolute top-0 right-0 w-32 h-full bg-gradient-to-l from-white via-white/50 to-transparent pointer-events-none z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      </div>

      <!-- Контейнер с тегами -->
      <div ref="containerRef" class="flex gap-2 overflow-x-auto whitespace-nowrap scrollbar-hide p-0.5 px-5"
        v-auto-animate>
        <div v-for="tag in filteredTags" :key="tag.id" @click="loadPinsByTag(tag.name)"
          :class="[tag.name == selectedTag ? 'bg-black text-white shadow-lg scale-105' : `${tag.color}`, 'flex', 'items-center', 'gap-1', 'text-sm', 'rounded-3xl', 'pl-2 pr-5', 'py-1', 'cursor-pointer', 'transition-transform', 'duration-100', 'transform', 'hover:scale-110']">
          <!-- Изображение или видео -->
          <div class="w-9 h-9 flex-shrink-0">
            <img v-show="tagsLoaded" v-if="tag.isImage && tag.file" :src="tag.file" alt="Tag Image" @load="onTagLoad"
              class="w-full h-full object-cover rounded-full fade-in" :class="{ 'fade-in-animation': tagsLoaded }" />
            <video v-show="tagsLoaded" v-else-if="!tag.isImage && tag.file" :src="tag.file" @loadeddata="onTagLoad"
              @mouseover="tag.videoPlayer.play()" :ref="el => { if (el) tag.videoPlayer = el; }"
              class="w-full h-full object-cover rounded-full fade-in" :class="{ 'fade-in-animation': tagsLoaded }"
              autoplay loop muted />
            <div v-show="!tagsLoaded" class="bg-gray-100 w-full h-full object-cover rounded-full animate-pulse">
            </div>
          </div>
          <!-- Название тега -->
          <span class="truncate">{{ tag.name }}</span>
        </div>
      </div>
    </div>

    <!-- Правая стрелка -->
    <button
      class="absolute right-5 top-1/2 transform -translate-y-1/2 z-20 bg-white rounded-full px-3 py-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 active:scale-75"
      @click="scrollRight(containerRef)">
      <i class="pi pi-chevron-right text-xl"></i>
    </button>
  </div>




  <div v-show="!showPinsBytag && !showSearchPins" class="ml-20 mt-28" v-masonry transition-duration="0.000000001s"
    item-selector=".item" stagger="0.000000001s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <Pin v-masonry-tile class="item " v-for="pinem in pinGroup.pins" :key="pinem.id" :pin="pinem"
        @pinLoaded="() => { pinGroup.cntLoading++; if (pinGroup.cntLoading === pinGroup.limitCntLoading) { pinGroup.showAllPins = true; } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
  <PinsByTag class="mt-28" v-if="showPinsBytag && selectedTag !== null && !showSearchPins" :tag="selectedTag" />
  <PinsBySearch class="mt-28" v-if="showSearchPins" :value="searchValue" />
</template>


<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  transform: scale(1);
}

/* Лёгкое свечение при фокусе */
input:focus {
  box-shadow: 0 0 8px rgba(199, 88, 151, 0.9);
}





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



@keyframes pulse-scale {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.5);
  }

  100% {
    transform: scale(1);
  }
}

.logo {
  animation: pulse-scale 1.5s infinite ease-in-out;
}
</style>