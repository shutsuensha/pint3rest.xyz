<script setup>
import { onMounted, ref } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import AOS from 'aos';
import 'aos/dist/aos.css';


const bg = ref('bg-gray-100')

const loading = ref(true)
const color = ref('red')
const size = ref('50px')

const textWelcome = ref('Welcome to Our Platform 🩸')

const images = ref([])

const showSignUp = ref(false)

const imagePreview = ref(null)


function changeBgColor1() {
  bg.value = 'bg-red-100'
  textWelcome.value = 'First time here ? - Sign Up 😇'
}

function changeBgColor2() {
  bg.value = 'bg-green-100'
  textWelcome.value = 'Already have an account ? 🤫'
}

function changeDefaultColor() {
  bg.value = 'bg-gray-100'
  textWelcome.value = 'Welcome to Our Platform 🩸'
}

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result; // Update the preview data
    };
    reader.readAsDataURL(file);
  }
}

onMounted(async () => {
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
  <div v-if="showSignUp" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-lg  font-semibold text-gray-900">
            Sign Up to our platform 😇
          </h3>
          <button @click="showSignUp = false" type="button"
            class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <!-- Modal body -->
        <div class="p-5">
          <form class="space-y-4" action="#">
            <div>
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900 ">Your username</label>
              <input type="text" name="username" id="username" autocomplete="off"
                class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Your
                password</label>
              <input type="password" name="password" id="password" placeholder="••••••••"
                class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <div>
              <label for="image" class="block mb-2 text-sm font-medium text-gray-900">Your Profile Image</label>
              <input type="file" id="image" name="image" accept="image/*" @change="handleImageUpload"
                class="block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
              <img v-if="imagePreview" :src="imagePreview" class="mt-2 h-28 w-28 object-cover rounded-lg"
                alt="Image Preview" />
            </div>
            <div>
              <label for="email" class="mb-2 text-sm font-medium text-gray-900 flex flex-col">Your email
                (Optional)</label>
              <input type="text" name="email" id="email" autocomplete="off"
                class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337@gmail.com" />
            </div>
            <button type="submit"
              class="w-full text-white bg-red-500 hover:bg-red-600 focus:ring-4  font-medium rounded-3xl text-sm px-5 py-2.5 text-center">Sign
              Up</button>
            <div class="text-sm font-medium text-gray-500 ">
              Already have an account? <a href="#" class="text-red-500 hover:underline">Login</a>
            </div>
            <div class="flex">
              <a href="#" class="text-sm text-red-500 hover:underline">Lost Password?</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

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
        <div v-for="(image, index) in images.slice(5, 10)" :key="index" class="p-2"
          :data-aos="index % 2 !== 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-full h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div v-if="bg === 'bg-green-100'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(10, 15)" :key="index" class="p-2"
          :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-full h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div class="text-center">
        <h1 class="text-5xl  font-bold text-black mb-6">{{ textWelcome }}</h1>
        <div class="space-x-4">
          <!-- Signup Button -->
          <button @mouseenter="changeBgColor1" @mouseleave="changeDefaultColor" @click="showSignUp = true"
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
