<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import CreatedPins from '@/components/Auth/CreatedPins.vue';
import SavedPins from '@/components/Auth/SavedPins.vue';
import LikedPins from '@/components/Auth/LikedPins.vue';

const color = ref('red');
const size = ref('100px');

const route = useRoute();
const router = useRouter();

const loadingUser = ref(true);

const username = route.params.username;
const user = ref(null);
const userImage = ref(null);

const userBanner = ref(null)

const auth_user_id = ref(null);

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const canEditProfile = ref(false)
const showEditModal = ref(false)


const editUsername = ref('')
const editDescription = ref('')
const editInstagram = ref('')
const editTiktok = ref('')
const editTelegram = ref('')
const editPinterest = ref('')

const imageFile = ref(null)
const imagePreview = ref(null)

const bannerImageFile = ref(null)
const bannerImagePreview = ref(null)


onMounted(async () => {
  const accessToken = getCookie('access_token');
  // Decode the JWT (assuming the access_token is a JWT)
  const base64Url = accessToken.split('.')[1]; // Get the payload part
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );

  const payload = JSON.parse(jsonPayload);

  // Log user_id to the console
  auth_user_id.value = payload.user_id;



  try {
    const response = await axios.get(`/api/users/user_username/${username}`);
    user.value = response.data;
    canEditProfile.value = auth_user_id.value === user.value.id
    if (canEditProfile.value) {
      document.title = 'pinterest.xyz / me ' + user.value.username
    } else {
      document.title = 'pinterest.xyz / user ' + user.value.username
    }

    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;
    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    router.push('/not-found')
  }

  try {
    if (user.value.banner_image) {
      try {
        const userResponse = await axios.get(
          `/api/users/upload/banner/${user.value.id}`,
          {
            responseType: 'blob', // Treat the response as a binary file
            withCredentials: true, // Include credentials such as cookies or client certificates
          }
        );
        const blobUrl = URL.createObjectURL(userResponse.data);
        userBanner.value = blobUrl;
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.log(error);
  }

  loadingUser.value = false;
  createdPins()
});

const bgCreated = ref('border-black');
const bgSaved = ref('border-black');
const bgLiked = ref('border-black');

const showCreated = ref(false);
const showSaved = ref(false);
const showLiked = ref(false)

const showEditModalBanner = ref(false)

async function createdPins() {
  showSaved.value = false;
  showLiked.value = false;
  showCreated.value = true;
  bgSaved.value = 'border-black';
  bgLiked.value = 'border-black';
  bgCreated.value = 'border-red-600';
}

async function savedPins() {
  showSaved.value = true;
  showCreated.value = false;
  showLiked.value = false;
  bgCreated.value = 'border-black';
  bgLiked.value = 'border-black';
  bgSaved.value = 'border-red-600';
}

async function likedPins() {
  showLiked.value = true;
  showCreated.value = false;
  showSaved.value = false;
  bgCreated.value = 'border-black';
  bgSaved.value = 'border-black';
  bgLiked.value = 'border-red-600';
}

// Function to go back to the previous page in history
const goBack = () => {
  router.back();
};


async function editProfile() {
  let newUsername = null
  let description = null
  let instagram = null
  let tiktok = null
  let telegram = null
  let pinterest = null
  if (editUsername.value.trim()) {
    newUsername = editUsername.value.trim()
  }
  if (editDescription.value.trim()) {
    description = editDescription.value.trim()
  }
  if (editInstagram.value.trim()) {
    instagram = editInstagram.value.trim()
  }
  if (editTiktok.value.trim()) {
    tiktok = editTiktok.value.trim()
  }
  if (editTelegram.value.trim()) {
    telegram = editTelegram.value.trim()
  }
  if (editPinterest.value.trim()) {
    pinterest = editPinterest.value.trim()
  }
  try {
    const response = await axios.patch('/api/users/information',
      {
        username: newUsername,
        description: description,
        instagram: instagram,
        tiktok: tiktok,
        telegram: telegram,
        pinterest: pinterest
      },  // Data to be sent in the request body
      {
        withCredentials: true  // Include credentials like cookies or authorization headers
      }
    );
    user.value = response.data

    showEditModal.value = false


  } catch (error) {
    console.error(error)
  }
}

const showEditModalImage = ref(false)

async function editProfileImage() {
  if (imageFile.value) {
    try {
      const formData = new FormData();
      formData.append('file', imageFile.value);

      const response = await axios.patch(
        `/api/users/upload/profile`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          withCredentials: true, // Include credentials like cookies or authorization headers
        }
      );

      imageFile.value = null
      imagePreview.value = null

      try {
        const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
        const blobUrl = URL.createObjectURL(userResponse.data);
        userImage.value = blobUrl;
      } catch (error) {
        console.error(error);
      }

      showEditModalImage.value = false

    } catch (error) {
      console.log(error)
    }
  }
}

