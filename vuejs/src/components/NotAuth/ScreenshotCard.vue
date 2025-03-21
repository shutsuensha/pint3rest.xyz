<template>
  <div data-kinesisdepth data-ks-sensitivity="20"
    class="p-10 relative group overflow-hidden rounded-2xl bg-white/20 border border-white/30 backdrop-blur-lg shadow-xl transition transform hover:scale-105 hover:shadow-2xl cursor-pointer"
    @mousemove="handleMouseMove" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @click="$emit('click')">
    <!-- Скриншот -->
    <img v-show="!showVideo" data-kinesisdepth-element data-ks-depth="400" :src="card.src" :alt="card.title"
      class="w-full h-[250px] object-cover rounded-2xl" />
    <video ref="videoElement" v-if="videoSrc" v-show="showVideo" autoplay muted loop class="w-full h-[250px] object-cover rounded-2xl"
      data-kinesisdepth-element data-ks-depth="200" @loadeddata="onVideoLoaded" @canplay="onVideoCanPlay">
      <source :src="videoSrc" type="video/mp4" />
    </video>

    <!-- Неоновое свечение под курсором -->
    <div
      class="pointer-events-none absolute w-48 h-48 rounded-full bg-gradient-radial from-pink-700 via-pink-600 to-transparent blur-3xl transition duration-300 mix-blend-screen z-50"
      :style="{
        top: glowY + 'px',
        left: glowX + 'px',
        transform: 'translate(-50%, -50%)',
        opacity: glowVisible ? 1 : 0.7
      }"></div>

    <!-- Оверлей с описанием (для ховера) -->
    <div
      class="absolute inset-0 flex flex-col items-center justify-center opacity-100 group-hover:opacity-0 transition duration-500 p-6 rounded-2xl z-20">
      <div class="relative p-4 rounded-3xl text-center">
        <div class="absolute inset-0 bg-white rounded-3xl opacity-80 blur-xl"></div>
        <div class="relative z-50 p-4">
          <h2 data-kinesisdepth-element data-ks-depth="800"
            class="text-4xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-black to-red-600 mb-2 drop-shadow-lg">
            {{ card.title }}
          </h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const props = defineProps({
  card: Object
});

const videoSrc = ref(null);
const showVideo = ref(false);
const streamLoaded = ref(false);
const streamCanPlay = ref(false);

const glowX = ref(0);
const glowY = ref(0);
const glowVisible = ref(false);

const videoElement = ref(null);
let timeoutId = null;

const handleMouseMove = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  glowX.value = event.clientX - rect.left;
  glowY.value = event.clientY - rect.top;
};

const onVideoLoaded = () => {
  streamLoaded.value = true;
};

const onVideoCanPlay = () => {
  streamCanPlay.value = true;
};

const handleMouseEnter = () => {
  glowVisible.value = true;
  timeoutId = setTimeout(() => {
    videoSrc.value = `/api/notauth/video-stream/${props.card.stream}`;
    showVideo.value = true;
  }, 1000);
};

const handleMouseLeave = async () => {
  glowVisible.value = false;
  showVideo.value = false;
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
  // Останавливаем воспроизведение видео, если элемент существует
  await nextTick();
  if (videoElement.value) {
    videoElement.value.pause();
    videoElement.value.removeAttribute('src'); // Это прерывает загрузку видео
    videoElement.value.load();
  }
  videoSrc.value = null;
  streamLoaded.value = false;
  streamCanPlay.value = false;
};
</script>

<style scoped>
/* Кастомное правило для radial-gradient */
.bg-gradient-radial {
  background-image: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>
