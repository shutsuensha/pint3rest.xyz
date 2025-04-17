<template>
  <div class="bg-black text-white font-sans z-50">
    <nav class="fixed top-0 left-0 w-full bg-black bg-opacity-50 backdrop-blur-lg p-6 z-50">
      <div class="flex justify-center items-center max-w-5xl mx-auto">
        <a href="#hero"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#hero')">Home</a>
        <a href="#about"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#about')">About</a>
        <a href="#skills"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#skills')">Skills</a>
        <a href="#projects"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#projects')">Proejcts</a>
        <a href="#experience"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#experience')">Experience</a>
        <a href="#achievements"
          class="text-white text-xl font-bold hover:text-indigo-400 px-10 py-2 rounded-md transition-colors"
          @click.prevent="scrollTo('#achievements')">Achievements</a>
      </div>
    </nav>



    <section id="hero"
      class="min-h-screen flex flex-col items-center justify-center text-center px-6 py-20 overflow-hidden"
      data-aos="fade-up">
      <svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 1920 1080"
        class="absolute top-0 left-0 w-full h-full opacity-30 pointer-events-none z-0 animate-pulse">
        <defs>
          <linearGradient id="grad-hero" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6366F1" stop-opacity="1" />
            <stop offset="100%" stop-color="#EC4899" stop-opacity="1" />
          </linearGradient>
        </defs>
        <g stroke="url(#grad-hero)" stroke-width="3" stroke-opacity="0.5" fill="none">
          <path d="M0,600 Q480,300 960,600 T1920,600" />
          <path d="M0,700 Q480,400 960,700 T1920,700" />
        </g>
      </svg>

      <h1
        class="z-10 text-6xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-pink-500 mb-4"
        style="line-height: 1.2;">
        Daniil Kupryianchyk
      </h1>
      <h2 class="z-10 text-3xl font-semibold text-indigo-400 mb-6">
        Python Backend Developer
      </h2>
      <a href="/cv.pdf" download
        class="z-10 inline-block mt-4 px-6 py-3 border border-indigo-400 rounded-full hover:bg-indigo-600 transition">
        Download CV
      </a>
    </section>

    <section id="about" class="px-6 py-20 w-full" data-aos="fade-up">
      <h2
        class="text-5xl font-extrabold mb-10 text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">
        About Me
      </h2>
      <div class="flex flex-col md:flex-row gap-8 items-center justify-center">
        <div
          class="bg-gradient-to-r from-indigo-500 to-pink-500 p-6 rounded-2xl shadow-xl transform hover:scale-105 transition duration-300 ease-in-out max-w-3xl w-full">
          <div class="flex justify-center mb-6">
            <img src="https://i.pinimg.com/originals/fe/0a/04/fe0a0428f7b2db2154cf9ced998e9617.gif" alt="Profile"
              class="w-48 h-48 object-cover rounded-full shadow-xl border-4 border-indigo-400">
          </div>
          <p class="text-xl text-white font-semibold text-center leading-relaxed">
            Passionate backend developer specializing in scalable and efficient Python applications. I love building
            APIs, automating processes, and designing backend systems using modern tools like FastAPI, PostgreSQL,
            Docker, and Celery.
          </p>
        </div>
      </div>
    </section>

    <section id="skills"
      class="px-6 py-20 w-full bg-gradient-to-r from-indigo-700 via-purple-600 to-pink-500 text-white"
      data-aos="fade-up">
      <h2 class="text-5xl font-extrabold mb-16 text-center">
        Skills
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-left z-10">
        <!-- Backend (Main Stack) -->

        <!-- Deployment & Infrastructure (Main Stack) -->
        <div
          class="bg-black p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-transform transform hover:scale-105 border-2 border-indigo-500">
          <h3 class="text-2xl font-bold text-indigo-400 mb-4">
            🚀 Deployment <span class="text-sm bg-indigo-500 text-white px-2 py-1 rounded-full ml-2">Main Stack</span>
          </h3>
          <hr class="border-indigo-500 mb-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-7 gap-y-3">
            <div class="space-y-3">
              <div class="text-xl">🐳 Docker</div>
              <div class="text-xl">📦 Docker Compose</div>
              <div class="text-xl">🌐 Nginx</div>
              <div class="text-xl">⚙️ GitLab CI/CD</div>
            </div>
            <div class="space-y-3">
              <div class="text-xl">☁️ Google Cloud</div>
              <div class="text-xl">☁️ Yandex Cloud</div>
              <div class="text-xl">🌀 Git</div>
              <div class="text-xl">🌍 VPS</div>
              <div class="text-xl">🔒 SSL</div>
            </div>
          </div>
        </div>


        <div
          class="bg-black p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-transform transform hover:scale-105 border-2 border-indigo-500">
          <h3 class="text-2xl font-bold text-indigo-400 mb-4">
            🐍 Backend <span class="text-sm bg-indigo-500 text-white px-2 py-1 rounded-full ml-2">Main Stack</span>
          </h3>
          <hr class="border-indigo-500 mb-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-10 gap-y-3">
            <div class="space-y-3">
              <div class="text-xl">⚡ FastAPI</div>
              <div class="text-xl">🛠️ SQLAlchemy</div>
              <div class="text-xl">🏛️ Alembic</div>
              <div class="text-xl">🐍 Celery</div>
              <div class="text-xl">⏱️ Celery Beat</div>
              <div class="text-xl">🔑 Jwt</div>
              <div class="text-xl">🌐 Httpx</div>
            </div>
            <div class="space-y-3">
              <div class="text-xl">📜 Pydantic</div>
              <div class="text-xl">🧪 Pytest</div>
              <div class="text-xl">🌀 AsyncIO</div>
              <div class="text-xl">🦊 Ruff</div>
              <div class="text-xl">🔗 WebSockets</div>
              <div class="text-xl">🌀 Redis Streams</div>
              <div class="text-xl">🍓 Strawberry</div>
            </div>
          </div>
        </div>

        <!-- Databases (Main Stack) -->
        <div
          class="bg-black p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-transform transform hover:scale-105 border-2 border-indigo-500">
          <h3 class="text-2xl font-bold text-indigo-400 mb-4">🗄️ Databases <span
              class="text-sm bg-indigo-500 text-white px-2 py-1 rounded-full ml-2">Main Stack</span></h3>
          <hr class="border-indigo-500 mb-4">
          <ul class="space-y-3">
            <li class="text-xl">🐘 PostgreSQL</li>
            <li class="text-xl">💾 MySQL</li>
            <li class="text-xl">🔴 Redis</li>
            <li class="text-xl">🍃 MongoDB</li>
          </ul>
        </div>

        <!-- Frontend -->
        <div class="bg-black p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-transform transform hover:scale-105">
          <h3 class="text-2xl font-bold text-indigo-400 mb-4">🎨 Frontend</h3>
          <hr class="border-indigo-400 mb-4">
          <ul class="space-y-3">
            <li class="text-xl">🌐 Vue.js</li>
            <li class="text-xl">🛣️ Vue Router</li>
            <li class="text-xl">💨 Tailwind CSS</li>
            <li class="text-xl">📦 Pinia</li>
            <li class="text-xl">📡 Axios</li>
          </ul>
        </div>

        <!-- Other Experience -->
        <div class="bg-black p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-transform transform hover:scale-105">
          <h3 class="text-2xl font-bold text-indigo-400 mb-4">🛠️ Other Experience</h3>
          <hr class="border-indigo-400 mb-4">
          <ul class="space-y-3">
            <li class="text-xl">🎭 Django</li>
            <li class="text-xl">🔗 Django REST Framework</li>
            <li class="text-xl">🍶 Flask</li>
            <li class="text-xl">⚙️ GitHub CI/CD</li>
            <li class="text-xl">🌍 Aiohttp</li>
            <li class="text-xl">🤖 Aiogram</li>
          </ul>
        </div>
      </div>
    </section>




    <section id="projects" class="px-0 py-20 bg-black min-h-screen" data-aos="fade-up">
      <h2
        class="text-5xl font-extrabold mb-10 text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">
        Projects
      </h2>

      <Swiper :modules="[Navigation]" :slides-per-view="1" :loop="true" :navigation="true"
        class="max-w-full mx-auto custom-swiper">
        <SwiperSlide v-for="(project, index) in projects" :key="index"
          class="bg-gray-900 p-8 rounded-xl shadow-xl hover:shadow-indigo-500/50 transition cursor-grab active:cursor-grabbing">

          <!-- Image Slider -->
          <img :src="project.image" alt="Project Image" class="w-full h-screen object-cover rounded-lg">

          <div class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black via-transparent to-transparent">
            <h3 class="text-2xl font-bold mb-3 text-indigo-400">{{ project.title }}</h3>
            <p class="text-lg text-white mb-4">{{ project.description }}</p>

            <!-- Технологии -->
            <div class="flex flex-wrap gap-2 mb-6">
              <span v-for="tech in project.stack" :key="tech"
                class="px-3 py-1 text-sm font-medium bg-indigo-500/10 text-indigo-300 rounded-full">
                {{ tech }}
              </span>
            </div>

            <div class="flex flex-col sm:flex-row sm:items-center gap-4">
              <a :href="project.link" target="_blank" class="text-indigo-400 text-xl hover:underline">
                View on GitHub →
              </a>
              <a v-if="project.demo" :href="project.demo" target="_blank" class="text-pink-400 text-xl hover:underline">
                Live Demo →
              </a>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </section>



    <section id="experience" class="px-6 py-20 max-w-5xl mx-auto" data-aos="fade-right">
      <h2
        class="text-5xl font-extrabold mb-6 text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">
        Experience
      </h2>
      <div class="border-l-2 border-indigo-500 pl-6">
        <div class="mb-10 border-pink-500 pl-6 border-l-2">
          <h3 class="text-xl font-semibold">Full-Stack Developer – Pinterest Clone</h3>
          <span class="text-sm text-gray-400">Dec 2024 – Apr 2025 (4 months)</span>
          <p class="text-gray-300 mt-2">
            Developed a Pinterest-like platform with a Vue 3 frontend and FastAPI backend, using PostgreSQL
            (SQLAlchemy, Alembic), MongoDB, and MySQL for databases. Integrated real-time chat wuth websockets, dynamic
            updates with sse, recommendations,
            notifications, tag-based search, authentication using JWT and cookies, many-to-mant complex relationships in
            the database. Utilized Celery for background tasks and Redis Streams for service
            communication. Employed FastAPI Mail and Cache for optimized email workflows and performance. Configured
            GraphQL (Strawberry) for flexible API interactions. Ensured code quality with Ruff, wrote tests with Pytest
            and httpx, and set up GitLab CI/CD for automation. Deployed to a VPS with Nginx and SSL, and integrated
            Yandex S3 for media storage.
          </p>
          <br />
          <div class="flex flex-row items-center gap-4 ">
            <a href="https://github.com/shutsuensha/pinterest-clone-vue3-fastapi" target="_blank"
              class="text-indigo-400  hover:underline">
              View on GitHub →
            </a>
            <br />
            <a href="https://pint3rest.xyz" target="_blank" class="text-pink-400 hover:underline">
              Live Demo →
            </a>
          </div>
        </div>

        <div class="border-pink-500 pl-6 border-l-2">
          <h3 class="text-xl font-semibold">Backend Developer – Krossovki By (TeachMeSkills Diploma Project)</h3>
          <span class="text-sm text-gray-400">Mar 2025 – Apr 2025 (1 month)</span>
          <p class="text-gray-300 mt-2">
            Created an e-commerce backend with Django. Implemented product filtering, order
            management,
            Telegram bot notifications, and custom admin tools. Integrated Google One Tap and social auth for
            streamlined user onboarding.
            Used PostgreSQL for relational data.
          </p>
          <br />
          <div>
            <a href="https://github.com/shutsuensha/online-store" target="_blank"
              class="text-indigo-400 hover:underline">
              View on GitHub →
            </a>
          </div>
        </div>
      </div>
    </section>


    <section id="achievements" class="px-6 py-20" data-aos="fade-up">
      <h2
        class="text-5xl font-extrabold mb-10 text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">
        Achievements
      </h2>

      <!-- Certificates with multiple images in a row -->
      <div class="flex flex-col  p-6 rounded-xl shadow hover:shadow-indigo-500/50 transition">
        <!-- Certificates Section -->
        <div class="flex flex-row gap-6">
          <!-- Certificate 1 -->
          <div class="flex-1">
            <img
              src="https://raw.githubusercontent.com/shutsuensha/shutsuensha/refs/heads/main/FastAPI-ArtemShumeiko-1.png"
              alt="Certificate 1" class="w-full rounded-lg shadow-md hover:shadow-lg transition-all">
          </div>

          <!-- Certificate 2 -->
          <div class="flex-1">
            <img
              src="https://raw.githubusercontent.com/shutsuensha/shutsuensha/refs/heads/main/FastAPI-ArtemShumeiko-2.png"
              alt="Certificate 2" class="w-full rounded-lg shadow-md hover:shadow-lg transition-all">
          </div>
        </div>
      </div>

      <!-- Certificate with a single image -->
      <div class="p-6 rounded-xl shadow hover:shadow-indigo-500/50 transition mt-8 text-center">

        <!-- Certificate Image -->
        <img src="https://raw.githubusercontent.com/shutsuensha/shutsuensha/refs/heads/main/TMS-1.png"
          alt="TeachMeSkills Certificate" class="w-full rounded-lg shadow-md hover:shadow-lg transition-all">
      </div>
    </section>

    <div id="contacts"
      class="px-6 py-20 w-full bg-black text-white flex flex-col items-center justify-center space-y-10">
      <div class="flex justify-center space-x-6">
        <!-- GitHub -->
        <a href="https://github.com/shutsuensha" target="_blank"
          class="z-10 inline-block mt-4 px-6 py-3 border border-indigo-400 rounded-full hover:bg-indigo-600 transition">
          GitHub
        </a>

        <!-- Telegram -->
        <a href="https://www.linkedin.com/in/daniil-kupryianchyk-960594322" target="_blank"
          class="z-10 inline-block mt-4 px-6 py-3 border border-indigo-400 rounded-full hover:bg-indigo-600 transition">
          LinkedIn
        </a>

        <!-- LinkedIn -->
        <a href="https://t.me/evalshine" target="_blank"
          class="z-10 inline-block mt-4 px-6 py-3 border border-indigo-400 rounded-full hover:bg-indigo-600 transition">
          Telegram
        </a>

        <!-- Email -->
        <a href="mailto:dankupr21@gmail.com" target="_blank"
          class="z-10 inline-block mt-4 px-6 py-3 border border-indigo-400 rounded-full hover:bg-indigo-600 transition">
          Gmail
        </a>
      </div>
    </div>


  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import AOS from 'aos'
