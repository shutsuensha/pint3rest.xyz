<template>
  <div
  data-kinesisdepth
  data-ks-sensitivity="20"
    class="p-10 relative group overflow-hidden rounded-2xl bg-white/20 border border-white/30 backdrop-blur-lg shadow-xl transition transform hover:scale-105 hover:shadow-2xl cursor-pointer"
    @mousemove="handleMouseMove" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @click="$emit('click')">
    <!-- Скриншот -->
    <img data-kinesisdepth-element
    data-ks-depth="400"
 :src="card.src" :alt="card.title" class="w-full h-64 object-cover rounded-2xl " />

    <!-- Неоновое свечение под курсором -->
    <div
      class="pointer-events-none absolute w-48 h-48 rounded-full bg-gradient-radial from-pink-700 via-pink-600 to-transparent blur-3xl transition duration-300 mix-blend-screen z-10"
      :style="{
        top: glowY + 'px',
        left: glowX + 'px',
        transform: 'translate(-50%, -50%)',
        opacity: glowVisible ? 1 : 0.7
      }"></div>

    <!-- Оверлей с описанием (для ховера) -->
    <div  

      class="absolute inset-0 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition duration-500 p-6 rounded-2xl z-20">
      <!-- Обертка для черного облака -->
      <div class="relative p-4 rounded-3xl text-center">
        <div class="absolute inset-0 bg-white rounded-3xl opacity-80 blur-xl"></div>
        <div           
        class="relative z-50 p-4">
          <h2
          data-kinesisdepth-element
        data-ks-depth="800"
            class="text-4xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-red-600 to-purple-500 mb-2 drop-shadow-lg">
            {{ card.title }}
          </h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

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