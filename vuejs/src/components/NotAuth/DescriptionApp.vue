<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-100 via-black to-white text-gray-900 relative">
    <img src="/screen.jpg" class="absolute top-0 right-0 h-[800px] opacity-40 mask-gradient" />
    <div class=" max-w-7xl mx-auto px-6 py-12 z-50">
      <!-- Заголовок с динамическим градиентом -->
      <div v-if="fontLoaded">
        <h1 class="z-50 text-6xl font-semibold text-center mb-10 cursor-default text-black   font-poppins">
          HАШ Слава Богу 🙏❤️СЛАВА РОССИИ 🙏❤️АНГЕЛА ХРАНИТЕЛЯ КАЖДОМУ ИЗ ВАС 🙏❤️БОЖЕ ХРАНИ РОССИЮ 🙏❤️СПАСИБО ВАМ НАШИ МАЛЬЧИКИ 🙏🏼❤️🇷🇺 ЧТО ПОДДЕРЖИМ НАШИХ СРАЗУ видно НАШ СЛОНЯРА🇷🇺🇷🇺💪 СВО слава тебе Господи🇷🇺🇷🇺🇷🇺💪🔥🔥 СВО да хранит ТЕБЯ ГОСПОДЬ🔥💪💪🇷🇺 НАШ живчик СРАЗУ видно НАШИХ парней издалека🇷🇺🇷🇺🇷🇺🇷🇺💪💪💪💪💪 СВОих не бросаем🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺💪💪Слава Богу СВО🙏❤️СЛАВА СВО🙏❤️АНГЕЛА ХРАНИТЕЛЯ СВО КАЖДОМУ ИЗ ВАС🙏❤️БОЖЕ ХРАНИ СВО🙏❤️СПАСИБО ВАМ НАШИ СВО🙏🏼❤️🇷🇺 ХРОНИ СВО✊🇷🇺💯СПАСИБО ВАМ НАШИ МАЛЬЧИКИ 🙏🏼❤️🇷🇺 ЧТО ПОДДЕРЖИВАЕТЕ СВО
        </h1>
        <h1
          class="z-50 text-6xl font-semibold text-center mb-10 cursor-default bg-gradient-to-r from-indigo-600 to-red-700 text-transparent bg-clip-text font-poppins">
          Pinterest Clone
        </h1>
        <h2
          class="z-50 text-4xl font-semibold text-center mb-2 cursor-default bg-gradient-to-r from-purple-600 to-red-700 text-transparent bg-clip-text font-poppins">
          1536 × 864 / Vue 3 & FastAPI
        </h2>
      </div>

      <div class="grid grid-cols-1 gap-4 h-[600px]">
        <Overview :card="overview" />
      </div>

      <!-- Первая галерея -->
      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(0, 2)" :key="index" :card="card"
          @click="openFullscreen(index)" />
      </div>

      <!-- Текстовый блок -->
      <!-- <div class="cursor-default mb-12 text-center px-4 py-6 bg-white/70 backdrop-blur-md rounded-lg shadow-lg"
        data-kinesisscroll-item data-ks-strength="30" data-ks-transformaxis="Y">
        <h2 class="text-4xl font-bold ">👤 Users 📌 Pins ❤️ Likes 💬 Comments 💭 Chats </h2>
      </div> -->

      <!-- Вторая галерея -->
      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(2, 4)" :key="index" :card="card"
          @click="openFullscreen(index + 2)" />
      </div>

      <!-- Текстовый блок -->
      <!-- <div class="cursor-default mb-12 text-center px-4 py-6 bg-white/70 backdrop-blur-md rounded-lg shadow-lg"
        data-kinesisscroll-item data-ks-strength="30" data-ks-transformaxis="Y">
        <h2 class="text-4xl font-bold">Easy registration with no hassle! 🚀 Give it a try now! 😊</h2>
      </div> -->

      <!-- Третья галерея -->
      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(4, 6)" :key="index" :card="card"
          @click="openFullscreen(index + 4)" />
      </div>

      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(6, 8)" :key="index" :card="card"
          @click="openFullscreen(index + 6)" />
      </div>


      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(8, 10)" :key="index" :card="card"
          @click="openFullscreen(index + 8)" />
      </div>

      <div class="grid grid-cols-2 gap-4" data-kinesisscroll-item data-ks-strength="-50" data-ks-transformaxis="Y">
        <ScreenshotCard v-for="(card, index) in screenshots.slice(10, 12)" :key="index" :card="card"
          @click="openFullscreen(index + 10)" />
      </div>

        <div class="cursor-default mb-12 text-center px-4 py-6 bg-white/70 backdrop-blur-md rounded-lg shadow-lg"
        data-kinesisscroll-item data-ks-strength="30" data-ks-transformaxis="Y">
        <h2 class="text-4xl font-bold">No commitments — just have a good time</h2>
      </div>

    </div>

    <!-- Полноэкранное модальное окно -->
    <transition name="fade">
      <div @click="closeFullscreen" v-if="fullscreenIndex !== null"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
        <div class="relative flex items-center justify-center max-w-full w-full">
          <!-- Стрелка слева -->
          <button @click.stop="closeFullscreen"
            class="absolute top-4 right-4 px-3 py-3 rounded-full bg-white/20 text-white text-3xl hover:bg-gray-100 hover:text-black transition z-50 flex items-center justify-center">
            <i class="pi pi-times"></i>
          </button>

          <button @click.stop="prevImage"
            class="py-5 px-6 rounded-full text-white text-5xl hover:bg-gray-100 hover:text-black transition mr-4 z-20 flex items-center justify-center aspect-square">
            <i class="pi pi-arrow-left"></i>
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
            class="py-5 px-6 rounded-full text-white text-5xl hover:bg-gray-100 hover:text-black transition ml-4 z-20 flex items-center justify-center aspect-square">
            <i class="pi pi-arrow-right"></i>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import ScreenshotCard from '@/components/NotAuth/ScreenshotCard.vue'
