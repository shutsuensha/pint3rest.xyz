<script setup>
import { onMounted, ref, onBeforeUnmount, nextTick, watch, computed, onActivated, onDeactivated } from 'vue';
import axios from 'axios';
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'

import Pin from '@/components/Auth/Pin.vue';

import PinsByTag from '@/components/Auth/PinsByTag.vue';
import PinsBySearch from '@/components/Auth/PinsBySearch.vue';



const emit = defineEmits(['createPinModelClose'])


const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

const cntTagLoading = ref(0)
const limitTagLoading = ref(null)

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
    pins.value.push({ pins: response.data, showAllPins: false });

    limitCntLoading.value = response.data.length

    limitCntLoading.value

    // Increment the offset
    offset.value += limit.value;

    // После первого запроса изменяем лимит на 5
    if (limit.value === 10) {
      limit.value = 5;
    }

  } catch (error) {
    console.log(error);
  }
};

const handleScroll = () => {
  const scrollableHeight = document.documentElement.scrollHeight;
  const currentScrollPosition = window.innerHeight + window.scrollY;

  // Trigger loadPins if user reaches bottom
  if (currentScrollPosition + 200 >= scrollableHeight) {
    loadPins();
  }
};

const randomBgColor = () => {
  const randomIndex = Math.floor(Math.random() * bgColors.value.length);
  return bgColors.value[randomIndex];
};

