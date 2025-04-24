<script setup>
import { onMounted, ref, reactive, computed, onUnmounted } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import AOS from 'aos';
import 'aos/dist/aos.css';
import { useToast } from "vue-toastification";
import DescriptionApp from '@/components/NotAuth/DescriptionApp.vue';
import { initializeKinesis } from "@amineyarman/kinesis"; // Import the functio

import Overview from '@/components/NotAuth/Overview.vue'

import logo from '@/assets/logo.png'


import { useRouter, useRoute } from 'vue-router'


const router = useRouter()
const route = useRoute()


import google_logo from '@/assets/g-logo.png';

const scrollContainer = ref(null)
let currentIndex = 0
let isScrolling = false
const sectionsCount = 2

const easings = {
  easeInOutCubic(t, b, c, d) {
    t /= d / 2
    if (t < 1) return c / 2 * t * t * t + b
    t -= 2
    return c / 2 * (t * t * t + 2) + b
  },
  linear(t, b, c, d) {
    return c * t / d + b
  },
}

function scrollToSection(index, easingName = 'easeInOutCubic') {
  if (index < 0 || index >= sectionsCount) return
  isScrolling = true

  const container = scrollContainer.value
  const start = container.scrollTop
  const end = container.children[index].offsetTop
  const change = end - start
  const duration = 800
  let startTime = null

  const ease = easings[easingName] || easings.linear

  function animateScroll(timestamp) {
    if (!startTime) startTime = timestamp
    const elapsed = timestamp - startTime
    const next = ease(elapsed, start, change, duration)
    container.scrollTop = next

    if (elapsed < duration) {
      requestAnimationFrame(animateScroll)
    } else {
      container.scrollTop = end
      currentIndex = index
      isScrolling = false
    }
  }

  requestAnimationFrame(animateScroll)
}

function onWheel(e) {
  e.preventDefault()
  if (isScrolling) return
  if (e.deltaY > 0) scrollToSection(currentIndex + 1)
  else if (e.deltaY < 0) scrollToSection(currentIndex - 1)
}





const tailwindColors = {
  "bg-red-100": "#fee2e2",
  "bg-red-200": "#fecaca",
  "bg-red-300": "#fca5a5",
  "bg-red-800": "#991b1b",
  "bg-red-900": "#7f1d1d",

  "bg-green-100": "#dcfce7",
  "bg-green-200": "#bbf7d0",
  "bg-green-300": "#86efac",
  "bg-green-800": "#166534",
  "bg-green-900": "#14532d",

  "bg-violet-100": "#f5f3ff",
  "bg-violet-200": "#ddd6fe",
  "bg-violet-300": "#c4b5fd",
  "bg-violet-800": "#5b21b6",
  "bg-violet-900": "#4c1d95",

  "bg-pink-100": "#fce7f3",
  "bg-pink-200": "#fbcfe8",
  "bg-pink-300": "#f9a8d4",
  "bg-pink-800": "#9d174d",
  "bg-pink-900": "#831843",

  "bg-blue-100": "#dbeafe",
  "bg-blue-200": "#bfdbfe",
  "bg-blue-300": "#93c5fd",
  "bg-blue-800": "#1e40af",
  "bg-blue-900": "#1e3a8a",

  "bg-yellow-100": "#fef9c3",
  "bg-yellow-200": "#fef08a",
  "bg-yellow-300": "#fde047",
  "bg-yellow-800": "#a16207",
  "bg-yellow-900": "#854d0e",

  "bg-gray-100": "#f3f4f6",
  "bg-gray-200": "#e5e7eb",
  "bg-gray-300": "#d1d5db",
  "bg-gray-800": "#1f2937",
  "bg-gray-900": "#111827",

  "bg-teal-100": "#ccfbf1",
  "bg-teal-200": "#99f6e4",
  "bg-teal-300": "#5eead4",
  "bg-teal-800": "#115e59",
  "bg-teal-900": "#134e4a",

  "bg-orange-100": "#ffedd5",
  "bg-orange-200": "#fed7aa",
  "bg-orange-300": "#fdba74",
  "bg-orange-800": "#9a3412",
  "bg-orange-900": "#7c2d12",

  "bg-indigo-100": "#e0e7ff",
  "bg-indigo-200": "#c7d2fe",
  "bg-indigo-300": "#a5b4fc",
  "bg-indigo-800": "#3730a3",
  "bg-indigo-900": "#312e81",

  // Добавь другие цвета, если нужно
};




