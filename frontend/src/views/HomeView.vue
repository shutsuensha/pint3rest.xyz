<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import axios from 'axios';
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'

import Pin from '@/components/Auth/Pin.vue';

const emit = defineEmits(['createPinModelClose'])

const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

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

onMounted(() => {
  loadPins();  // Initial load
  window.addEventListener('scroll', handleScroll);
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


  <div class="mt-20 ml-20" v-masonry transition-duration="0.4s" item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <Pin v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id" :pin="pinem"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
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
</style>