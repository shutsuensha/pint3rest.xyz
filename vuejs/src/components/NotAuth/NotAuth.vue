<script setup>
import { onMounted, ref, reactive, computed } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import AOS from 'aos';
import 'aos/dist/aos.css';
import { useToast } from "vue-toastification";
import DescriptionApp from '@/components/NotAuth/DescriptionApp.vue';
import { initializeKinesis } from "@amineyarman/kinesis"; // Import the function

const tailwindColors = {
  "bg-red-100": "#fee2e2",
  "bg-red-200": "#fecaca",
  "bg-red-300": "#fca5a5",
  "bg-green-100": "#dcfce7",
  "bg-green-200": "#bbf7d0",
  "bg-green-300": "#86efac",
  "bg-violet-100": "#f5f3ff",
  "bg-violet-200": "#ddd6fe",
  "bg-violet-300": "#c4b5fd",
  "bg-pink-100": "#fce7f3",
  "bg-pink-200": "#fbcfe8",
  "bg-pink-300": "#f9a8d4",
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


const toast = useToast();

const bg = ref('bg-green-300')

const colorBg = computed(() => tailwindColors[bg.value] || "#ffffff");

const loading = ref(true)
const color = ref('red')
const size = ref('100px')

const textWelcome = ref('Welcome to Our Platform 🩸')

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


async function submitSignUp() {
  const username = formSignUp.username
  const password = formSignUp.password
  const email = formSignUp.email

  if (!username.trim()) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password.trim()) {
    toast.warning('Please, enter Password', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!imageFile.value) {
    toast.warning('Please, Upload Profile Image', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  showSignUpLoader.value = true

  if (!email.trim()) {
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

async function submitLogin() {
  const username = formLogin.username
  const password = formLogin.password

  if (!username.trim()) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password.trim()) {
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
  const username = formPasswordReset.username
  const password = formPasswordReset.password
  const email = formPasswordReset.email

  if (!username.trim()) {
    toast.warning('Please, enter Username', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!email.trim()) {
    toast.warning('Please, enter Email', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  if (!password.trim()) {
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

function changeDefaultColor() {
  bg.value = 'bg-white'
  textWelcome.value = 'Welcome to Our Platform 🩸'
}

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result; // Update the preview data
    };
    reader.readAsDataURL(file);
  }
}

onMounted(async () => {
  document.title = 'Pint3rest Next-Gen'
  initializeKinesis()
  AOS.init({
    duration: 3000,  // 800 мс (быстрее)
    once: false     // Позволит анимации повторяться при повторном наведении
  });
  try {
    for (let i = 1; i <= 15; i++) {
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


</script>

<template>
  <DescriptionApp />
  <div v-if="showSignUp" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-cent er justify-between p-4 md:p-5 border-b rounded-t">
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
        <ClipLoader v-if="showSignUpLoader" :color="color" :size="size"
          class="flex items-center justify-center h-96 font-extrabold" />
        <!-- Modal body -->
        <div v-else class="p-5">
          <form class="space-y-4" @submit.prevent="submitSignUp">
            <div>
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900 ">Your username</label>
              <input v-model="formSignUp.username" type="text" name="username" id="username" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Your
                password</label>
              <input v-model="formSignUp.password" type="password" name="password" id="password" placeholder="••••••••"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <div>
              <label for="image" class="block mb-2 text-sm font-medium text-gray-900">Your Profile Image</label>
              <input type="file" id="image" name="image" accept="image/*" @change="handleImageUpload"
                class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
              <img v-if="imagePreview" :src="imagePreview" class="mt-2 h-28 w-28 object-cover rounded-lg"
                alt="Image Preview" />
            </div>
            <div>
              <label for="email" class="mb-2 text-sm font-medium text-gray-900 flex flex-col">Your email
                (Optional)</label>
              <input v-model="formSignUp.email" type="text" name="email" id="email" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337@gmail.com" />
            </div>
            <button type="submit"
              class="w-full transition duration-300  text-white bg-red-500 hover:bg-red-600 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">Sign
              Up</button>
            <div class="text-sm font-medium text-gray-500 ">
              Already have an account? <a @click="showSignUp = false; showLogin = true"
                class="text-red-500 hover:underline cursor-pointer">Login</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showLogin" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-lg  font-semibold text-gray-900">
            Already have an account ? 🤫
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
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900 ">Your username</label>
              <input v-model="formLogin.username" type="text" name="username" id="username" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Your
                password</label>
              <input v-model="formLogin.password" type="password" name="password" id="password" placeholder="••••••••"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <button type="submit"
              class=" transition duration-300 w-full text-white bg-red-500 hover:bg-red-600 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">Log
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

  <div v-if="showPasswordReset" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <!-- Modal content -->
      <div class="relative bg-white rounded-3xl">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-lg  font-semibold text-gray-900">
            Password Reset >< </h3>
              <button @click="showPasswordReset = false" type="button"
                class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center">
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 14 14">
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
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900 ">Your username</label>
              <input v-model="formPasswordReset.username" type="text" name="username" id="username" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337" />
            </div>
            <div>
              <label for="email" class="mb-2 text-sm font-medium text-gray-900 flex flex-col">Your email</label>
              <input v-model="formPasswordReset.email" type="text" name="email" id="email" autocomplete="off"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="akinak1337@gmail.com" />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Your
                New Password</label>
              <input v-model="formPasswordReset.password" type="password" name="password" id="password"
                placeholder="••••••••"
                class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500" />
            </div>
            <button type="submit"
              class="w-full transition duration-300 text-white bg-red-500 hover:bg-red-600 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">Reset
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


  <ClipLoader v-if="loading" :color="color" :size="size"
    class="flex items-center justify-center h-screen font-extrabold" />
  <div v-else :style="{ background: `linear-gradient(to top, ${colorBg}, white)` }"
    class="flex items-center justify-center h-screen">

    <div class="items-center space-y-6 flex flex-col">
      <div v-if="bg === 'bg-green-300'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(0, 5)" :key="index" class="p-2"
          :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'">
          <img :src="image" alt="Image" class="w-[240px] h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div v-if="bg === 'bg-violet-300'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(5, 10)" :key="index" class="p-2"
          :data-aos="index % 2 !== 0 ? 'fade-down' : 'fade-up'" >
          <img :src="image" alt="Image" class="w-[240px] h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div v-if="bg === 'bg-red-300'" class="grid grid-cols-5 gap-4">
        <div v-for="(image, index) in images.slice(10, 15)" :key="index" class="p-2"
          :data-aos="index % 2 === 0 ? 'fade-down' : 'fade-up'" >
          <img :src="image" alt="Image" class="w-[240px] h-80 rounded-3xl object-cover">
        </div>
      </div>
      <div class="text-center z-30">
        <h1 class="text-4xl  text-black mb-6">{{ textWelcome }}</h1>
        <div class="space-x-4">
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
        </div>
      </div>
    </div>
  </div>
</template>