const buttonBg = ref('bg-indigo-400')
const buttonText = ref('text-white')
const buttonBgHover = ref('hover:bg-indigo-600')
const buttonBgHoverText = ref('hover:text-white')


const buttonBg2 = ref('bg-red-400')
const buttonText2 = ref('text-white')
const buttonBgHover2 = ref('hover:bg-red-600')
const buttonBgHoverText2 = ref('hover:text-white')

const buttonBg3 = ref('bg-black')
const buttonText3 = ref('text-white')
const buttonBgHover3 = ref('hover:bg-black')
const buttonBgHoverText3 = ref('hover:text-white')


const toast = useToast();

const bg = ref('bg-green-300')

const colorBg = computed(() => tailwindColors[bg.value] || "#ffffff");

const loading = ref(true)
const color = ref('red')
const size = ref('100px')

const textWelcome = ref('Welcome to Pinterest 🩸')

const images = ref([])

const showSignUp = ref(false)
const showLogin = ref(false)
const showPasswordReset = ref(false)

const imageFile = ref(null);
const imagePreview = ref(null)

const showErrorModalSignup = ref(false)
const errorMessageSignup = ref('')

const showErrorModalLogin = ref(false)
const errorMessageLogin = ref('')

const showErrorModalPasswordReset = ref(false)
const errorMessagePasswordReset = ref('')

const formSignUp = reactive({
  username: '',
  password: '',
  email: '',
});


const formLogin = reactive({
  username: '',
  password: ''
});

const formPasswordReset = reactive({
  username: '',
  email: '',
  password: ''
});


const emit = defineEmits(['login', 'signup'])

const showSignUpLoader = ref(false)
const showLoginLoader = ref(false)
const showPasswordResetLoader = ref(false)

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // For smooth scrolling
  });
}

const fileError = ref(false)


function addQueryToCurrentRoute() {
  router.push({
    path: route.path,
    query: {
      ...route.query,
      register: 'true'
    }
  })
}

