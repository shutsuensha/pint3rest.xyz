<script setup>
import { onMounted, ref, onActivated, onDeactivated } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import CreatedPins from '@/components/Auth/CreatedPins.vue';
import SavedPins from '@/components/Auth/SavedPins.vue';
import LikedPins from '@/components/Auth/LikedPins.vue';
import FollowersSection from '@/components/Auth/FollowersSection.vue';
import FollowingSection from '@/components/Auth/FollowingSection.vue';

const isLoading = ref(false);
const progress = ref(0);

const activeTab = ref('created');


const sendingMessage = ref(false)


const updateInformation = ref(false)


onActivated(() => {
  if (user.value) {
    if (canEditProfile.value) {
      document.title = 'pinterest.xyz / me ' + user.value.username
    } else {
      document.title = 'pinterest.xyz / user ' + user.value.username
    }
  }
});


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

const cntUserFollowers = ref(null)
const cntUserFollowing = ref(null)
const checkUserFollow = ref(null)
const checkUserChat = ref(null)

const showFollowers = ref(false)
const showFollowing = ref(false)


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

  // Start the loading process
  isLoading.value = true;
  progress.value = 0;

  try {
    const response = await axios.get(`/api/users/user_username/${username}`);
    user.value = response.data;
    canEditProfile.value = auth_user_id.value === user.value.id;

    // Update progress after fetching user data
    progress.value = 20;

    if (canEditProfile.value) {
      document.title = 'pinterest.xyz / me ' + user.value.username;
    } else {
      document.title = 'pinterest.xyz / user ' + user.value.username;
    }

    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;

      // Update progress after fetching user image
      progress.value = 40;
    } catch (error) {
      console.error(error);
    }
  } catch (error) {
    router.push('/not-found');
  }

  try {
    if (user.value.banner_image) {
      try {
        const userResponse = await axios.get(
          `/api/users/banner/upload/${user.value.id}`,
          {
            responseType: 'blob', // Treat the response as a binary file
            withCredentials: true, // Include credentials such as cookies or client certificates
          }
        );
        const blobUrl = URL.createObjectURL(userResponse.data);
        userBanner.value = blobUrl;

        // Update progress after fetching banner image
        progress.value = 60;
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.log(error);
  }

  try {
    const response = await axios.get(`/api/subscription/followers/cnt/${user.value.id}`, { withCredentials: true });
    cntUserFollowers.value = response.data;

    // Update progress after fetching followers count
    progress.value = 70;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/following/cnt/${user.value.id}`, { withCredentials: true });
    cntUserFollowing.value = response.data;

    // Update progress after fetching following count
    progress.value = 80;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/check_user_follow/${user.value.id}`, { withCredentials: true });
    checkUserFollow.value = response.data;

    // Update progress after checking user follow status
    progress.value = 90;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/messages/check_chat/${user.value.id}`, { withCredentials: true });
    checkUserChat.value = response.data;

    // Update progress after checking user follow status
    progress.value = 95;
  } catch (error) {
    console.error(error);
  }

  // Final progress update and stop loading
  loadingUser.value = false;
  isLoading.value = false;
  progress.value = 100;
  createdPins();
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
  updateInformation.value = true

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

    updateInformation.value = false

  } catch (error) {
    console.error(error)
  }
}

const showEditModalImage = ref(false)

const updateProfileImage = ref(false)

async function editProfileImage() {
  if (imageFile.value) {
    updateProfileImage.value = true
    try {
      const formData = new FormData();
      formData.append('file', imageFile.value);

      const response = await axios.post(
        `/api/users/upload/${auth_user_id.value}`,
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
      updateProfileImage.value = false

    } catch (error) {
      console.log(error)
    }
  }
}

const updateProfileBanner = ref(false)

async function editBannerImage() {
  if (bannerImageFile.value) {
    updateProfileBanner.value = true
    try {
      const formData = new FormData();
      formData.append('file', bannerImageFile.value);

      const response = await axios.post(
        `/api/users/banner/upload/${auth_user_id.value}`,
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
          `/api/users/banner/upload/${auth_user_id.value}`,
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
      updateProfileBanner.value = false

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

async function follow() {
  try {
    const response = await axios.post(`/api/subscription/${user.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = true
  cntUserFollowers.value += 1
}

async function unfollow() {
  try {
    const response = await axios.delete(`/api/subscription/${user.value.id}`, { withCredentials: true })
  } catch (error) {
    console.log(error)
  }
  checkUserFollow.value = false
  cntUserFollowers.value -= 1
}

const openSendMessage = ref(false)
const messageContent = ref('')

async function sendMessage() {
  sendingMessage.value = true
  try {
    const response = await axios.post('/api/messages/', {
      content: messageContent.value,
      to_user_id: user.value.id
    }, { withCredentials: true })
    messageContent.value = ''
    openSendMessage.value = false
    sendingMessage.value = true
  } catch (error) {
    console.error(error)
  }
  checkUserChat.value = true
  redirectToNewChat()
}

async function redirectToNewChat() {
  try {
    const response = await axios.get(`/api/messages/get_chat/${user.value.id}`, { withCredentials: true });
    router.push(`/messages?chat_id=${response.data}&new_chat=true`);
  } catch (error) {
    console.error(error);
  }
}

async function redirectToChat() {
  try {
    const response = await axios.get(`/api/messages/get_chat/${user.value.id}`, { withCredentials: true });
    router.push(`/messages?chat_id=${response.data}`);
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <transition name="fade" appear>
    <div v-if="openSendMessage" class="fixed inset-0 bg-black bg-opacity-20 z-40 p-6">

      <div class="flex justify-center items-center min-h-screen">
        <div v-if="!sendingMessage"
          class="flex flex-col gap-2  bg-gray-200 h-auto max-h-[600px] text-2xl rounded-3xl  z-50 w-[800px] overflow-y-auto py-2 items-center">

          <h1 class="text-center text-6xl text-black mt-4">Write Message</h1>
          <textarea v-model="messageContent" name="messageContent" id="messageContent" style="height: 200px;"
            class=" cursor-pointer  text-black text-3xl rounded-3xl block w-3/4 py-10 px-10 focus:ring-black  bg-white focus:border-4 focus:border-white"></textarea>

          <button @click="sendMessage"
            class="my-5 w-[400px] py-3 bg-white text-black font-semibold rounded-3xl hover:bg-indigo-300 transition duration-200">
            Send
          </button>
        </div>
        <div v-if="sendingMessage"
          class="flex flex-col gap-2  bg-gray-200 h-auto max-h-[600px] text-2xl rounded-3xl  z-50 w-[800px] overflow-y-auto py-20 items-center">

          <ClipLoader :color="color" :size="size" class="" />
        </div>
      </div>

      <i @click="openSendMessage = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>
  <div v-if="isLoading"
    class="fixed top-0 left-0 h-1 bg-purple-500 transition-all ease-in-out duration-300 z-50 rounded-r-full"
    :style="{ width: `${progress}%` }">
  </div>
  <transition name="fade" appear>
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">


      <ClipLoader v-if="updateInformation" color="white" :size="size"
        class="flex flex-col items-center justify-center text-center min-h-screen" />

      <div v-if="!updateInformation" class="flex flex-col items-center justify-center gap-5">

        <div class="space-y-7 mt-2">
          <div>
            <label for="username" class="text-white text-xl">username</label>
            <input v-model="editUsername" type="text" name="username" id="username" autocomplete="off"
              class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[400px] py-4 px-5 focus:ring-white focus:border-white"
              style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
          </div>

          <div>
            <label for="description" class="text-white text-xl">description</label>
            <textarea v-model="editDescription" name="description" id="description"
              style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);"
              class="hover:bg-black hover:text-white transition duration-300  cursor-pointer  border border-white bg-transparent  text-white text-sm rounded-xl block w-[400px] py-4 px-5 focus:ring-white focus:border-white"></textarea>
          </div>
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
          <button @click="showEditModal = false"
            class="ml-10 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>
          <button @click="editProfile"
            class="ml-4 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Save
          </button>
        </div>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showEditModalImage" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <ClipLoader v-if="updateProfileImage" color="white" :size="size"
        class="flex flex-col items-center justify-center text-center" />

      <div v-if="!updateProfileImage" class="flex flex-col items-center justify-center gap-5">
        <div class="flex flex-col items-center">
          <label for="image" class="block mb-2 text-sm font-medium text-white">Your Profile Image</label>
          <input type="file" id="image" name="image" accept="image/*" @change="handleImageUpload"
            class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
          <img v-if="imagePreview" :src="imagePreview"
            class="mt-2 rounded-full w-32 h-32 object-cover border-4 border-black" alt="Image Preview"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div clas="flex space-x-4">
          <button @click="showEditModalImage = false"
            class="mx-2 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>

          <button @click="editProfileImage"
            class="mx-5 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Update
          </button>
        </div>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showEditModalBanner" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">

      <!-- Lottie Animation -->

      <ClipLoader v-if="updateProfileBanner" color="white" :size="size"
      class="flex flex-col items-center justify-center text-center min-h-screen" />

      <div v-if="!updateProfileBanner" class="flex flex-col items-center justify-center gap-5">
        <div class="flex flex-col items-center">
          <label for="image" class="block mb-2 text-sm font-medium text-white">Your Banner Image</label>
          <input type="file" id="image" name="image" accept="image/*" @change="handleBannerUpload"
            class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
          <img v-if="bannerImagePreview" :src="bannerImagePreview"
            class="mt-2 rounded-2xl h-[400px] w-[600px] object-cover" alt="Image Preview"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
        </div>
        <div clas="flex space-x-4">
          <button @click="showEditModalBanner = false"
            class="mx-2 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Cancel
          </button>
          <button @click="editBannerImage"
            class="mx-5 w-[100px] py-3 bg-white text-black font-semibold rounded-3xl shadow-3xl hover:bg-black hover:text-white transition duration-300 ease-in-out"
            style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);">
            Update
          </button>

        </div>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowersSection :user_id="user.id" :cntUserFollowers="cntUserFollowers" />
      <i @click="showFollowers = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-40 p-6">
      <FollowingSection :user_id="user.id" :cntUserFollowing="cntUserFollowing" />
      <i @click="showFollowing = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
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
            class="rounded-full w-32 h-32 object-cover border-4 border-white" />
        </div>
        <p v-if="user" class="mt-4 text-lg font-semibold">{{ user.username }}</p>
        <button v-if="canEditProfile" @click="showEditButtons = !showEditButtons"
          class="px-6 py-3 bg-gray-300 text-black font-semibold rounded-3xl transition hover:bg-black hover:text-white">Edit
          profile</button>
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
        <p v-if="user && user.description" class="text-center mt-4 text-lg truncate-wrap mx-auto w-[400px]">{{
          user.description }}</p>
        <div class="flex flex-row gap-2 text-4xl text-red-600">
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
        <div class="flex gap-4">
          <a v-show="cntUserFollowers > 0" @click="showFollowers = true"
            class=" text-black cursor-pointer hover:underline ">
            {{ cntUserFollowers }} follower
          </a>
          <a v-show="cntUserFollowing > 0" @click="showFollowing = true"
            class=" text-black cursor-pointer hover:underline">
            {{ cntUserFollowing }} following
          </a>
        </div>
        <div class="flex flex-row gap-4">
          <button v-if="!canEditProfile && !checkUserFollow" @click="follow"
            class="px-6 py-3 bg-red-300 text-black  rounded-3xl transition hover:bg-red-500 hover:text-white">
            Follow
          </button>
          <button v-if="!canEditProfile && checkUserFollow" @click="unfollow"
            class="px-6 py-3 bg-red-300 text-black  rounded-3xl transition hover:bg-red-500 hover:text-white">
            Unfollow
          </button>
          <button v-if="!canEditProfile && !checkUserChat" @click="openSendMessage = true"
            class="px-6 py-3 bg-gray-300 text-black  rounded-3xl transition hover:bg-black hover:text-white">
            Message
          </button>
          <button v-if="!canEditProfile && checkUserChat" @click="redirectToChat"
            class="px-6 py-3 bg-gray-300 text-black  rounded-3xl transition hover:bg-black hover:text-white">
            Go to Chat
          </button>
        </div>
      </div>
      <div class="flex items-center mt-6 justify-center space-x-4">
        <button @click="createdPins(); activeTab = 'created'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border"
          :class="{ 'active scale-105': activeTab === 'created' }">
          Created
        </button>

        <button @click="savedPins(); activeTab = 'saved'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border"
          :class="{ 'active scale-105': activeTab === 'saved' }">
          Saved
        </button>

        <button @click="likedPins(); activeTab = 'liked'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border"
          :class="{ 'active scale-105': activeTab === 'liked' }">
          Liked
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
.animated-border {
  position: relative;
  transition: color 0.3s ease-in-out, transform 0.2s ease-out;
}

.animated-border::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: red;
  transition: width 0.3s ease-out, transform 0.3s ease-out;
  transform: translateX(-50%);
}

.active::after {
  width: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.animated-border:hover {
  color: red;
  transform: scale(1.05);
}

.animated-border:hover::after {
  width: 100%;
  left: 50%;
  transform: translateX(-50%);
}



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





.loader {
  width: 48px;
  height: 48px;
  display: inline-block;
  position: relative;
  border-width: 3px 2px 3px 2px;
  border-style: solid dotted solid dotted;
  border-color: #c50000 rgba(10, 255, 39, 0.3) #1c589e rgba(255, 101, 101, 0.836);
  border-radius: 50%;
  box-sizing: border-box;
  animation: 1s rotate linear infinite;
}

.loader:before,
.loader:after {
  content: '';
  top: 0;
  left: 0;
  position: absolute;
  border: 10px solid transparent;
  border-bottom-color: #a309d27a;
  transform: translate(-10px, 19px) rotate(-35deg);
}

.loader:after {
  border-color: #de3500 #670e6d00 #7b090900 #0000;
  transform: translate(32px, 3px) rotate(-35deg);
}

@keyframes rotate {
  100% {
    transform: rotate(360deg)
  }
}
</style>