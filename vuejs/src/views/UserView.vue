<script setup>
import { onMounted, ref, onActivated, onDeactivated, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import CreatedPins from '@/components/Auth/CreatedPins.vue';
import SavedPins from '@/components/Auth/SavedPins.vue';
import LikedPins from '@/components/Auth/LikedPins.vue';
import Boards from '@/components/Auth/Boards.vue';
import FollowersSection from '@/components/Auth/FollowersSection.vue';
import FollowingSection from '@/components/Auth/FollowingSection.vue';

import { useToast } from "vue-toastification";
const toast = useToast();

import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();

import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

import SearchBar from '@/components/Auth/SearchBar.vue';

const isLoading = ref(true);

const activeTab = ref('created');


const sendingMessage = ref(false)


const updateInformation = ref(false)


const showHeader = ref(false)
const observerTargetHeader = ref(null)
let observerHeader = null

observerHeader = new IntersectionObserver(
  ([entry]) => {
    showHeader.value = !entry.isIntersecting
  },
  {
    threshold: 1,
    rootMargin: '-20px 0px 0px 0px',
  }
)

watch(observerTargetHeader, (newVal) => {
  if (observerTargetHeader.value) {
    observerHeader.observe(observerTargetHeader.value)
  }
})



const showHeaderButtons = ref(false)
const observerTargetHeaderButtons = ref(null)
let observerHeaderButtons = null

observerHeaderButtons = new IntersectionObserver(
  ([entry]) => {
    showHeaderButtons.value = !entry.isIntersecting
  },
  {
    threshold: 0.05,
    rootMargin: '30px 0px 0px 0px',
  }
)

watch(observerTargetHeaderButtons, (newVal) => {
  if (observerTargetHeaderButtons.value) {
    observerHeaderButtons.observe(observerTargetHeaderButtons.value)
  }
})


onActivated(() => {
  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest`; // Если есть непрочитанные уведомления
  } else {
    document.title = 'Pinterest'; // Если уведомлений нет
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

const userAlreadyExistsError = ref(false)




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

  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest`; // Если есть непрочитанные уведомления
  } else {
    document.title = 'Pinterest'; // Если уведомлений нет
  }

  try {
    const response = await axios.get(`/api/users/user_username/${username}`);
    user.value = response.data;
    canEditProfile.value = auth_user_id.value === user.value.id;


    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;

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

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/following/cnt/${user.value.id}`, { withCredentials: true });
    cntUserFollowing.value = response.data;
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/subscription/check_user_follow/${user.value.id}`, { withCredentials: true });
    checkUserFollow.value = response.data;

  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get(`/api/messages/check_chat/${user.value.id}`, { withCredentials: true });
    checkUserChat.value = response.data;

  } catch (error) {
    console.error(error);
  }

  loadingUser.value = false;
  isLoading.value = false;

  createdPins();
});


const formatLink = (url) => {
  return url.replace(/^https?:\/\//, '');
};


const showCreated = ref(false);
const showSaved = ref(false);
const showLiked = ref(false)
const showBoards = ref(false)

const showEditModalBanner = ref(false)

async function createdPins() {
  showSaved.value = false;
  showLiked.value = false;
  showCreated.value = true;
  showBoards.value = false
}

async function savedPins() {
  showSaved.value = true;
  showCreated.value = false;
  showLiked.value = false;
  showBoards.value = false
}

async function likedPins() {
  showLiked.value = true;
  showCreated.value = false;
  showSaved.value = false;
  showBoards.value = false

}

async function boards() {
  showLiked.value = false;
  showCreated.value = false;
  showSaved.value = false;
  showBoards.value = true

}

// Function to go back to the previous page in history
const goBack = () => {
  router.back();
};

const userHasTestAcc = ref(false)

async function editProfile() {

  let newUsername = null
  let description = null
  let instagram = null
  let tiktok = null
  let telegram = null
  let pinterest = null

  let atLeastOneField = false

  if (editUsername.value.trim()) {
    newUsername = editUsername.value.trim()
    atLeastOneField = true
  }
  if (editDescription.value.trim()) {
    description = editDescription.value.trim()
    atLeastOneField = true
  }
  if (editInstagram.value.trim()) {
    instagram = editInstagram.value.trim()
    atLeastOneField = true
  }
  if (editTiktok.value.trim()) {
    tiktok = editTiktok.value.trim()
    atLeastOneField = true
  }
  if (editTelegram.value.trim()) {
    telegram = editTelegram.value.trim()
    atLeastOneField = true
  }
  if (editPinterest.value.trim()) {
    pinterest = editPinterest.value.trim()
    atLeastOneField = true
  }

  if (atLeastOneField == true) {
    updateInformation.value = true
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
      if (error.response.status === 409) {
        updateInformation.value = false
        userAlreadyExistsError.value = true
      }
      if (error.response.status === 403) {
        updateInformation.value = false
        userHasTestAcc.value = true
      }
    }
  }
}

