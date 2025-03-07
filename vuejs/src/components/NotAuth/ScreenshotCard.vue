<template>
  <div
    data-kinesisdepth
    data-ks-sensitivity="20"
    class="p-10 relative group overflow-hidden rounded-2xl bg-white/20 border border-white/30 backdrop-blur-lg shadow-xl transition transform hover:scale-105 hover:shadow-2xl cursor-pointer"
    @mousemove="handleMouseMove"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    @click="$emit('click')"
  >
    <!-- Скриншот занимает весь контейнер -->
    <img
      data-kinesisdepth-element
      data-ks-depth="400"
      v-show="!videoLoaded"
      :src="card.src"
      :alt="card.title"
      class="w-full h-64 object-cover rounded-2xl"
    />

    <!-- Видео занимает весь контейнер -->
    <video
      ref="videoEl"
      :src="card.video"
      class="absolute inset-0 w-full h-full object-cover rounded-2xl"
      muted
      loop
      v-if="isHovered"
      v-show="videoLoaded"
      @canplaythrough="onVideoLoad"
      @ended="onVideoEnded"
    ></video>

    <!-- Неоновое свечение под курсором -->
    <div
      class="pointer-events-none absolute w-48 h-48 rounded-full bg-gradient-radial from-pink-700 via-pink-600 to-transparent blur-3xl transition duration-300 mix-blend-screen z-50"
      :style="{
        top: glowY + 'px',
        left: glowX + 'px',
        transform: 'translate(-50%, -50%)',
        opacity: glowVisible ? 1 : 0.7
      }"
    ></div>

    <!-- Оверлей с описанием (показывается только когда видео не воспроизводится) -->
    <div
      v-show="!videoLoaded"
      class="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition duration-500 p-6 rounded-2xl z-20"
    >
      <div class="relative p-4 rounded-3xl text-center">
        <div class="absolute inset-0 bg-white rounded-3xl opacity-80 blur-xl"></div>
        <div class="relative z-50 p-4">
          <h2
            data-kinesisdepth-element
            data-ks-depth="800"
            class="text-4xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-indigo-700 to-purple-900 mb-2 drop-shadow-lg"
          >
            {{ card.title }}
          </h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  card: Object
})

// Неоновое свечение
const glowX = ref(0)
const glowY = ref(0)
const glowVisible = ref(false)

// Флаги управления видео
const isHovered = ref(false)
const videoLoaded = ref(false)
const showVideo = ref(false)
const videoEl = ref(null)
const hasPlayedOnce = ref(false) // Флаг, что видео уже проигралось за текущий hover
let hoverTimer = null

const handleMouseMove = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  glowX.value = event.clientX - rect.left
  glowY.value = event.clientY - rect.top
}


const hoverTwoSeconds = ref(false)

const startHoverTimer = () => {
    hoverTimer = setTimeout(() => {
      hoverTwoSeconds.value = true
    }, 2000) 
}

const handleMouseEnter = () => {
  glowVisible.value = true
  isHovered.value = true
}

const handleMouseLeave = () => {
  isHovered.value = false
  videoLoaded.value = false
  // glowVisible.value = false
  // isHovered.value = false
  // showVideo.value = false
  // hasPlayedOnce.value = false
  // if (hoverTimer) {
  //   clearTimeout(hoverTimer)
  //   hoverTimer = null
  // }
  // if (videoEl.value) {
  //   videoEl.value.pause()
  //   videoEl.value.currentTime = 0
  // }
}

const onCanPlay = () => {
  videoLoaded.value = true
  if (isHovered.value && showVideo.value && videoEl.value) {
    videoEl.value.play().catch(() => {})
  }
}

const onVideoLoad = () => {
  videoLoaded.value = true
  videoEl.value.play()
}

const onVideoEnded = () => {
  
}
</script>

<style scoped>
/* Кастомное правило для radial-gradient */
.bg-gradient-radial {
  background-image: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>
