<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-100 via-purple-200 to-white text-gray-900 relative">
    <div class="max-w-7xl mx-auto px-6 py-12">
      <!-- Заголовок с динамическим градиентом -->


      <div data-kinesistransformer>
        <h1 class="text-6xl font-extrabold text-center mb-10 cursor-default" @mousemove="updateHeaderGradient"
          data-kinesistransformer-element data-ks-transform="translate" @mouseleave="resetHeaderGradient"
          :style="headerStyle">
          🚀 Pint3rest Next-Gen
        </h1>
      </div>


      <!-- Галерея -->
      <div class="grid grid-cols-2 ">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(0, 2)" :key="index" :card="card"
          @click="openFullscreen(index)" />
      </div>

      <div class="overflow-hidden relative">
        <!-- Первая строка -->
        <div class="marquee-wrapper animate-marquee">
          <span class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-700 to-red-800">
            Vuejs3,
            Tailwind CSS,
            Pinia,
            Vue Router,
            Vue Masonry,
            Vue Keep Alive,
            Vue Spinner, JsConfetti, DaysJs, Aos, Auto-animate, Kenesis
          </span>
        </div>
      </div>

      <div class="grid grid-cols-2">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(2, 4)" :key="index" :card="card"
          @click="openFullscreen(index + 2)" />
      </div>

      <div class="overflow-hidden relative">
        <div class="marquee-wrapper2 animate-marquee">
          <span class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-700 to-indigo-800">
            FastAPI, Postgresql, Redis, Asyncio, Jwt, Mail, Celery, Httpx, Yandex S3, Google Auth, Mysql, Mongodb,
            GraphQL, Pydantic, Sqlalchemy, Logging, Docker, Docker-compose, Gitlab ci/cd, Pytests, Ruff, Nginx, Ssl/Vps
          </span>
        </div>
      </div>

      <div class="grid grid-cols-2">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(4, 6)" :key="index" :card="card"
          @click="openFullscreen(index + 4)" />
      </div>

    </div>

    <!-- Полноэкранное модальное окно -->
    <transition name="fade">
      <div @click="closeFullscreen" v-if="fullscreenIndex !== null"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
        <div class="relative flex items-center justify-center max-w-full w-full">
          <!-- Стрелка слева -->
          <button @click.stop="prevImage"
            class="p-4 rounded-full text-white text-6xl hover:bg-gray-100 hover:text-black transition mr-4 z-20 items-center justify-center">
            &larr;
          </button>
          <!-- Контент модального окна -->
          <div class="relative max-w-6xl w-full p-6 rounded-xl" @click.stop>
            <img :src="currentCard.src" alt="" class="w-full h-auto rounded-lg shadow-2xl mb-4 object-cover"
              @click.stop />
            <h2 class="text-5xl font-bold text-white mb-2">{{ currentCard.title }}</h2>
            <p class="text-2xl text-gray-200">{{ currentCard.description }}</p>
          </div>
          <!-- Стрелка справа -->
          <button @click.stop="nextImage"
            class="p-4 rounded-full text-white text-6xl hover:bg-gray-100 hover:text-black transition ml-4 z-20">
            &rarr;
          </button>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ScreenshotCard from '@/components/NotAuth/ScreenshotCard.vue'
import { initializeKinesis } from "@amineyarman/kinesis";

onMounted(() => {
  initializeKinesis();
});

const screenshots = ref([
  { src: '/screenshots/home.png', title: '🏠 Главная', description: 'Стильный фид для вдохновения.', video: "/screenshots/home.mp4" },
  { src: '/screenshots/search.png', title: '🔍 Поиск', description: 'Находите лучшие идеи.', video: "/screenshots/search.mp4"},
  { src: '/screenshots/user.png', title: '👤 Профиль', description: 'Ваш личный космический кабинет.', video: "/screenshots/user.mp4" },
  { src: '/screenshots/pin-detail.png', title: '📌 Пин', description: 'Подробности, лайки, сохранения.', video: "/screenshots/pin-detail.mp4" },
  { src: '/screenshots/create-pin.png', title: '✨ Новый Пин', description: 'Создавайте шедевры за секунды.', video: "/screenshots/pin-create.mp4" },
  { src: '/screenshots/chats.png', title: '💬 Чаты', description: 'Мгновенное общение без границ.', video: "/screenshots/chats.mp4" },
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

<style scoped>
.marquee-wrapper {
  display: inline-block;
  /* Элементы в одном ряду */
  animation: marquee 40s linear infinite;
  font-size: 5rem;
  /* Увеличиваем размер шрифта */
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  /* Прокрутка в одном ряду */
  overflow: hidden;
}

.marquee-wrapper2 {
  display: inline-block;
  /* Элементы в одном ряду */
  animation: marquee2 40s linear infinite;
  font-size: 5rem;
  /* Увеличиваем размер шрифта */
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  /* Прокрутка в одном ряду */
  overflow: hidden;
}


.animate-marquee {
  font-size: 5rem;
  /* Увеличиваем размер шрифта для анимации */
}

@keyframes marquee {
  0% {
    transform: translateX(20%);
    /* Начало прокрутки с правого края */
  }

  100% {
    transform: translateX(-100%);
    /* Конец прокрутки слева */
  }
}

@keyframes marquee2 {
  0% {
    transform: translateX(-100%);
    /* Начало прокрутки с правого края */
  }

  100% {
    transform: translateX(0%);
    /* Конец прокрутки слева */
  }
}

.bg-clip-text {
  background-clip: text;
  color: transparent;
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, #f0f, rgb(233, 52, 11));
}

.relative {
  position: relative;
}

@keyframes cloudAnimation {
  0% {
    left: -100%;
    right: -100%;
  }

  100% {
    left: 100%;
    right: 100%;
  }
}
</style>
