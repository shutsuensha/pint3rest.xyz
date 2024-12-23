<script setup>
import { initCarousels } from 'flowbite'
import { onMounted, ref } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import AOS from 'aos';
import 'aos/dist/aos.css';


const bg = ref('bg-gray-100')

const loading = ref(true)
const color = ref('red')
const size = ref('50px')

const textWelcome = ref('Welcome to Our Platform')

const images = ref([])

function changeBgColor1() {
  bg.value = 'bg-red-100'
  textWelcome.value = 'First time here? - Sign Up'
}

function changeBgColor2() {
  bg.value = 'bg-green-100'
  textWelcome.value = 'Already has an account ?'
}

function changeDefaultColor() {
  bg.value = 'bg-gray-100'
  textWelcome.value = 'Welcome to Our Platform'
}

onMounted(async () => {
  initCarousels();
  AOS.init({
    duration: 3000,  // Длительность анимации
    once: true,      // Анимация будет воспроизводиться только один раз
  });
  try {
    for (let i = 1; i <= 15; i++) {
      const response = await axios.get(`/api/index/notauth/images/${i}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(response.data);
      images.value.push(blobUrl)
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <ClipLoader v-if="loading" :color="color" :size="size"
    class="flex items-center justify-center h-screen font-extrabold" />
  <div v-else :class="`${bg} flex items-center justify-center h-screen`">
    <div class="items-center space-y-6 flex flex-col">
      <div v-if="bg === 'bg-gray-100'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(0, 5)" :key="index" class="p-2"
          :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-full h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div v-if="bg === 'bg-red-100'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(5, 10)" :key="index" class="p-2" :data-aos="index % 2 !== 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-full h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div v-if="bg === 'bg-green-100'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(10, 15)" :key="index" class="p-2" :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-full h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div class="text-center">
        <h1 class="text-3xl font-bold text-black mb-6">{{ textWelcome }}</h1>
        <div class="space-x-4">
          <!-- Signup Button -->
          <button @mouseenter="changeBgColor1" @mouseleave="changeDefaultColor"
            class="hover:-translate-y-2 px-6 py-3 bg-red-400 text-black font-semibold rounded-3xl transition hover:bg-red-600 hover:text-white">
            Sign Up
          </button>
          <!-- Login Button -->
          <button @mouseenter="changeBgColor2" @mouseleave="changeDefaultColor"
            class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            Log In
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
