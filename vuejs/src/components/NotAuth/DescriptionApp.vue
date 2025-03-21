<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-100 via-black to-white text-gray-900 relative">
    <img src="/screen.jpg" class="absolute top-0 right-0 h-full opacity-40 mask-gradient" />
    <div class=" max-w-7xl mx-auto px-6 py-12 z-50">
      <!-- Заголовок с динамическим градиентом -->
      <div>
        <h1
          class="z-50 text-6xl font-extrabold text-center mb-10 cursor-default bg-gradient-to-r from-black to-black text-transparent bg-clip-text">
          Pint3rest Next-Gen
        </h1>
        <h2
          class="z-50 text-4xl font-extrabold text-center mb-10 cursor-default bg-gradient-to-r from-black to-black text-transparent bg-clip-text">
          your fun space to share art & ideas!
        </h2>
      </div>


      <!-- Первая галерея -->
      <div class="grid grid-cols-2" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(0, 2)" :key="index" :card="card"
          @click="openFullscreen(index)" />
      </div>

      <!-- Текстовый блок -->
      <div class="cursor-default mb-12 text-center px-4 py-6 bg-white/70 backdrop-blur-md rounded-lg shadow-lg"
        data-kinesisscroll-item data-ks-strength="30" data-ks-transformaxis="Y">
        <h2 class="text-4xl font-bold mb-4">👤 Users 📌 Pins ❤️ Likes 💬 Comments</h2>
      </div>

      <!-- Вторая галерея -->
      <div class="grid grid-cols-2" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(2, 4)" :key="index" :card="card"
          @click="openFullscreen(index + 2)" />
      </div>

      <!-- Текстовый блок -->
      <div class="cursor-default mb-12 text-center px-4 py-6 bg-white/70 backdrop-blur-md rounded-lg shadow-lg"
        data-kinesisscroll-item data-ks-strength="30" data-ks-transformaxis="Y">
        <h2 class="text-4xl font-bold mb-4">💡 Fast, cool, and creative! 😎✨</h2>
      </div>

      <!-- Третья галерея -->
      <div class="grid grid-cols-2" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
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
          <button @click.stop="closeFullscreen"
            class="absolute top-4 right-4 px-5 py-2 rounded-full bg-white/20 text-white text-3xl hover:bg-gray-100 hover:text-black transition z-50">
            ✕
          </button>

          <button @click.stop="prevImage"
            class="p-4 rounded-full text-white text-6xl hover:bg-gray-100 hover:text-black transition mr-4 z-20 flex items-center justify-center aspect-square">
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


onMounted(async () => {
  initializeKinesis();
});

const screenshots = ref([
  {
    src: '/screenshots/pint3rest-home.png',
    stream: 'home.mp4',
    title: '🏠 Home',
    description: 'A stylish feed designed to spark creativity and inspiration. Explore a curated collection of visually stunning content that fuels your imagination.'
  },
  {
    src: '/screenshots/pint3rest-search.png',
    stream: 'search.mp4',
    title: '🔍 Search',
    description: 'Discover trending ideas and the latest content with our advanced search tools. Quickly find inspiration and innovative concepts.'
  },
  {
    src: '/screenshots/pint3rest-user.png',
    stream: 'profile.mp4',
    title: '👤 Profile',
    description: 'Your personalized profile where your creativity shines. Showcase your interests, connect with others, and manage your content effortlessly.'
  },
  {
    src: '/screenshots/pint3rest-detail.png',
    stream: 'detail.mp4',
    title: '📌 Pin',
    description: 'Dive into detailed insights on every pin, including likes, comments, and saves. Gain a deeper understanding of what makes each pin unique.'
  },
  {
    src: '/screenshots/pint3rest-create.png',
    stream: 'create.mp4',
    title: '✨ New Pin',
    description: 'Easily create and share stunning pins with our intuitive interface. Turn your ideas into captivating visuals in seconds.'
  },
  {
    src: '/screenshots/pint3rest-chats.png',
    stream: 'chats.mp4',
    title: '💬 Chats',
    description: 'Engage in real-time, limitless conversations with fellow creatives. Share ideas, feedback, and inspiration instantly.'
  },
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
  animation: marquee 40s linear infinite;
  font-size: 5rem;
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  overflow: hidden;
}

.marquee-wrapper2 {
  display: inline-block;
  animation: marquee2 40s linear infinite;
  font-size: 5rem;
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  overflow: hidden;
}

.animate-marquee {
  font-size: 5rem;
}

@keyframes marquee {
  0% {
    transform: translateX(20%);
  }

  100% {
    transform: translateX(-100%);
  }
}

@keyframes marquee2 {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(0%);
  }
}

.bg-clip-text {
  background-clip: text;
  color: transparent;
}

/* .bg-gradient-to-r {
  background-image: linear-gradient(to right, #f0f, rgb(233, 52, 11));
} */

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

.mask-gradient {
  -webkit-mask-image: linear-gradient(to bottom, white, transparent),
    linear-gradient(to left, white, transparent);
  mask-image: linear-gradient(to bottom, white, transparent),
    linear-gradient(to left, white, transparent);
  -webkit-mask-composite: multiply;
  mask-composite: intersect;
}
</style>