onMounted(async () => {
  document.title = 'pinterest.xyz'
  loadPins();
  window.addEventListener('scroll', handleScroll);
  if (props.register === true) {
    setTimeout(() => {
      showCreatePin.value = true
      document.body.style.overflowY = 'clip'
    }, 2000);
  }
  try {
    const response = await axios.get('/api/tags/', { withCredentials: true })
    available_tags.value = response.data
    limitTagLoading.value = available_tags.value.length
    for (let i = 0; i < response.data.length; i++) {
      const tag = response.data[i];
      tag.color = randomBgColor()
    }
    available_tags.value.unshift({ id: available_tags.value.length, name: 'Everything', color: randomBgColor(), file: null, isImage: null });
    try {
      const response = await axios.get(`/api/pins/`, {
        params: { offset: 0, limit: 1 },
        withCredentials: true,
      })
      const pin_id = response.data[0].id
      try {
        const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(pinResponse.data);
        const contentType = pinResponse.headers['content-type'];
        if (contentType.startsWith('image/')) {
          available_tags.value[0].file = blobUrl;
          available_tags.value[0].isImage = true
        } else {
          available_tags.value[0].file = blobUrl;
          available_tags.value[0].isImage = false
        }
      } catch (error) {
        console.error(error);
      }
    } catch (error) {
      console.error(error)
    }
  } catch (error) {
    console.log(error)
  }
  for (let i = 1; i < available_tags.value.length; i++) {
    try {
      const response = await axios.get(`/api/pins/tag/${available_tags.value[i].name}`, {
        params: { offset: 0, limit: 1 },
        withCredentials: true,
      })

      if (response.data.length === 1) {
        const pin_id = response.data[0].id

        try {
          const pinResponse = await axios.get(`/api/pins/upload/${pin_id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(pinResponse.data);
          const contentType = pinResponse.headers['content-type'];
          if (contentType.startsWith('image/')) {
            available_tags.value[i].file = blobUrl;
            available_tags.value[i].isImage = true
          } else {
            available_tags.value[i].file = blobUrl;
            available_tags.value[i].isImage = false
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        available_tags.value[i].file = 'https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg';
        available_tags.value[i].isImage = true
      }

    } catch (error) {
      console.error(error)
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

onActivated(() => {
  document.title = 'pinterest.xyz'
  window.addEventListener('scroll', handleScroll);
});

onDeactivated(() => {
  window.removeEventListener('scroll', handleScroll);
}); 



const selectedTag = ref('Everything')
const showPinsBytag = ref(false)

async function loadPinsByTag(name) {
  if (showSearchPins.value) {
    showSearchPins.value = false
    window.addEventListener('scroll', handleScroll);
    searchValue.value = ''
  }
  if (name !== selectedTag.value) {
    showPinsBytag.value = false
    selectedTag.value = null
    if (name === 'Everything') {
      window.addEventListener('scroll', handleScroll);
      showPinsBytag.value = false
      selectedTag.value = 'Everything'
    } else {
      window.removeEventListener('scroll', handleScroll);
      await nextTick();
      selectedTag.value = name
      showPinsBytag.value = true
    }
  }
}

const scrollAmount = 400;

// Ссылка на контейнер с тегами
const containerRef = ref(null);

function customScroll(container, amount, duration = 300) {
  const start = container.scrollLeft;
  const startTime = performance.now();

  function scrollStep(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1); // Ensure progress doesn't exceed 1
    const ease = 0.5 - 0.5 * Math.cos(Math.PI * progress); // Ease-in-out effect

    container.scrollLeft = start + amount * ease;

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

const showSearchPins = ref(false)
const searchValue = ref('')

watch(searchValue, async (newValue, oldValue) => {
  if (newValue.trim() !== '') {
    showSearchPins.value = false
    window.removeEventListener('scroll', handleScroll);
    await nextTick()
    searchValue.value = newValue
    showSearchPins.value = true
  } else {
    if (oldValue.trim() !== '') {
      showSearchPins.value = false
      window.addEventListener('scroll', handleScroll);
    }
  }
});


const filteredTags = computed(() => {
  const trimmedValue = searchValue.value.trim().toLowerCase();
  if (trimmedValue === '') {
    return available_tags.value; // Возвращаем все теги, если строка поиска пустая
  }

  // Разбиваем поисковую строку на слова
  const searchWords = trimmedValue.split(/\s+/); // Разделяем по пробелам
  return available_tags.value.filter(tag =>
    searchWords.some(word => tag.name.toLowerCase().includes(word))
  );
});
</script>

<template>
  <transition name="fade" appear>
    <div v-if="showCreatePin" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <div class="flex flex-col items-start justify-start">
        <DotLottieVue class="ml-4"
          style="height: 210px; width: 250px; filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.8)) drop-shadow(0 0 30px rgba(255, 255, 255, 0.6));"
          autoplay loop src="https://lottie.host/283cf83b-92ee-4d44-93d9-d62849b90da3/LCwNUy8wJT.lottie" />

        <!-- Centered Text with Glow (Positioned top-left) -->
        <p class="text-white text-3xl font-cursive mb-2"
          style="text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 255, 255, 0.6);">
          Create your first pin!
        </p>
      </div>

      <button @click="closeCreatePin"
        class="absolute top-72 left-36 px-6 py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
        style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
        Done
      </button>

      <!-- Centered Button with Glow -->
    </div>
  </transition>

  <nav :class="['fixed top-0 left-20 w-full bg-white z-30', 'bg-opacity-20 backdrop-blur-sm']">
    <div class="flex items-center justify-between px-6 py-2">
      <!-- Search Bar -->

      <div class="relative flex-1 mr-20">
        <input v-model="searchValue" type="text" placeholder="Search"
          class="transition duration-300 cursor-pointer bg-gray-200 hover:bg-gray-300 text-md rounded-3xl block w-full py-3 px-10 outline-none border-none focus:ring-0" />
        <div class="absolute left-1 top-4 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-600"></i>
        </div>
      </div>
    </div>
  </nav>


  <div class="mt-16 ml-20 group bg-white fixed top-0 right-0 left-0 z-30 bg-opacity-20 backdrop-blur-sm">
    <!-- Левая стрелка -->
    <button
      class="absolute left-5 top-1/2 transform -translate-y-1/2 z-20 bg-white rounded-full px-4 py-2 hover:-translate-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 active:scale-75"
      @click="scrollLeft(containerRef)">
      <i class="pi pi-chevron-left text-xl"></i>
    </button>

    <!-- Контейнер с градиентами -->
    <div class="relative overflow-hidden">
      <!-- Облака (градиенты) видны только при наведении на контейнер -->
      <div
        class="absolute top-0 left-0 w-32 h-full bg-gradient-to-r from-white via-white/70 to-transparent pointer-events-none z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      </div>
      <div
        class="absolute top-0 right-0 w-32 h-full bg-gradient-to-l from-white via-white/70 to-transparent pointer-events-none z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      </div>

      <!-- Контейнер с тегами -->
      <div ref="containerRef" class="flex gap-2 overflow-x-auto whitespace-nowrap scrollbar-hide p-0.5 px-5"
        v-auto-animate>
        <div v-for="tag in filteredTags" :key="tag.id" @click="loadPinsByTag(tag.name)"
          :class="[tag.name == selectedTag ? 'bg-black text-white shadow-lg scale-105' : `${tag.color}`, 'flex', 'items-center', 'gap-1', 'text-sm', 'rounded-3xl', 'pl-2 pr-5', 'py-1', 'cursor-pointer', 'transition-transform', 'duration-100', 'transform', 'hover:scale-110']">
          <!-- Отображение изображения или видео -->
          <div class="w-9 h-9 flex-shrink-0">
            <img v-show="tagsLoaded" v-if="tag.isImage && tag.file" :src="tag.file" alt="Tag Image" @load="onTagLoad"
              class="w-full h-full object-cover rounded-full fade-in" :class="{ 'fade-in-animation': tagsLoaded }" />
            <video v-show="tagsLoaded" v-else-if="!tag.isImage && tag.file" :src="tag.file" @loadeddata="onTagLoad"
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
      class="absolute right-5 top-1/2 transform -translate-y-1/2 z-20 bg-white rounded-full px-4 py-2 hover:translate-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 active:scale-75"
      @click="scrollRight(containerRef)">
      <i class="pi pi-chevron-right text-xl"></i>
    </button>
  </div>




  <div v-show="!showPinsBytag && !showSearchPins" class="ml-20 mt-28" v-masonry transition-duration="0.4s"
    item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <Pin v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id" :pin="pinem"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
  <PinsByTag class="mt-28" v-if="showPinsBytag && selectedTag !== null && !showSearchPins" :tag="selectedTag" />
  <PinsBySearch class="mt-28" v-if="showSearchPins" :value="searchValue" />
</template>


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