import { initializeKinesis } from "@amineyarman/kinesis";
import Overview from '@/components/NotAuth/Overview.vue'

const fontLoaded = ref(false)


onMounted(async () => {
  try {
    // Ждём загрузки шрифта
    await document.fonts.load('1rem "Poppins"')
    fontLoaded.value = true
  } catch (err) {
    console.error('Poppins failed to load:', err)
  }
  initializeKinesis();
});

const overview = ref(
  {
    src: '/screenshots/overview.png',
    stream: 'overview.mp4',
    title: 'Overview',
  })


const screenshots = ref([
  {
    src: '/screenshots/feed.png',
    stream: 'feed.mp4',
    title: '🌸 Feed',
    description: 'The feed is the main page featuring search and tags, displaying pins in the form of gifs, videos, and images. It shows users who have posted these pins. The layout follows a masonry grid design with infinite scrolling.'
  },
  {
    src: '/screenshots/detail.png',
    stream: 'detail.mp4',
    title: '📌 Pin + Related',
    description: 'A detailed pin with title, description, href, tags, and the user who created it. Includes comments and likes. Below the pin, related pins are displayed based on connected tags.'
  },
  {
    src: '/screenshots/search.png',
    stream: 'search.mp4',
    title: '🔍 Search',
    description: 'Pin search by query and tags, with a quick search feature available on any page. It also displays popular pins and a list of recent searches.'
  },
  {
    src: '/screenshots/create.png',
    stream: 'create.mp4',
    title: '✨ New Pin',
    description: 'Pin creation — image/gif/video, with the option to add additional information to the pin and assign tags to it.'
  },
  {
    src: '/screenshots/user.png',
    stream: 'user.mp4',
    title: '👤 User Profile',
    description: 'User profile — profile editing by the owner, creation of boards, viewing/editing created/liked/saved pins, viewing/editing pins on boards. Users can also follow/unfollow and message other users.'
  },
  {
    src: '/screenshots/followers.png',
    stream: 'followers.mp4',
    title: '👥 Followers/Following',
    description: 'View followers/following for any user.'
  },
  {
    src: '/screenshots/boards.png',
    stream: 'boards.mp4',
    title: '🧷 Boards',
    description: 'Users create boards and add/remove pins on them'
  },
  {
    src: '/screenshots/recomendations.png',
    stream: 'recomendations.mp4',
    title: '⭐ Recommendations',
    description: 'Users receive real-time recommendations based on their recently viewed pins.'
  },
  {
    src: '/screenshots/updates.png',
    stream: 'realtimeUpdates.mp4',
    title: '🔔 Realtime Updates',
    description: 'Users receive real-time updates from others when their pins are saved, commented on, or liked.'
  },
  {
    src: '/screenshots/cahts.png',
    stream: 'chats.mp4',
    title: '💬 Chats',
    description: 'By messaging another user, you create a chat where you can exchange messages and media in real time. Chats can be customized in terms of size and color. You can also see which users are online on the site or in the chat.'
  },
  {
    src: '/screenshots/chats_updates.png',
    stream: 'chats_updates.mp4',
    title: '💬🔔 Chats Updates',
    description: 'On any page, you receive real-time updates about new messages from other users.'
  },
  {
    src: '/screenshots/comments_likes.png',
    stream: 'comments_likes.mp4',
    title: '📝❤️ Comments/Likes',
    description: 'You can comment on, like, and save a pin, as well as comment on and like other comments.'
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


<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.font-poppins {
  font-family: 'Poppins', sans-serif;
}
</style>