import 'aos/dist/aos.css'


import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import { Pagination, Navigation } from 'swiper/modules';

// import { Pagination } from 'swiper/modules'

onMounted(() => {
  document.title = "Resume - Daniil Kupryianchyk"
  AOS.init({ once: false, duration: 2000 })
})

const projects = ref([
  {
    title: 'Pinterest Clone',
    description: 'Full-featured FastAPI backend and Vue3 frontend with real-time chat, real-time updates, media uploads, boards, pins, comments, likes, recommendations and more.',
    link: 'https://github.com/shutsuensha/pinterest-clone-vue3-fastapi',
    image: 'https://raw.githubusercontent.com/shutsuensha/pinterest-clone-vue3-fastapi/refs/heads/main/.github/assets/feed.png',
    stack: [
      'FastAPI', 'FastAPI-Cache', 'FastAPI-Mail', 'SQLAlchemy', 'Pydantic', 'pydantic-settings', 'JWT',
      'OAuth2', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Celery', 'Celery Beat', 'Docker',
      'Docker Compose', 'Nginx', 'SSL', 'VPS', 'Yandex S3', 'httpx', 'Websockets', 'SSE',
      'Asyncio', 'Aiofiles', 'Logging', 'Pytest', 'Ruff', 'Alembic', 'GitLab CI/CD',
      'GraphQL (Strawberry)', 'Redis Stream', 'Vue 3', 'Vue Router', 'Tailwind CSS', 'Pinia', 'Axios'
    ],
    demo: 'https://pint3rest.xyz'
  },
  {
    title: 'Krossovki By - Diploma project from TeachMeSkills',
    description: 'Django e-commerce backend, user auth, order tracking, and admin dashboard.',
    link: 'https://github.com/shutsuensha/online-store',
    image: 'https://raw.githubusercontent.com/shutsuensha/online-store/refs/heads/main/assets/screenshots/logo.png',
    stack: ['Django', 'PostgreSQL', 'Tailwind CSS'],
    demo: null, // нет live demo
  }
])