const showModal = ref(false)


const showEditModalImage = ref(false)

const updateProfileImage = ref(false)

const errorUpdateProfileImage = ref(false)

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
      if (error.response.status === 415) {
        imageFile.value = null
        imagePreview.value = null
        updateProfileImage.value = false
        errorUpdateProfileImage.value = true
      }
    }
  }
}

const updateProfileBanner = ref(false)

const errorUpdateBannerImage = ref(false)

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
      if (error.response.status === 415) {
        bannerImageFile.value = null
        bannerImagePreview.value = null
        updateProfileBanner.value = false
        errorUpdateBannerImage.value = true
      }
    }
  }
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

function handleBannerUpload(event) {
  const file = event.target.files[0];


  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp'];


  if (file) {

    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid image file (.jpg, .jpeg, .gif, .webp, .png, .bmp).', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
      return;
    }

    const minWidth = 200;
    const minHeight = 300;

    const img = new Image();
    img.onload = () => {
      if (img.width < minWidth || img.height < minHeight) {
        toast.warning(`Image must be at least ${minWidth}x${minHeight}.`, {
          position: "top-center",
          bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
        });
        return;
      }

      bannerImageFile.value = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        bannerImagePreview.value = e.target.result; // Update the preview data
      };
      reader.readAsDataURL(file);

    };
    img.src = URL.createObjectURL(file);
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
  if (messageContent.value.trim()) {
    sendingMessage.value = true
    try {
      const response = await axios.post('/api/messages/', {
        content: messageContent.value.trim(),
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
    <div v-if="openSendMessage" class="fixed inset-0 bg-black bg-opacity-50 z-50 p-6">

      <div class="ml-20 flex justify-center items-center min-h-screen" @click.self="openSendMessage = false">
        <div v-if="!sendingMessage"
          class="flex flex-col gap-2  bg-gray-200 h-auto max-h-[600px] text-2xl rounded-3xl  z-50 w-[800px] overflow-y-auto py-2 items-center">

          <h1 class="text-center text-6xl text-black mt-4 mb-4 ">Message to {{ user.username }}</h1>
          <textarea v-model="messageContent" name="messageContent" id="messageContentUser" style="height: 200px;"
            class=" cursor-pointer  text-black text-3xl rounded-3xl block w-3/4 py-10 px-10 focus:ring-black  bg-white focus:border-4 focus:border-white"></textarea>

          <button @click="sendMessage"
            class="my-5 w-[400px] py-3 bg-white text-black font-semibold rounded-3xl hover:bg-indigo-300 transition duration-200">
            Send
          </button>
        </div>
        <div v-if="sendingMessage"
          class="ml-20 flex flex-col gap-2  bg-gray-200 h-auto max-h-[600px] text-2xl rounded-3xl  z-50 w-[800px] overflow-y-auto py-20 items-center">

          <ClipLoader :color="color" :size="size" class="" />
        </div>
      </div>

      <i @click="openSendMessage = false"
        class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
        style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
    </div>
  </transition>
  <transition name="fade" appear>
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-6"
      @click.self="showEditModal = false">
      <!-- Модальное окно -->
      <div class="ml-20 bg-white rounded-3xl shadow-2xl max-w-lg w-full p-6 relative">

        <!-- Если идет обновление информации -->
        <ClipLoader v-if="updateInformation" color="#E60023" :size="size"
          class="flex flex-col items-center justify-center text-center min-h-[200px]" />

        <!-- Форма редактирования -->
        <div v-if="!updateInformation" class="flex flex-col items-stretch gap-6">
          <!-- Заголовок окна -->
          <h2 class="text-2xl font-semibold text-gray-900 text-center">
            Edit Profile
          </h2>

          <div class="space-y-6">
            <!-- Username Input -->
            <div>
              <label for="usernameEditUsername" class="block text-gray-700 text-lg mb-2">Username</label>
              <input v-model="editUsername" type="text" name="username" id="usernameEditUsername" autocomplete="off"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300" />
            </div>

            <!-- Description Input -->
            <div>
              <label for="descriptionEditUser" class="block text-gray-700 text-lg mb-2">Description</label>
              <textarea v-model="editDescription" name="description" id="descriptionEditUser" rows="4"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300 resize-none"></textarea>
            </div>
          </div>

          <!-- Социальные ссылки -->
          <div class="flex flex-col gap-4">
            <div class="flex items-center space-x-3">
              <i class="pi pi-instagram text-3xl text-gray-700"></i>
              <input v-model="editInstagram" type="url" name="href-instagram" id="instagram" autocomplete="off"
                placeholder="Instagram URL"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300" />
            </div>
            <div class="flex items-center space-x-3">
              <i class="pi pi-tiktok text-3xl text-gray-700"></i>
              <input v-model="editTiktok" type="url" name="href-tiktok" id="tiktok" autocomplete="off"
                placeholder="Tiktok URL"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300" />
            </div>
            <div class="flex items-center space-x-3">
              <i class="pi pi-telegram text-3xl text-gray-700"></i>
              <input v-model="editTelegram" type="url" name="href-telegram" id="telegram" autocomplete="off"
                placeholder="Telegram URL"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300" />
            </div>
            <div class="flex items-center space-x-3">
              <i class="pi pi-pinterest text-3xl text-gray-700"></i>
              <input v-model="editPinterest" type="url" name="href-pinterest" id="pinterest" autocomplete="off"
                placeholder="Pinterest URL"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-600 transition duration-300" />
            </div>
          </div>

          <!-- Кнопки управления -->
          <div class="flex justify-center items-center gap-4 mt-6">
            <button @click="showEditModal = false"
              class="w-28 py-2 border border-gray-300 rounded-full text-gray-700 font-semibold hover:bg-gray-100 transition duration-300">
              Cancel
            </button>
            <button @click="editProfile"
              class="w-28 py-2 rounded-full bg-red-600 text-white font-semibold hover:bg-red-700 transition duration-300">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>



  <transition name="fade" appear>
    <div v-if="showEditModalImage"
      class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-6"
      @click.self="showEditModalImage = false">
      <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-8 relative ml-20">
        <!-- Лоадер при обновлении -->
        <ClipLoader v-if="updateProfileImage" color="#E60023" :size="size"
          class="flex flex-col items-center justify-center text-center min-h-[150px]" />

        <!-- Форма редактирования изображения -->
        <div v-else class="flex flex-col items-center justify-center gap-5">
          <div class="flex flex-col items-center w-full">
            <label for="imageProfile" class="block mb-2 text-sm font-medium text-gray-700">
              Your Profile Image (.jpg, .jpeg, .gif, .webp, .png, .bmp)
            </label>
            <input type="file" id="imageProfile" name="image" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp"
              @change="handleImageUpload"
              class="block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500 transition duration-300" />
            <img v-if="imagePreview" :src="imagePreview" alt="Image Preview"
              class="mt-4 rounded-full w-32 h-32 object-cover border-4 border-gray-300"
              style="box-shadow: 0 0 15px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.6);" />
          </div>
          <div class="flex space-x-4 mt-4">
            <button @click="showEditModalImage = false"
              class="w-28 py-2 border border-gray-300 rounded-full text-gray-700 font-medium hover:bg-gray-100 transition duration-300">
              Cancel
            </button>
            <button @click="editProfileImage"
              class="w-28 py-2 rounded-full bg-red-600 text-white font-medium hover:bg-red-700 transition duration-300">
              Update
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showEditModalBanner"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      @click.self="showEditModalBanner = false">

      <!-- Lottie Animation (при обновлении) -->

      <!-- Контейнер модального окна -->
      <div class="bg-white rounded-xl shadow-lg p-6 max-w-lg w-full ml-20">

        <ClipLoader v-if="updateProfileBanner" color="#E60023" :size="size"
          class="flex flex-col items-center justify-center text-center min-h-[300px]" />

        <div v-else>
          <h2 class="text-center text-2xl font-bold text-gray-800 mb-4">Update Banner</h2>

          <!-- Блок загрузки изображения -->
          <div class="mb-6">
            <label for="imageBanner" class="block mb-2 text-sm font-semibold text-gray-700">
              Select Banner Image (.jpg, .jpeg, .gif, .webp, .png, .bmp)
            </label>
            <input type="file" id="imageBanner" name="image" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp"
              @change="handleBannerUpload"
              class="block w-full text-sm text-gray-900 border border-gray-300 rounded-md cursor-pointer bg-gray-50 focus:outline-none focus:ring focus:ring-red-500" />
            <img v-if="bannerImagePreview" :src="bannerImagePreview" class="mt-4 rounded-xl w-full object-cover"
              style="max-height: 300px;" alt="Image Preview" />
          </div>

          <!-- Кнопки управления -->
          <div class="flex justify-end space-x-4">
            <button @click="showEditModalBanner = false"
              class="px-4 py-2 bg-gray-100 text-gray-800 rounded-md hover:bg-gray-200 transition-colors">
              Cancel
            </button>
            <button @click="editBannerImage"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors">
              Update
            </button>
          </div>
        </div>

      </div>
    </div>
  </transition>


  <div v-if="userAlreadyExistsError"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full ml-20">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> User with that username already exists </h3>
          <button @click="userAlreadyExistsError = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  
  <div v-if="userHasTestAcc"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full ml-20">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> U cannot change username of test profile </h3>
          <button @click="userHasTestAcc = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>



  <div v-if="errorUpdateProfileImage"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full ml-20">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp,
            .png, .bmp </h3>
          <button @click="errorUpdateProfileImage = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>


  <div v-if="errorUpdateBannerImage"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full ml-20">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp,
            .png, .bmp </h3>
          <button @click="errorUpdateBannerImage = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>

  <transition name="fade" appear>
    <div v-if="showFollowers" class="fixed inset-0 bg-black bg-opacity-75 z-50 p-6">
      <div class="ml-20 flex justify-center items-center min-h-screen" @click.self="showFollowers = false">
        <FollowersSection :user_id="user.id" :cntUserFollowers="cntUserFollowers" />
        <i @click="showFollowers = false"
          class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
      </div>
    </div>
  </transition>

  <transition name="fade" appear>
    <div v-if="showFollowing" class="fixed inset-0 bg-black bg-opacity-75 z-50 p-6">
      <div class="ml-20 flex justify-center items-center min-h-screen" @click.self="showFollowing = false">
        <FollowingSection :user_id="user.id" :cntUserFollowing="cntUserFollowing" />
        <i @click="showFollowing = false"
          class="absolute right-20 top-20 pi pi-times text-white text-4xl cursor-pointer transition-transform duration-200 transform hover:scale-150"
          style="text-shadow: 0 0 20px rgba(255, 255, 255, 0.9), 0 0 40px rgba(255, 255, 255, 0.8), 0 0 80px rgba(255, 255, 255, 0.7);"></i>
      </div>
    </div>
  </transition>

  <SearchBar />

  <div class="flex items-center justify-center mt-20 ml-20">
    <ClipLoader v-if="isLoading" :color="color" :size="size" class="" />
    <div v-else>
      <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div v-if="!userBanner" class="flex flex-col items-center">
        <div class="relative">
          <i v-if="user && user.verified" class="absolute top-0 left-28 pi pi-verified text-2xl"></i>
          <img v-if="userImage" :src="userImage" alt="Profile Picture"
            class="rounded-full w-32 h-32 object-cover border-4 border-white" />
        </div>
        <p v-if="user" class="mt-4 text-3xl font-extrabold">{{ user.username }}</p>
        <div>
          <p v-if="user && user.description"
            class="description-box destext-center text-center mt-4 text-md mx-auto w-[500px]">
            {{ user.description }}
          </p>
          <span v-if="user && user.description && user.description.length > 200"
            class="text-black cursor-pointer justify-center flex font-extrabold" @click="showModal = true">
            More
          </span>

          <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-40 "
            @click.self="showModal = false">
            <div class="bg-white p-6 rounded-2xl w-[550px] relative h-[700px] ml-20">

              <button @click="showModal = false"
                class="absolute top-10 right-10 text-gray-500 hover:text-black">✕</button>

              <h2 class="text-4xl font-bold mb-4 mt-10 px-4 py-7">About user {{ user.username }}</h2>

              <div class="overflow-y-auto max-h-[400px] mt-10">

                <div class="space-y-6 text-md ml-4 mb-6">
                  <a v-if="user && user.instagram" :href="user.instagram" class="block w-full" target="_blank"
                    rel="noopener noreferrer">
                    <i class="pi pi-instagram mr-5"></i> {{ formatLink(user.instagram) }}
                  </a>
                  <a v-if="user && user.telegram" :href="user.telegram" class="block w-full" target="_blank"
                    rel="noopener noreferrer">
                    <i class="pi pi-telegram mr-5"></i> {{ formatLink(user.telegram) }}
                  </a>
                  <a v-if="user && user.tiktok" :href="user.tiktok" class="block w-full" target="_blank"
                    rel="noopener noreferrer">
                    <i class="pi pi-tiktok mr-5"></i> {{ formatLink(user.tiktok) }}
                  </a>
                  <a v-if="user && user.pinterest" :href="user.pinterest" class="block w-full" target="_blank"
                    rel="noopener noreferrer">
                    <i class="pi pi-pinterest mr-5"></i> {{ formatLink(user.pinterest) }}
                  </a>
                </div>

                <div class="space-y-6">
                  <a v-show="cntUserFollowers > 0" @click="showFollowers = true"
                    class=" text-black block w-full cursor-pointer hover:underline font-extrabold px-4">
                    <i class="pi pi-user-plus mr-5"></i> {{ cntUserFollowers }} follower
                  </a>

                  <a v-show="cntUserFollowing > 0" @click="showFollowing = true"
                    class=" text-black block w-full cursor-pointer hover:underline font-extrabold px-4">
                    <i class="pi pi-users mr-5"></i> {{ cntUserFollowing }} following
                  </a>
                </div>



                <p class="text-gray-800 whitespace-pre-line px-4 py-7 ">{{ user.description }}</p>

              </div>

              <!-- Follow Button -->
              <div class="absolute bottom-6 right-6">
                <button v-if="!canEditProfile && !checkUserFollow" @click="follow"
                  class="px-6 py-3 bg-red-500 text-white  rounded-2xl transition hover:bg-red-700 ">
                  Follow
                </button>
                <button v-if="!canEditProfile && checkUserFollow" @click="unfollow" :class="[
                  'px-6 py-3 rounded-2xl transition',
                  checkUserFollow ? 'bg-black text-white hover:bg-gray-900' : 'bg-red-500 text-white hover:bg-red-700'
                ]">
                  Unfollow
                </button>
              </div>

              <div class="absolute bottom-6 left-6">
                <button v-if="!canEditProfile && !checkUserChat" @click="openSendMessage = true"
                  class="px-6 py-3 bg-gray-300 hover:bg-gray-400 text-black  rounded-2xl transition  ">
                  Send Message
                </button>
                <button v-if="!canEditProfile && checkUserChat" @click="redirectToChat"
                  class="px-6 py-3 bg-gray-300 hover:bg-gray-400 text-black  rounded-2xl transition   ">
                  Go to Chat
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-row gap-2 text-md text-black max-w-[500px] mt-2">
          <a v-if="user && user.instagram" :href="user.instagram" class="truncate inline-block max-w-[100px]"
            target="_blank" rel="noopener noreferrer">
            <i class="pi pi-instagram"></i> {{ formatLink(user.instagram) }}
          </a>
          <a v-if="user && user.telegram" :href="user.telegram" class="truncate inline-block max-w-[100px]"
            target="_blank" rel="noopener noreferrer">
            <i class="pi pi-telegram"></i> {{ formatLink(user.telegram) }}
          </a>
          <a v-if="user && user.tiktok" :href="user.tiktok" class="truncate inline-block max-w-[100px]" target="_blank"
            rel="noopener noreferrer">
            <i class="pi pi-tiktok"></i> {{ formatLink(user.tiktok) }}
          </a>
          <a v-if="user && user.pinterest" :href="user.pinterest" class="truncate inline-block max-w-[100px]"
            target="_blank" rel="noopener noreferrer">
            <i class="pi pi-pinterest"></i> {{ formatLink(user.pinterest) }}
          </a>
        </div>
        <div class="flex gap-4 mt-4">
          <a v-show="cntUserFollowers > 0" @click="showFollowers = true"
            class=" text-black cursor-pointer hover:underline font-extrabold">
            {{ cntUserFollowers }} follower
          </a>
          <a v-show="cntUserFollowing > 0" @click="showFollowing = true"
            class=" text-black cursor-pointer hover:underline font-extrabold">
            {{ cntUserFollowing }} following
          </a>
        </div>
        <div v-if="!canEditProfile" class="flex flex-row gap-4 mt-4">
          <button v-if="!canEditProfile && !checkUserChat" @click="openSendMessage = true"
            class="px-6 py-3 bg-gray-300 hover:bg-gray-400 text-black  rounded-2xl transition  ">
            Send Message
          </button>
          <button v-if="!canEditProfile && checkUserChat" @click="redirectToChat"
            class="px-6 py-3 bg-gray-300 hover:bg-gray-400 text-black  rounded-2xl transition   ">
            Go to Chat
          </button>
          <button v-if="!canEditProfile && !checkUserFollow" @click="follow"
            class="px-6 py-3 bg-red-500 text-white  rounded-2xl transition hover:bg-red-700 ">
            Follow
          </button>
          <button v-if="!canEditProfile && checkUserFollow" @click="unfollow" :class="[
            'px-6 py-3 rounded-2xl transition',
            checkUserFollow ? 'bg-black text-white hover:bg-gray-900' : 'bg-red-500 text-white hover:bg-red-700'
          ]">
            Unfollow
          </button>
        </div>
        <div class="flex flex-col items-center">
          <!-- Основная кнопка для редактирования профиля -->
          <button v-if="canEditProfile" @click="showEditButtons = !showEditButtons"
            class="px-5 py-2 bg-red-600 text-white font-medium rounded-full transition duration-300 hover:bg-red-700 focus:outline-none">
            Edit Profile
          </button>

          <!-- Дополнительные кнопки для разных возможностей редактирования -->
          <div v-if="showEditButtons" class="mt-4 flex space-x-3">
            <button v-if="canEditProfile" @click="showEditModal = true"
              class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
              Information
            </button>
            <button v-if="canEditProfile" @click="showEditModalImage = true"
              class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
              Profile Image
            </button>
            <button v-if="canEditProfile" @click="showEditModalBanner = true"
              class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
              Banner
            </button>
          </div>
        </div>
      </div>
      <div v-if="userBanner" class="">
        <!-- Обёртка-сетка: в мобильном виде 1 колонка, на md и выше – 2 колонки -->
        <div class="grid grid-cols-2 gap-6 px-4 py-6">

          <div v-if="showHeader"
            class="fixed left-20 right-0 top-14 w-full z-20 bg-white bg-opacity-20 backdrop-blur-sm">
            <div class="ml-[140px] flex items-center gap-4">
              <!-- Аватар -->
              <img :src="userImage" alt="User Avatar" class="w-12 h-12 rounded-full object-cover" />

              <!-- Username -->
              <span class="text-2xl font-semibold text-black">
                {{ user.username }}
              </span>

              <div v-if="showHeaderButtons" class="ml-[195px] space-x-4">
                <button @click="createdPins(); activeTab = 'created'"
                  class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border  rounded-t-xl"
                  :class="{ 'active scale-105': activeTab === 'created' }">
                  Created
                </button>

                <button @click="savedPins(); activeTab = 'saved'"
                  class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border  rounded-t-2xl"
                  :class="{ 'active scale-105': activeTab === 'saved' }">
                  Saved
                </button>

                <button @click="likedPins(); activeTab = 'liked'"
                  class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border  rounded-t-2xl"
                  :class="{ 'active scale-105': activeTab === 'liked' }">
                  Liked
                </button>

                <button @click="boards(); activeTab = 'boards'"
                  class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border  rounded-t-2xl"
                  :class="{ 'active scale-105': activeTab === 'boards' }">
                  Boards
                </button>
              </div>
            </div>
          </div>

          <!-- Левая колонка: профиль пользователя -->
          <div ref="observerTargetHeader" class="ml-10">
            <!-- Аватарка с меткой проверки -->
            <div class="relative flex items-center">
              <i v-if="user && user.verified" class="absolute top-0 left-28 pi pi-verified text-2xl text-black"></i>
              <img v-if="userImage" :src="userImage" alt="Profile Picture"
                class="rounded-full w-32 h-32 object-cover" />
              <p v-if="user" class="ml-4 text-3xl font-extrabold text-gray-800">{{ user.username }}</p>
            </div>

            <div class="flex gap-4 mt-4 justify-left">
              <a v-show="cntUserFollowers > 0" @click="showFollowers = true"
                class="cursor-pointer hover:underline font-extrabold text-black">
                {{ cntUserFollowers }} follower
              </a>
              <a v-show="cntUserFollowing > 0" @click="showFollowing = true"
                class="cursor-pointer hover:underline font-extrabold text-black">
                {{ cntUserFollowing }} following
              </a>
            </div>

            <!-- Имя пользователя -->

            <!-- Описание + кнопка для открытия модального окна "подробнее" -->
            <div class="mt-4">
              <p v-if="user && user.description" class="description-box destext-center mt-4 text-md w-[500px]">
                {{ user.description }}
              </p>
              <span v-if="user && user.description && user.description.length > 200"
                class="text-black cursor-pointer flex justify-left font-extrabold mt-2" @click="showModal = true">
                More
              </span>
            </div>

            <!-- Модальное окно для детального описания -->
            <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-40"
              @click.self="showModal = false">
              <div class="bg-white p-6 rounded-2xl w-[550px] relative h-[700px]">
                <button @click="showModal = false" class="absolute top-4 right-4 text-gray-500 hover:text-black">
                  ✕
                </button>
                <h2 class="text-4xl font-bold mb-4 mt-10 text-center">
                  About user {{ user.username }}
                </h2>
                <div class="overflow-y-auto max-h-[400px] px-4 mt-10">
                  <div class="space-y-6 text-md mb-6">
                    <a v-if="user && user.instagram" :href="user.instagram" class="block" target="_blank"
                      rel="noopener noreferrer">
                      <i class="pi pi-instagram mr-3"></i> {{ formatLink(user.instagram) }}
                    </a>
                    <a v-if="user && user.telegram" :href="user.telegram" class="block" target="_blank"
                      rel="noopener noreferrer">
                      <i class="pi pi-telegram mr-3"></i> {{ formatLink(user.telegram) }}
                    </a>
                    <a v-if="user && user.tiktok" :href="user.tiktok" class="block" target="_blank"
                      rel="noopener noreferrer">
                      <i class="pi pi-tiktok mr-3"></i> {{ formatLink(user.tiktok) }}
                    </a>
                    <a v-if="user && user.pinterest" :href="user.pinterest" class="block" target="_blank"
                      rel="noopener noreferrer">
                      <i class="pi pi-pinterest mr-3"></i> {{ formatLink(user.pinterest) }}
                    </a>
                  </div>
                  <div class="space-y-6">
                    <a v-show="cntUserFollowers > 0" @click="showFollowers = true"
                      class="block cursor-pointer hover:underline font-extrabold">
                      <i class="pi pi-user-plus mr-3"></i> {{ cntUserFollowers }} follower
                    </a>
                    <a v-show="cntUserFollowing > 0" @click="showFollowing = true"
                      class="block cursor-pointer hover:underline font-extrabold">
                      <i class="pi pi-users mr-3"></i> {{ cntUserFollowing }} following
                    </a>
                  </div>
                  <p class="text-gray-800 whitespace-pre-line py-7">
                    {{ user.description }}
                  </p>
                </div>
                <!-- Кнопки взаимодействия (Follow / Unfollow и Send Message / Go to Chat) -->
                <div class="absolute bottom-6 right-6 flex flex-col space-y-3">
                  <button v-if="!canEditProfile && !checkUserFollow" @click="follow"
                    class="px-6 py-3 bg-red-500 text-white rounded-2xl transition hover:bg-red-700">
                    Follow
                  </button>
                  <button v-if="!canEditProfile && checkUserFollow" @click="unfollow"
                    :class="['px-6 py-3 rounded-2xl transition', checkUserFollow ? 'bg-black text-white hover:bg-gray-900' : 'bg-red-500 text-white hover:bg-red-700']">
                    Unfollow
                  </button>
                </div>
                <div class="absolute bottom-6 left-6 flex flex-col space-y-3">
                  <button v-if="!canEditProfile && !checkUserChat" @click="openSendMessage = true"
                    class="px-6 py-3 bg-neutral-200 hover:bg-neutral-300 text-black rounded-2xl transition">
                    Send Message
                  </button>
                  <button v-if="!canEditProfile && checkUserChat" @click="redirectToChat"
                    class="px-6 py-3 bg-neutral-200 hover:bg-neutral-300 text-black rounded-2xl transition">
                    Go to Chat
                  </button>
                </div>
              </div>
            </div>

            <!-- Социальные ссылки (под миниатюрной версией) -->
            <div class="flex flex-row gap-2 text-md text-black max-w-[500px] mt-2 justify-left">
              <a v-if="user && user.instagram" :href="user.instagram" class="truncate inline-block max-w-[100px]"
                target="_blank" rel="noopener noreferrer">
                <i class="pi pi-instagram"></i> {{ formatLink(user.instagram) }}
              </a>
              <a v-if="user && user.telegram" :href="user.telegram" class="truncate inline-block max-w-[100px]"
                target="_blank" rel="noopener noreferrer">
                <i class="pi pi-telegram"></i> {{ formatLink(user.telegram) }}
              </a>
              <a v-if="user && user.tiktok" :href="user.tiktok" class="truncate inline-block max-w-[100px]"
                target="_blank" rel="noopener noreferrer">
                <i class="pi pi-tiktok"></i> {{ formatLink(user.tiktok) }}
              </a>
              <a v-if="user && user.pinterest" :href="user.pinterest" class="truncate inline-block max-w-[100px]"
                target="_blank" rel="noopener noreferrer">
                <i class="pi pi-pinterest"></i> {{ formatLink(user.pinterest) }}
              </a>
            </div>


            <!-- Дополнительные кнопки действий (повтор для маленьких экранов) -->
            <div class="flex flex-row gap-4 mt-4 justify-left">
              <button v-if="!canEditProfile && !checkUserFollow" @click="follow"
                class="px-6 py-3 bg-red-500 text-white rounded-2xl transition hover:bg-red-700">
                Follow
              </button>
              <button v-if="!canEditProfile && checkUserFollow" @click="unfollow"
                :class="['px-6 py-3 rounded-2xl transition', checkUserFollow ? 'bg-black text-white hover:bg-gray-900' : 'bg-red-500 text-white hover:bg-red-700']">
                Unfollow
              </button>
              <button v-if="!canEditProfile && !checkUserChat" @click="openSendMessage = true"
                class="px-6 py-3 bg-neutral-200 hover:bg-neutral-300 text-black rounded-2xl transition">
                Send Message
              </button>
              <button v-if="!canEditProfile && checkUserChat" @click="redirectToChat"
                class="px-6 py-3 bg-neutral-200 hover:bg-neutral-300 text-black rounded-2xl transition">
                Go to Chat
              </button>
            </div>

            <!-- Контролы редактирования профиля (видны только администратору/владельцу профиля) -->
            <div class="flex flex-col items-start justify-start mt-6">
              <button v-if="canEditProfile" @click="showEditButtons = !showEditButtons"
                class="px-5 py-2 bg-red-600 text-white font-medium rounded-full transition duration-300 hover:bg-red-700 focus:outline-none">
                Edit Profile
              </button>
              <div v-if="showEditButtons" class="mt-4 flex space-x-3">
                <button v-if="canEditProfile" @click="showEditModal = true"
                  class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
                  Information
                </button>
                <button v-if="canEditProfile" @click="showEditModalImage = true"
                  class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
                  Profile Image
                </button>
                <button v-if="canEditProfile" @click="showEditModalBanner = true"
                  class="px-5 py-2 bg-gray-100 text-gray-800 font-medium rounded-full transition duration-300 hover:bg-gray-200 focus:outline-none">
                  Banner
                </button>
              </div>
            </div>
          </div>

          <!-- Правая колонка: баннер -->
          <div ref="observerTargetHeaderButtons" class="flex items-center justify-center">
            <img v-if="userBanner" :src="userBanner" alt="Banner"
              class="rounded-2xl h-[400px] w-[600px] object-cover" />
          </div>
        </div>
      </div>
      <div  class="flex items-center mt-6 justify-center space-x-4">
        <button @click="createdPins(); activeTab = 'created'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border hover:bg-gray-100 rounded-t-2xl"
          :class="{ 'active scale-105': activeTab === 'created' }">
          Created
        </button>

        <button @click="savedPins(); activeTab = 'saved'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border hover:bg-gray-100 rounded-t-2xl"
          :class="{ 'active scale-105': activeTab === 'saved' }">
          Saved
        </button>

        <button @click="likedPins(); activeTab = 'liked'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border hover:bg-gray-100 rounded-t-2xl"
          :class="{ 'active scale-105': activeTab === 'liked' }">
          Liked
        </button>

        <button @click="boards(); activeTab = 'boards'"
          class="relative px-6 py-2 text-black transition hover:border-red-600 animated-border hover:bg-gray-100 rounded-t-2xl"
          :class="{ 'active scale-105': activeTab === 'boards' }">
          Boards
        </button>
      </div>
    </div>
  </div>
  <div class="min-h-[500px]">
    <CreatedPins v-if="showCreated" :user_id="user.id" :auth_user_id="auth_user_id" />
    <SavedPins v-if="showSaved" :user_id="user.id" :auth_user_id="auth_user_id" />
    <LikedPins v-if="showLiked" :user_id="user.id" />
    <Boards v-if="showBoards" :user_id="user.id" :auth_user_id="auth_user_id" />
  </div>
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

.description-box {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  overflow: hidden;
}
</style>