async function editBannerImage() {
  if (bannerImageFile.value) {
    try {
      const formData = new FormData();
      formData.append('file', bannerImageFile.value);

      const response = await axios.patch(
        `/api/users/upload/banner`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          withCredentials: true, // Include credentials like cookies or authorization headers
        }
      );

      bannerImageFile.value = null
      bannerImagePreview.value = null

      try {
        const userResponse = await axios.get(
          `/api/users/upload/banner/${user.value.id}`,
          {
            responseType: 'blob', // Treat the response as a binary file
            withCredentials: true, // Include credentials such as cookies or client certificates
          }
        );
        const blobUrl = URL.createObjectURL(userResponse.data);
        userBanner.value = blobUrl;
      } catch (error) {
        console.error(error);
      }

      showEditModalBanner.value = false

    } catch (error) {
      console.log(error)
    }
  }
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

function handleBannerUpload(event) {
  const file = event.target.files[0];
  if (file) {
    bannerImageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      bannerImagePreview.value = e.target.result; // Update the preview data
    };
    reader.readAsDataURL(file);
  }
}

const showEditButtons = ref(false)
</script>

<template>
  <transition name="fade" appear>
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <div class="flex flex-col items-center justify-center gap-5">
        <!-- <DotLottieVue class="ml-4"
          style="height: 210px; width: 250px; filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.8)) drop-shadow(0 0 30px rgba(255, 255, 255, 0.6));"
          autoplay loop src="https://lottie.host/283cf83b-92ee-4d44-93d9-d62849b90da3/LCwNUy8wJT.lottie" />

        <p class="text-white text-3xl font-cursive mb-2"
          style="text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 255, 255, 0.6);">
          Create your first pin!
        </p> -->
        <div class="space-y-7 mt-2">
          <!-- Title Field -->
          <div>
            <label for="username" class="text-white text-xl">username</label>
            <input v-model="editUsername" type="text" name="username" id="username" autocomplete="off"
              class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[400px] py-4 px-5 focus:ring-white focus:border-white"
              style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
          </div>
          <!-- Description Field -->
          <div>
            <label for="description" class="text-white text-xl">description</label>
            <textarea v-model="editDescription" name="description" id="description"
              style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);"
              class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[400px] py-4 px-5 focus:ring-white focus:border-white"></textarea>
          </div>
          <!-- Href Field -->
        </div>


        <div class="flex flex-row items-center justify-center space-x-2">
          <i class="pi pi-instagram text-4xl text-white"></i>
          <input v-model="editInstagram" type="url" name="href-instagram" id="instagram" autocomplete="off"
            class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[300px] py-4 px-5 focus:ring-white focus:border-white"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div class="flex flex-row items-center justify-center space-x-2">
          <i class="pi pi-tiktok text-4xl text-white"></i>
          <input v-model="editTiktok" type="url" name="href-tiktok" id="tiktok" autocomplete="off"
            class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[300px] py-4 px-5 focus:ring-white focus:border-white"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div class="flex flex-row items-center justify-center space-x-2">
          <i class="pi pi-telegram text-4xl text-white"></i>
          <input v-model="editTelegram" type="url" name="href-telegram" id="telegram" autocomplete="off"
            class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[300px] py-4 px-5 focus:ring-white focus:border-white"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div class="flex flex-row items-center justify-center space-x-2">
          <i class="pi pi-pinterest text-4xl text-white"></i>
          <input v-model="editPinterest" type="url" name="href-pinterest" id="pinterest" autocomplete="off"
            class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[300px] py-4 px-5 focus:ring-white focus:border-white"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>



        <div clas="flex space-x-4">
          <button @click="editProfile"
            class="mx-10 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Save
          </button>
          <button @click="showEditModal = false"
            class="mx-2 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>
        </div>
      </div>

      <!-- Centered Button with Glow -->
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showEditModalImage" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <div class="flex flex-col items-center justify-center gap-5">
        <div class="flex flex-col items-center">
          <label for="image" class="block mb-2 text-sm font-medium text-white">Your Profile Image</label>
          <input type="file" id="image" name="image" accept="image/*" @change="handleImageUpload"
            class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
          <img v-if="imagePreview" :src="imagePreview"
            class="mt-2 rounded-full w-32 h-32 object-cover border-4 border-black" alt="Image Preview"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div clas="flex space-x-4">
          <button @click="editProfileImage"
            class="mx-5 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Update
          </button>
          <button @click="showEditModalImage = false"
            class="mx-2 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>

        </div>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showEditModalBanner" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <div class="flex flex-col items-center justify-center gap-5">
        <div class="flex flex-col items-center">
          <label for="image" class="block mb-2 text-sm font-medium text-white">Your Banner Image</label>
          <input type="file" id="image" name="image" accept="image/*" @change="handleBannerUpload"
            class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
          <img v-if="bannerImagePreview" :src="bannerImagePreview"
            class="mt-2 rounded-2xl h-[400px] w-[600px] object-cover" alt="Image Preview"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div clas="flex space-x-4">
          <button @click="editBannerImage"
            class="mx-5 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Update
          </button>
          <button @click="showEditModalBanner = false"
            class="mx-2 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>

        </div>
      </div>
    </div>
  </transition>
  <div class="flex items-center justify-center mt-5">
    <ClipLoader v-if="loadingUser" :color="color" :size="size" class="" />
    <div v-else>
      <div class="flex flex-col items-center">
        <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="relative">
          <i v-if="user.verified" class="absolute top-0 left-28 pi pi-verified text-2xl"></i>
          <img v-if="userImage" :src="userImage" alt="Profile Picture"
            class="rounded-full w-32 h-32 object-cover border-4 border-black" />
        </div>
        <p v-if="user" class="mt-4 text-lg font-semibold">{{ user.username }}</p>
        <button v-if="canEditProfile" @click="showEditButtons = !showEditButtons" class="px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">Edit profile</button>
        <div v-if="showEditButtons" class="mt-4 space-x-2">
          <button v-if="canEditProfile" @click="showEditModal = true"
          class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            information
          </button>
          <button v-if="canEditProfile" @click="showEditModalImage = true"
          class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            profile image
          </button>
          <button v-if="canEditProfile" @click="showEditModalBanner = true"
          class="hover:-translate-y-2 px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">
            banner
          </button>
        </div>
        <p v-if="user && user.description"
          class="text-center mt-4 text-lg font-semibold  truncate-wrap mx-auto w-[400px]">{{ user.description }}</p>
        <div class="flex flex-row gap-2 text-4xl">
          <a v-if="user && user.instagram" :href="user.instagram">
            <i class="pi pi-instagram"></i>
          </a>
          <a v-if="user && user.tiktok" :href="user.tiktok">
            <i class="pi pi-tiktok"></i>
          </a>
          <a v-if="user && user.telegram" :href="user.telegram">
            <i class="pi pi-telegram"></i>
          </a>
          <a v-if="user && user.pinterest" :href="user.pinterest">
            <i class="pi pi-pinterest"></i>
          </a>
        </div>
      </div>
      <div class="flex items-center mt-6 justify-center space-x-4">
        <button @click="createdPins"
          :class="`px-6 py-2 text-black border-b-4 ${bgCreated} transition hover:border-red-600`">
          Созданные
        </button>
        <button @click="savedPins"
          :class="`px-6 py-2 text-black border-b-4 ${bgSaved} transition hover:border-red-600`">
          Сохраненные
        </button>
        <button @click="likedPins"
          :class="`px-6 py-2 text-black border-b-4 ${bgLiked} transition hover:border-red-600`">
          Понравившиеся
        </button>
      </div>
    </div>
    <div v-if="userBanner" class="flex items-center mt-6 ml-5">
      <img v-if="userBanner" :src="userBanner" alt="Profile Picture"
        class="rounded-2xl h-[400px] w-[600px] object-cover" />
    </div>
  </div>
  <CreatedPins v-if="showCreated" :user_id="user.id" :auth_user_id="auth_user_id" />
  <SavedPins v-if="showSaved" :user_id="user.id" :auth_user_id="auth_user_id" />
  <LikedPins v-if="showLiked" :user_id="user.id" />
</template>


<style scoped>
/* Define transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  /* Internet Explorer 10+ */
  scrollbar-width: none;
  /* Firefox */
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
}

.fade-in-animation {
  opacity: 0;
  transform: scale(0.95);
  animation: fadeIn 0.3s ease-in-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>