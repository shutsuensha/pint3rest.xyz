<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 text-gray-900">
    <div class="max-w-7xl mx-auto px-6 py-12">
      <!-- Заголовок с динамическим градиентом -->
      <h1 
        class="text-6xl font-extrabold text-center mb-10 cursor-default" 
        @mousemove="updateHeaderGradient"
        @mouseleave="resetHeaderGradient"
        :style="headerStyle"
      >
        🚀 Pint3rest Next-Gen
      </h1>
      <p class="text-xl text-center text-gray-700 mb-14">
        Добро пожаловать в будущее. Стиль, скорость, инновации.
      </p>

      <!-- Галерея -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10">
        <ScreenshotCard
          v-for="(card, index) in screenshots"
          :key="index"
          :card="card"
          @click="openFullscreen(index)"
        />
      </div>
    </div>

    <!-- Полноэкранное модальное окно -->
    <transition name="fade">
      <div v-if="fullscreenIndex !== null" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
        <div class="relative flex items-center justify-center max-w-full w-full">
          <!-- Стрелка слева -->
          <button @click="prevImage" class="p-4 bg-black/70 rounded-full text-white text-4xl hover:text-gray-300 transition mr-4 z-20">
            &larr;
          </button>
          <!-- Контент модального окна -->
          <div class="relative max-w-4xl w-full p-6 bg-gray-900/80 rounded-xl">
            <button @click="closeFullscreen" class="absolute top-4 right-4 z-20 p-2 bg-black/70 rounded-full text-white text-3xl hover:text-gray-300 transition">
              &times;
            </button>
            <img :src="currentCard.src" alt="" class="w-full h-auto rounded-lg shadow-2xl mb-4 object-cover" />
            <h2 class="text-3xl font-bold text-white mb-2">{{ currentCard.title }}</h2>
            <p class="text-xl text-gray-200">{{ currentCard.description }}</p>
          </div>
          <!-- Стрелка справа -->
          <button @click="nextImage" class="p-4 bg-black/70 rounded-full text-white text-4xl hover:text-gray-300 transition ml-4 z-20">
            &rarr;
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ScreenshotCard from '@/components/NotAuth/ScreenshotCard.vue'

const screenshots = ref([
  { src: '/screenshots/home.png', title: '🏠 Главная', description: 'Стильный фид для вдохновения.' },
  { src: '/screenshots/search.png', title: '🔍 Поиск', description: 'Находите лучшие идеи.' },
  { src: '/screenshots/user.png', title: '👤 Профиль', description: 'Ваш личный космический кабинет.' },
  { src: '/screenshots/pin-detail.png', title: '📌 Пин', description: 'Подробности, лайки, сохранения.' },
  { src: '/screenshots/create-pin.png', title: '✨ Новый Пин', description: 'Создавайте шедевры за секунды.' },
  { src: '/screenshots/chats.png', title: '💬 Чаты', description: 'Мгновенное общение без границ.' },
])

const fullscreenIndex = ref(null)
const openFullscreen = (index) => {
  fullscreenIndex.value = index
}
const closeFullscreen = () => {
  fullscreenIndex.value = null
}
const prevImage = () => {
  if (fullscreenIndex.value !== null) {
    fullscreenIndex.value = (fullscreenIndex.value - 1 + screenshots.value.length) % screenshots.value.length
  }
}
const nextImage = () => {
  if (fullscreenIndex.value !== null) {
    fullscreenIndex.value = (fullscreenIndex.value + 1) % screenshots.value.length
  }
}
const currentCard = computed(() => {
  return fullscreenIndex.value !== null ? screenshots.value[fullscreenIndex.value] : {}
})

// Динамический градиент для заголовка
const headerStyle = ref({
  backgroundImage: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
  WebkitBackgroundClip: 'text',
  color: 'transparent'
})

const updateHeaderGradient = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  const relX = x / rect.width;
  const relY = y / rect.height;
  const hue1 = Math.floor(relX * 360);
  const hue2 = Math.floor(relY * 360);
  headerStyle.value = {
    backgroundImage: `linear-gradient(135deg, hsl(${hue1}, 90%, 50%), hsl(${hue2}, 90%, 50%))`,
    WebkitBackgroundClip: 'text',
    color: 'transparent'
  }
}

const resetHeaderGradient = () => {
  headerStyle.value = {
    backgroundImage: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
    WebkitBackgroundClip: 'text',
    color: 'transparent'
  }
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