function scrollTo(selector) {
  const target = document.querySelector(selector)
  if (!target) return

  const offset = 80 // если у тебя фиксированное меню
  const targetPosition = target.offsetTop - offset
  const startPosition = window.pageYOffset
  const distance = targetPosition - startPosition
  const duration = 1000 // время анимации в миллисекундах
  let startTime = null

  function animation(currentTime) {
    if (startTime === null) startTime = currentTime
    const timeElapsed = currentTime - startTime
    const run = ease(timeElapsed, startPosition, distance, duration)
    window.scrollTo(0, run)
    if (timeElapsed < duration) {
      requestAnimationFrame(animation)
    }
  }

  // Эasing функция для плавности (с задержкой в начале и конце)
  function ease(t, b, c, d) {
    const ts = (t /= d) * t
    const tc = ts * t
    return b + c * (tc + -3 * ts + 3 * t)
  }

  requestAnimationFrame(animation)
}

</script>

<style scoped>
section {
  min-height: 100vh;
  padding-top: 100px;
}



body {
  font-family: 'Segoe UI', sans-serif;
}

.animate-pulse {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {

  0%,
  100% {
    opacity: 0.3;
  }

  50% {
    opacity: 1;
  }
}

.custom-swiper .swiper-pagination-bullet {
  background-color: #818cf8 !important;
  /* Tailwind indigo-400 */
  opacity: 1 !important;
}

.custom-swiper .swiper-pagination-bullet-active {
  background-color: #c084fc !important;
  /* Tailwind fuchsia-400 */
}
</style>

<style>
.swiper-button-next,
.swiper-button-prev {
  background-color: rgba(0, 0, 0, 0.5);
  /* Добавить полупрозрачный фон */
  border-radius: 50%;
  width: 100px;
  height: 100px;
  top: 50%;
  /* Центрирование по вертикали */
  transform: translateY(-50%);
  z-index: 10;
}

.swiper-button-next {
  right: 50px;
  /* Отступ от правого края */
}

.swiper-button-prev {
  left: 50px;
  /* Отступ от левого края */
}

/* Стиль для стрелочек (увеличение) */
.swiper-button-next:after,
.swiper-button-prev:after {
  font-size: 2rem;
  color: white;
}

/* Контейнер для описания проекта */
.swiper-slide {
  position: relative;
}

.swiper-slide .absolute {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.85) 80%, rgba(0, 0, 0, 0) 100%);
}
</style>