async function submitSignUp() {
  const username = formSignUp.username.trim()
  const password = formSignUp.password.trim()
  const email = formSignUp.email.trim()

  if (!username) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password) {
    toast.warning('Please, enter Password', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!imageFile.value) {
    toast.warning('Please, Upload Profile Image', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  showSignUpLoader.value = true

  if (!email) {
    try {
      const formData = new FormData();
      formData.append("file", imageFile.value); // Файл

      const jsonData = JSON.stringify({
        username: username,
        password: password
      });

      formData.append("user_model", jsonData); // Передаем строку, а не Blob

      const response = await axios.post("/api/users/create-user-entity", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      try {
        const response = await axios.post('/api/users/login', {
          username: username,
          password: password
        })
        const access_token = response.data.access_token

        scrollToTop()
        showSignUpLoader.value = false
        showSignUp.value = false

        addQueryToCurrentRoute()

        emit('signup', access_token)
      } catch (error) {
        showSignUpLoader.value = false
        showErrorModalSignup.value = true
        showSignUp.value = false
        errorMessageSignup.value = 'Unknown error, try later'
      }

    } catch (error) {
      if (error.response.status === 409) {
        showSignUpLoader.value = false
        showErrorModalSignup.value = true
        showSignUp.value = false
        errorMessageSignup.value = 'User already exists'
      }
      if (error.response.status === 415) {
        fileError.value = true
      }
    }
  } else {
    try {
      const formData = new FormData();
      formData.append("file", imageFile.value); // Файл

      const jsonData = JSON.stringify({
        username: username,
        password: password,
        email: email
      });

      formData.append("user_model", jsonData); // Передаем строку, а не Blob

      const response = await axios.post("/api/users/create-user-entity", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      showSignUpLoader.value = false
      showSignUp.value = false
      showLogin.value = true

      addQueryToCurrentRoute()

      toast.success(`Verification Link is sending on ${email}`, { timeout: 10000, closeOnClick: false, position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });

    } catch (error) {
      if (error.response.status === 409) {
        showSignUpLoader.value = false
        showErrorModalSignup.value = true
        showSignUp.value = false
        errorMessageSignup.value = 'User already exists'
      }
      if (error.response.status === 422) {
        showSignUpLoader.value = false
        showErrorModalSignup.value = true
        showSignUp.value = false
        errorMessageSignup.value = 'Enter correct email, please'
      }
    }
  }
}

const testLoginLoading = ref(false)

async function handleTestLogin() {

  testLoginLoading.value = true

  formLogin.username = 'testusername'
  formLogin.password = 'testusername'

  addQueryToCurrentRoute()

  submitLogin()
}

async function submitLogin() {
  const username = formLogin.username.trim()
  const password = formLogin.password.trim()

  if (!username) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password) {
    toast.warning('Please, enter Password', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  showLoginLoader.value = true


  try {
    const response = await axios.post('/api/users/login', {
      username: username,
      password: password
    })
    const access_token = response.data.access_token
    scrollToTop()

    showLoginLoader.value = false
    showLogin.value = false
    testLoginLoading.value = false

    emit('login', access_token)
  } catch (error) {
    if (error.response.status === 401) {
      showLoginLoader.value = false
      showErrorModalLogin.value = true
      showLogin.value = false
      errorMessageLogin.value = error.response.data.detail
    }
    if (error.response.status === 403) {
      showLoginLoader.value = false
      showErrorModalLogin.value = true
      showLogin.value = false
      errorMessageLogin.value = 'You need verify your account to login'
      toast.success(`${error.response.data.detail}`, { timeout: 10000, closeOnClick: false, position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    }
  }
}


async function submitPasswordReset() {
  const username = formPasswordReset.username.trim()
  const password = formPasswordReset.password.trim()
  const email = formPasswordReset.email.trim()

  if (!username) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!email) {
    toast.warning('Please, enter Email', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password) {
    toast.warning('Please, enter new Password', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  showPasswordResetLoader.value = true

  try {
    const response = await axios.post('/api/users/password-reset-request', {
      username: username,
      email: email,
      password: password
    })

    toast.success(`Password Reset Link is sending on ${email}`, { timeout: 10000, closeOnClick: false, position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });

    showPasswordResetLoader.value = false
    showPasswordReset.value = false
    showLogin.value = true

  } catch (error) {
    if (error.response.status === 422) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = 'Enter Correct Email'
    }
    if (error.response.status === 404) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = 'user not found'
    }
    if (error.response.status === 403) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = error.response.data.detail
    }
    if (error.response.status === 400) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = error.response.data.detail
    }
    if (error.response.status === 405) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = error.response.data.detail
    }
    if (error.response.status === 406) {
      showPasswordResetLoader.value = false
      showErrorModalPasswordReset.value = true
      showPasswordReset.value = false
      errorMessagePasswordReset.value = error.response.data.detail
    }
  }
}


function changeBgColor1() {
  bg.value = 'bg-violet-300'
  textWelcome.value = 'First time here ? - Sign Up 😇'
}

function changeBgColor2() {
  bg.value = 'bg-red-300'
  textWelcome.value = 'Already have an account ? 🤫'
}

function changeBgColor3() {
  bg.value = 'bg-teal-300'
  textWelcome.value = 'Continue Google 𓆩🖤𓆪'
}

function changeDefaultColor() {
  bg.value = 'bg-white'
  textWelcome.value = 'Welcome to Our Platform 🩸'
}

function handleImageUpload(event) {
  const file = event.target.files[0];

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp'];


  if (file) {

    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid image file (.jpg, .jpeg, .gif, .webp, .png, .bmp).', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
      return;
    }

    imageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result; // Update the preview data
    };
    reader.readAsDataURL(file);
  }
}

onUnmounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('wheel', onWheel)
  }
})

