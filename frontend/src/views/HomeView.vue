<script setup>
import { onMounted, ref, onBeforeUnmount, nextTick } from 'vue';
import axios from 'axios';
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'

import Pin from '@/components/Auth/Pin.vue';

import PinsByTag from '@/components/Auth/PinsByTag.vue';

const emit = defineEmits(['createPinModelClose'])

const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

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
  loadPins();
  window.addEventListener('scroll', handleScroll);
  try {
    const response = await axios.get('/api/tags/', { withCredentials: true })
    available_tags.value = response.data
    for (let i = 0; i < response.data.length; i++) {
      const tag = response.data[i];
      tag.color = randomBgColor()
    }
    available_tags.value.unshift({ id: available_tags.value.length, name: 'All', color: randomBgColor() });
  } catch (error) {
    console.log(error)
  }
  for (let i = 1; i < available_tags.value.length; i++) {
    try {
      const response = await axios.get(`/api/pins/tag/${available_tags.value[i].name}`, {
        params: { offset: 0, limit: 1 },
        withCredentials: true,
      })
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

    } catch (error) {
      console.error(error)
    }
  }
  if (props.register === true) {
    setTimeout(() => {
      showCreatePin.value = true
      document.body.style.overflowY = 'clip'
    }, Math.random() * 2000);
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


const selectedTag = ref('All')
const showPinsBytag = ref(false)

async function loadPinsByTag(name) {
  if (name !== selectedTag.value) {
    showPinsBytag.value = false
    selectedTag.value = null
    if (name === 'All') {
      window.addEventListener('scroll', handleScroll);
      showPinsBytag.value = false
      selectedTag.value = 'All'
    } else {
      window.removeEventListener('scroll', handleScroll);
      await nextTick();
      selectedTag.value = name
      showPinsBytag.value = true
    }
  }
}

const scrollAmount = 200;

// Ссылка на контейнер с тегами
const containerRef = ref(null);

// Функция для прокрутки влево
const scrollLeft = () => {
  if (containerRef.value) {
    containerRef.value.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  }
};

// Функция для прокрутки вправо
const scrollRight = () => {
  if (containerRef.value) {
    containerRef.value.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  }
};

</script>

<template>
  <transition name="fade" appear>
    <div v-if="showCreatePin" class="fixed inset-0 bg-black bg-opacity-75 z-50 p-6">

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
        Ok
      </button>

      <!-- Centered Button with Glow -->
    </div>
  </transition>


  <div class="relative mt-20 ml-24">
    <!-- Левая стрелка -->
    <button
      class="absolute left-0 top-1/2 transform -translate-y-1/2 z-10 bg-gray-200 rounded-full p-2 shadow hover:bg-gray-300"
      @click="scrollLeft(containerRef)">
      ◀
    </button>

    <!-- Контейнер с тегами -->
    <div ref="containerRef"
      class="flex gap-2 overflow-x-auto whitespace-nowrap scrollbar-hide p-1"
      v-auto-animate>
      <div v-for="tag in available_tags" :key="tag.id" @click="loadPinsByTag(tag.name)"
        :class="[tag.name == selectedTag ? 'bg-black text-white shadow-lg scale-105' : `${tag.color}`, 'flex', 'items-center', 'gap-1', 'text-sm', '', 'rounded-3xl', 'pl-2 pr-5', 'py-1', 'cursor-pointer', 'transition-transform', 'duration-200', 'transform', 'hover:scale-105']">
        <!-- Отображение изображения или видео -->
        <div class="w-9 h-9 flex-shrink-0">
          <img v-if="tag.isImage && tag.file" :src="tag.file" alt="Tag Image"
            class="w-full h-full object-cover rounded-full" />
          <video v-else-if="!tag.isImage && tag.file" :src="tag.file" class="w-full h-full object-cover rounded-full"
            autoplay loop muted />
        </div>
        <!-- Название тега -->
        <span class="truncate">{{ tag.name }}</span>
      </div>
    </div>

    <!-- Правая стрелка -->
    <button
      class="absolute right-0 top-1/2 transform -translate-y-1/2 z-10 bg-gray-200 rounded-full p-2 shadow hover:bg-gray-300"
      @click="scrollRight(containerRef)">
      ▶
    </button>
  </div>


  <div v-show="!showPinsBytag" class="ml-20" v-masonry transition-duration="0.4s" item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <Pin v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id" :pin="pinem"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
  <PinsByTag v-if="showPinsBytag && selectedTag !== null" :tag="selectedTag" />
</template>


<style>
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
</style>