<template>
  <div
    class="relative group overflow-hidden rounded-2xl bg-white/20 border border-white/30 backdrop-blur-lg shadow-xl transition transform hover:scale-105 hover:shadow-2xl cursor-pointer"
    @mousemove="handleMouseMove"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    @click="$emit('click')"
  >
    <!-- Скриншот -->
    <img :src="card.src" :alt="card.title" class="w-full h-64 object-cover rounded-t-2xl" />

    <!-- Неоновое свечение под курсором -->
    <div
      class="pointer-events-none absolute w-48 h-48 rounded-full bg-gradient-radial from-pink-500 via-pink-400 to-transparent blur-3xl transition duration-300 mix-blend-screen"
      :style="{
        top: glowY + 'px',
        left: glowX + 'px',
        transform: 'translate(-50%, -50%)',
        opacity: glowVisible ? 1 : 0.7
      }"
    ></div>

    <!-- Оверлей с описанием (для ховера) -->
    <div class="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition duration-500 bg-black/70 p-6 rounded-2xl z-20">
      <h2 class="text-2xl font-semibold text-white mb-2 drop-shadow-lg">{{ card.title }}</h2>
      <p class="text-lg text-white drop-shadow-md">{{ card.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  card: Object
})

const glowX = ref(0)
const glowY = ref(0)
const glowVisible = ref(false)

const handleMouseMove = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  glowX.value = event.clientX - rect.left
  glowY.value = event.clientY - rect.top
}

const handleMouseEnter = () => {
  glowVisible.value = true
}

const handleMouseLeave = () => {
  glowVisible.value = false
}
</script>

<style scoped>
/* Кастомное правило для radial-gradient */
.bg-gradient-radial {
  background-image: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>
