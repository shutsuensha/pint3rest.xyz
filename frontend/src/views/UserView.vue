<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import CreatedPins from '@/components/Auth/CreatedPins.vue';
import SavedPins from '@/components/Auth/SavedPins.vue';

const color = ref('red');
const size = ref('100px');

const route = useRoute();
const router = useRouter(); // Add useRouter to access the router instance

const loadingUser = ref(true);

const username = route.params.username;
const user = ref(null);
const userImage = ref(null);

const auth_user_id = ref(null);

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

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
    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;
      loadingUser.value = false;
    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    console.log(error);
  }
});

const bgCreated = ref('border-gray-200');
const bgSaved = ref('border-gray-200');

const showCreated = ref(false);
const showSaved = ref(false);

async function createdPins() {
  showSaved.value = false;
  showCreated.value = true;
  bgSaved.value = 'border-gray-200';
  bgCreated.value = 'border-red-600';
}

async function savedPins() {
  showSaved.value = true;
  showCreated.value = false;
  bgCreated.value = 'border-gray-200';
  bgSaved.value = 'border-red-600';
}

// Function to go back to the previous page in history
const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="flex items-center justify-center mt-20">
    <ClipLoader v-if="loadingUser" :color="color" :size="size" class="" />
    <div v-else class="flex flex-col items-center">
      <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <img v-if="userImage" :src="userImage" alt="Profile Picture" class="rounded-full w-32 h-32 object-cover" />
      <p v-if="user" class="mt-4 text-lg font-semibold text-gray-700">@{{ user.username }}</p>
      <div class="flex mt-4 space-x-4">
        <button @click="createdPins" :class="`px-6 py-2 text-black border-b-4 ${bgCreated} transition hover:border-red-600`">
          Созданные
        </button>
        <button @click="savedPins" :class="`px-6 py-2 text-black border-b-4 ${bgSaved} transition hover:border-red-600`">
          Сохраненные
        </button>
      </div>
    </div>
  </div>
  <CreatedPins v-if="showCreated" :user_id="user.id" />
  <SavedPins v-if="showSaved" :user_id="user.id" :auth_user_id="auth_user_id" />
</template>
