<template>
  <div 
    class=" relative group overflow-hidden  bg-white/20 border border-white/30 backdrop-blur-lg shadow-xl transition transform hover:scale-105 hover:shadow-2xl cursor-pointer">
    <!-- Скриншот -->
    <img v-show="!canPlay" :src="card.src" :alt="card.title" class="w-full h-screen object-cover  " />
    <video ref="videoPlayer" v-show="canPlay" :src="`/api/sse/notauth/video-stream/${props.card.stream}`" muted loop
      autoplay class="w-full h-full " @canplay="canPlay = true" />


    <!-- Оверлей с описанием (для ховера) -->
    <div v-if="!canPlay"
      class="absolute inset-0 flex flex-col items-center justify-center opacity-100 group-hover:opacity-0 transition duration-500 p-6 rounded-2xl z-20">
      <!-- Обертка для черного облака -->
      <div class="relative p-4 rounded-3xl text-center">
        <div class="absolute inset-0 bg-white rounded-3xl opacity-80 blur-xl"></div>
        <div class="relative z-50 p-4 flex flex-col items-center justify-center">
          <!-- Pinterest логотип -->
          <img :src="pinterest_logo" class="w-14 h-14" />
          <h2
            class="text-4xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-black to-pink-600 mb-2 drop-shadow-lg">
            {{ card.title }}
          </h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import pinterest_logo from '@/assets/logo.png';

const videoPlayer = ref(null)

const canPlay = ref(false)

const props = defineProps({
  card: Object
})

const showVideo = ref(false)

const glowX = ref(0)
const glowY = ref(0)
const glowVisible = ref(true)

const handleMouseMove = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  glowX.value = event.clientX - rect.left
  glowY.value = event.clientY - rect.top
}

let timeoutId = null;

const handleMouseEnter = () => {
  glowVisible.value = true;
};

</script>

<style scoped>
/* Кастомное правило для radial-gradient */
.bg-gradient-radial {
  background-image: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>