onMounted(async () => {
  scrollContainer.value.addEventListener('wheel', onWheel, { passive: false })

  document.title = 'Pinterest'
  initializeKinesis()


  AOS.init({
    duration: 3000,  // 800 мс (быстрее)
    once: true     // Позволит анимации повторяться при повторном наведении
  });
  try {
    for (let i = 1; i <= 20; i++) {
      const response = await axios.get(`/api/notauth/images/${i}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(response.data);
      images.value.push(blobUrl)
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})


async function googleAuth() {
  try {
    const response = await axios.get('/api/users/google/auth/login/')
    const data = response.data
    window.location.href = data.url;
  } catch (error) {
    console.error(error)
  }
}

const overview = ref(
  {
    src: '/screenshots/overview.png',
    stream: 'overview.mp4',
    title: 'Overview',
  })
</script>

<template>
  <div v-show="showSignUp" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    @click.self="showSignUp = false">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <!-- Logo -->
          <h3 class="text-lg font-semibold text-gray-900">Sign Up to Pinterest 😇</h3>
          <button @click="showSignUp = false" type="button"
            class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>

        <ClipLoader v-if="showSignUpLoader" :color="color" :size="size"
          class="flex items-center justify-center h-96 font-extrabold" />

        <!-- Modal body -->
        <div v-else class="p-5">
          <form class="space-y-4" @submit.prevent="submitSignUp">
            <div>
              <label for="usernamesignup" class="block mb-2 text-sm font-medium text-gray-900">Your username</label>
              <input v-model="formSignUp.username" type="text" name="username" id="usernamesignup" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="passwordsignup" class="block mb-2 text-sm font-medium text-gray-900">Your password</label>
              <input v-model="formSignUp.password" type="password" name="password" id="passwordsignup"
                placeholder="••••••••" autocomplete="new-password"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <div class="flex items-center space-x-4">
              <div class="w-full">
                <label for="imagesignup" class="block mb-2 text-sm font-medium text-gray-900">Your Profile Image (.jpg
                  .jpeg .gif .webp .png .bmp)</label>
                <input type="file" id="imagesignup" name="image" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp"
                  @change="handleImageUpload"
                  class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
              </div>
            </div>
            <div class="w-full flex justify-center">
              <div class="w-28 h-28 object-cover rounded-full" v-if="imagePreview">
                <img :src="imagePreview" class="w-full h-full object-cover rounded-full" alt="Image Preview" />
              </div>
            </div>
            <div>
              <label for="emailsignup" class="mb-2 text-sm font-medium text-gray-900 flex flex-col">Your email
                (Optional)</label>
              <input v-model="formSignUp.email" type="text" name="email" id="emailsignup" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337@gmail.com" />
            </div>
            <button type="submit"
              class="w-full transition duration-300 text-white bg-red-500 hover:bg-red-600 font-semibold rounded-3xl text-sm px-5 py-3 text-center">Sign
              Up</button>
            <div class="text-sm font-medium text-gray-500">
              Already have an account? <a @click="showSignUp = false; showLogin = true"
                class="text-red-500 hover:underline cursor-pointer">Login</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-show="showLogin" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    @click.self="showLogin = false">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <!-- Logo -->
          <h3 class="text-lg font-semibold text-gray-900">
            Log In to Pinterest 🤫
          </h3>
          <button @click="showLogin = false" type="button"
            class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <ClipLoader v-if="showLoginLoader" :color="color" :size="size"
          class="flex items-center justify-center h-96 font-extrabold" />
        <!-- Modal body -->
        <div v-else class="p-5">
          <form class="space-y-4" @submit.prevent="submitLogin">
            <div>
              <label for="usernamelogin" class="block mb-2 text-sm font-medium text-gray-900 ">Your username</label>
              <input v-model="formLogin.username" type="text" name="username" id="usernamelogin" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="passwordlogin" class="block mb-2 text-sm font-medium text-gray-900">Your
                password</label>
              <input v-model="formLogin.password" type="password" name="password" id="passwordlogin"
                placeholder="••••••••" autocomplete="current-password"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <button type="submit"
              class=" transition duration-300 w-full text-white bg-red-500 hover:bg-red-600 font-semibold rounded-3xl text-sm px-5 py-3 text-center">Log
              In</button>
            <div class="text-sm font-medium text-black ">
              Dont have an account? <a @click="showLogin = false; showSignUp = true"
                class="text-red-500 hover:underline cursor-pointer">Sign Up</a>
            </div>
            <div class="flex">
              <a @click="showLogin = false; showPasswordReset = true"
                class="text-sm text-red-500 hover:underline cursor-pointer">Lost Password?</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-show="showPasswordReset" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    @click.self="showPasswordReset = false">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <!-- Logo -->
          <h3 class="text-lg font-semibold text-gray-900">
            Password Reset
          </h3>
          <button @click="showPasswordReset = false" type="button"
            class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <ClipLoader v-if="showPasswordResetLoader" :color="color" :size="size"
          class="flex items-center justify-center h-96 font-extrabold" />
        <!-- Modal body -->
        <div v-else class="p-5">
          <form class="space-y-4" @submit.prevent="submitPasswordReset">
            <div>
              <label for="usernamepasswordreset" class="block mb-2 text-sm font-medium text-gray-900 ">Your
                username</label>
              <input v-model="formPasswordReset.username" type="text" name="username" id="usernamepasswordreset"
                autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="emailpasswordreset" class="mb-2 text-sm font-medium text-gray-900 flex flex-col">Your
                email</label>
              <input v-model="formPasswordReset.email" type="text" name="email" id="emailpasswordreset"
                autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337@gmail.com" />
            </div>
            <div>
              <label for="passwordpasswordreset" class="block mb-2 text-sm font-medium text-gray-900">Your
                New Password</label>
              <input v-model="formPasswordReset.password" type="password" name="password" id="passwordpasswordreset"
                autocomplete="new-password" placeholder="••••••••"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <button type="submit"
              class="w-full transition duration-300 text-white bg-red-500 hover:bg-red-600 font-medium rounded-3xl text-sm px-5 py-3 text-center">Reset
              Password</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showErrorModalSignup" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> {{ errorMessageSignup }} </h3>
          <button @click="showErrorModalSignup = false; showSignUp = true" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="fileError" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp,
            .png, .bmp </h3>
          <button @click="fileError = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showErrorModalLogin" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-gray-500"> {{ errorMessageLogin }} </h3>
          <button @click="showErrorModalLogin = false; showLogin = true" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showErrorModalPasswordReset"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-gray-500"> {{ errorMessagePasswordReset }} </h3>
          <button @click="showErrorModalPasswordReset = false; showPasswordReset = true" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>


  <!-- <ClipLoader v-if="loading" :color="color" :size="size"
    class="flex items-center justify-center h-screen font-extrabold" /> -->
  <div ref="scrollContainer" class="relative overflow-hidden h-screen">

    <div v-if="loading" class="flex items-center justify-center h-screen">
      <span class="loader text-4xl"></span>
    </div>
    <div v-else :style="{ background: `linear-gradient(to top, ${colorBg}, white)` }"
      class="flex items-center justify-center h-screen overflow-hidden relative">

      <img src="/screen.jpg" class="absolute top-0 right-0 h-screen opacity-60 w-[700px] mask-gradient" />

      <div class="absolute bottom-2 left-1/2 transform -translate-x-1/2" @click="scrollToSection(1)">
        <button
          class="items-center justify-center flex z-50 px-6 py-3 text-white text-lg font-semibold bg-red-600 rounded-3xl animate-bounce-slow">
          Overview <i class="ml-2 pi pi-angle-down"></i>
        </button>
      </div>

      <!-- <img src="/screen.jpg" class="absolute top-0 right-0 h-screen w-[700px] opacity-40 mask-gradient" /> -->
      <div class="relative z-10 max-w-7xl mx-auto px-6 py-12 flex flex-col items-center">
        <!-- Логотип и заголовки -->
        <img :src="logo" alt="Pinterest Logo" class="w-24 h-24 mb-6" />

        <h1
          class="text-6xl font-semibold mb-4 text-center bg-gradient-to-r from-indigo-600 to-red-700 text-transparent bg-clip-text">
          Pinterest Clone
        </h1>
        <h2
          class="text-4xl font-semibold mb-12 text-center bg-gradient-to-r from-purple-600 to-red-700 text-transparent bg-clip-text">
          1536 × 864 / Vue 3 &amp; FastAPI
        </h2>

        <div class="w-full max-w-sm bg-white bg-opacity-50 backdrop-blur-sm rounded-3xl p-8 shadow-lg">
          <h3 class="text-2xl font-bold mb-1 text-gray-800 text-center">Quick Log In</h3>

          <div v-if="testLoginLoading" class="flex items-center justify-center h-full p-3">
            <span class="text-center loader2"></span>
          </div>

          <button v-if="!testLoginLoading" @click="handleTestLogin"
            class="w-full mt-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-3xl transition">
            Login as Test User
          </button>
        </div>
      </div>

      <div class="items-center space-y-6 flex flex-col">
        <div v-if="bg === 'bg-green-300'" class="grid grid-cols-5 gap-1">
          <div v-for="(image, index) in images.slice(0, 5)" :key="index" class="p-1"
            :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'">
            <img :src="image" alt="Image" class="w-[240px] h-60 rounded-3xl object-cover">
          </div>
        </div>
        <div v-if="bg === 'bg-violet-300'" class="grid grid-cols-5 gap-1">
          <div v-for="(image, index) in images.slice(5, 10)" :key="index" class="p-1"
            :data-aos="index % 2 !== 0 ? 'flip-right' : 'zoom-in'" data-aos-easing="ease" :data-aos-duration="2000">
            <img :src="image" alt="Image" class="w-[240px] h-60 rounded-3xl object-cover">
          </div>
        </div>
        <div v-if="bg === 'bg-red-300'" class="grid grid-cols-5 gap-1">
          <div v-for="(image, index) in images.slice(10, 15)" :key="index" class="p-1"
            :data-aos="index % 2 === 0 ? 'zoom-in' : 'flip-right'" data-aos-easing="ease" :data-aos-duration="2000">
            <img :src="image" alt="Image" class="w-[240px] h-60 rounded-3xl object-cover">
          </div>
        </div>
        <div v-if="bg === 'bg-teal-300'" class="grid grid-cols-5 gap-1">
          <div v-for="(image, index) in images.slice(15, 20)" :key="index" class="p-1"
            :data-aos="index % 2 === 0 ? 'zoom-in' : 'zoom-out'" data-aos-easing="ease" :data-aos-duration="2000">
            <img :src="image" alt="Image" class="w-[240px] h-60 rounded-3xl object-cover">
          </div>
        </div>
        <div class="text-center z-30">
          <h1 v-if="bg === 'bg-red-300'" class="text-4xl  text-black mb-6" data-aos="zoom-in" data-aos-easing="ease"
            :data-aos-duration="2000">{{ textWelcome }}</h1>
          <h1 v-if="bg === 'bg-violet-300'" class="text-4xl  text-black mb-6" :data-aos="'zoom-in'"
            data-aos-easing="ease" :data-aos-duration="2000">{{ textWelcome }}</h1>
          <h1 v-if="bg === 'bg-green-300'" class="text-4xl  text-black mb-6" :data-aos="'zoom-in'"
            data-aos-easing="ease" :data-aos-duration="2000">{{ textWelcome }}</h1>
          <h1 v-if="bg === 'bg-teal-300'" class="text-4xl  text-black mb-6" :data-aos="'zoom-in'" data-aos-easing="ease"
            :data-aos-duration="2000">{{ textWelcome }}</h1>
          <div v-if="bg === 'bg-green-300'" class="space-x-2 flex flex-row justify-center items-center"
            :data-aos="'zoom-in'" data-aos-easing="ease" :data-aos-duration="3000">
            <!-- Signup Button -->
            <button @mouseenter="changeBgColor1" @click="showSignUp = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg} ${buttonText} font-semibold rounded-3xl transition ${buttonBgHover} ${buttonBgHoverText}`">
              Sign Up
            </button>

            <!-- Login Button -->
            <button @mouseenter="changeBgColor2" @click="showLogin = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg2} ${buttonText2} font-semibold rounded-3xl transition ${buttonBgHover2} ${buttonBgHoverText2}`">
              Log In
            </button>

            <button @click="googleAuth" @mouseenter="changeBgColor3"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg3} ${buttonText3} font-semibold rounded-3xl transition ${buttonBgHover3} ${buttonBgHoverText3}`">
              <div class="flex flex-row gap-2 items-center justify-center">
                <img :src="google_logo" alt="Google Logo" class="rounded-full w-5 h-5">
                <span>Google</span>
              </div>
            </button>
          </div>
          <div v-if="bg === 'bg-violet-300'" class="space-x-2 flex flex-row justify-center items-center" :data-aos="``"
            data-aos-easing="ease" :data-aos-duration="2000">
            <!-- Signup Button -->
            <button @mouseenter="changeBgColor1" @click="showSignUp = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg} ${buttonText} font-semibold rounded-3xl transition ${buttonBgHover} ${buttonBgHoverText}`">
              Sign Up
            </button>

            <!-- Login Button -->
            <button @mouseenter="changeBgColor2" @click="showLogin = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg2} ${buttonText2} font-semibold rounded-3xl transition ${buttonBgHover2} ${buttonBgHoverText2}`">
              Log In
            </button>

            <button @click="googleAuth" @mouseenter="changeBgColor3"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg3} ${buttonText3} font-semibold rounded-3xl transition ${buttonBgHover3} ${buttonBgHoverText3}`">
              <div class="flex flex-row gap-2 items-center justify-center">
                <img :src="google_logo" alt="Google Logo" class="rounded-full w-5 h-5">
                <span>Google</span>
              </div>
            </button>
          </div>
          <div v-if="bg === 'bg-red-300'" class="space-x-2 flex flex-row justify-center items-center" :data-aos="''"
            data-aos-easing="ease" :data-aos-duration="2000">
            <!-- Signup Button -->
            <button @mouseenter="changeBgColor1" @click="showSignUp = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg} ${buttonText} font-semibold rounded-3xl transition ${buttonBgHover} ${buttonBgHoverText}`">
              Sign Up
            </button>

            <!-- Login Button -->
            <button @mouseenter="changeBgColor2" @click="showLogin = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg2} ${buttonText2} font-semibold rounded-3xl transition ${buttonBgHover2} ${buttonBgHoverText2}`">
              Log In
            </button>

            <button @click="googleAuth" @mouseenter="changeBgColor3"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg3} ${buttonText3} font-semibold rounded-3xl transition ${buttonBgHover3} ${buttonBgHoverText3}`">
              <div class="flex flex-row gap-2 items-center justify-center">
                <img :src="google_logo" alt="Google Logo" class="rounded-full w-5 h-5">
                <span>Google</span>
              </div>
            </button>
          </div>
          <div v-if="bg === 'bg-teal-300'" class="space-x-2 flex flex-row justify-center items-center" :data-aos="''"
            data-aos-easing="ease" :data-aos-duration="3000">
            <!-- Signup Button -->
            <button @mouseenter="changeBgColor1" @click="showSignUp = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg} ${buttonText} font-semibold rounded-3xl transition ${buttonBgHover} ${buttonBgHoverText}`">
              Sign Up
            </button>

            <!-- Login Button -->
            <button @mouseenter="changeBgColor2" @click="showLogin = true"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg2} ${buttonText2} font-semibold rounded-3xl transition ${buttonBgHover2} ${buttonBgHoverText2}`">
              Log In
            </button>

            <button @click="googleAuth" @mouseenter="changeBgColor3"
              :class="`hover:-translate-y-2 px-6 py-3 ${buttonBg3} ${buttonText3} font-semibold rounded-3xl transition ${buttonBgHover3} ${buttonBgHoverText3}`">
              <div class="flex flex-row gap-2 items-center justify-center">
                <img :src="google_logo" alt="Google Logo" class="rounded-full w-5 h-5">
                <span>Google</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>


    <div class="h-screen overflow-hidden w-full">
      <div class="z-0 pointer-events-none">
        <Overview :card="overview" />
      </div>
    </div>

  </div>

</template>

<style scoped>
@keyframes bounce-slow {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-15px);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 2s ease-in-out infinite;
}

.loader {
  transform: rotateZ(45deg);
  perspective: 1000px;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  color: rgb(231, 15, 15);
}

.loader:before,
.loader:after {
  content: '';
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: inherit;
  height: inherit;
  border-radius: 50%;
  transform: rotateX(70deg);
  animation: 1s spin linear infinite;
}

.loader:after {
  color: #000000;
  transform: rotateY(70deg);
  animation-delay: .3s;
}

@keyframes rotate {
  0% {
    transform: translate(-50%, -50%) rotateZ(0deg);
  }

  100% {
    transform: translate(-50%, -50%) rotateZ(360deg);
  }
}

@keyframes rotateccw {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  100% {
    transform: translate(-50%, -50%) rotate(-360deg);
  }
}

@keyframes spin {

  0%,
  100% {
    box-shadow: .2em 0px 0 0px currentcolor;
  }

  12% {
    box-shadow: .2em .2em 0 0 currentcolor;
  }

  25% {
    box-shadow: 0 .2em 0 0px currentcolor;
  }

  37% {
    box-shadow: -.2em .2em 0 0 currentcolor;
  }

  50% {
    box-shadow: -.2em 0 0 0 currentcolor;
  }

  62% {
    box-shadow: -.2em -.2em 0 0 currentcolor;
  }

  75% {
    box-shadow: 0px -.2em 0 0 currentcolor;
  }

  87% {
    box-shadow: .2em -.2em 0 0 currentcolor;
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


.loader2 {
  width: 48px;
  height: 48px;
  background: #FFF;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

.loader2::after {
  content: '';
  box-sizing: border-box;
  position: absolute;
  left: 6px;
  top: 10px;
  width: 12px;
  height: 12px;
  color: #FF3D00;
  background: currentColor;
  border-radius: 50%;
  box-shadow: 25px 2px, 10px 22px;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>