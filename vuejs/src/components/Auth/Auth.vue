<script setup>
import Aside from './Aside.vue';
import { RouterView } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import { useRoute, RouterLink, useRouter } from 'vue-router';
import MessagesView from '@/views/MessagesView.vue';
import HomeView from '@/views/HomeView.vue';

import { useUnreadMessagesStore } from "@/stores/unreadMessages";
import { useSelectedBoard } from "@/stores/userSelectedBoard";
import { authUserStore } from "@/stores/authUserStore";

const unreadMessagesStore = useUnreadMessagesStore();
const userSelectedBoardStroe = useSelectedBoard();
const userStore = authUserStore();

import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();


const route = useRoute();

const emit = defineEmits(['logout', 'createPinModelClose'])

const me = ref(null)
const meImage = ref(null)
const loadingProfile = ref(true)

const color = ref('red')
const size = ref('100px')


const props = defineProps({
  access_token: String,
  register: Boolean,
})


onMounted(async () => {
  unreadMessagesStore.fetchUnreadMessages();
  userSelectedBoardStroe.fetchSelectedBoard()
  unreadUpdatesStore.fetchUnreadUpdates()
  try {
    if (props.access_token) {
      // Decode the JWT token
      const base64Url = props.access_token.split('.')[1] // Get the payload part of the token
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )

      const payload = JSON.parse(jsonPayload) // Parse the payload

      const user_id = payload.user_id // Assuming 'user_id' exists in the payload

      const response = await axios.get(`/api/users/user_id/${user_id}`)
      me.value = response.data

      userStore.setUsername(me.value.username)

      try {
        const response = await axios.get(`/api/users/upload/${user_id}`, { responseType: 'blob' })
        const blobUrl = URL.createObjectURL(response.data);
        meImage.value = blobUrl
        loadingProfile.value = false
      } catch (error) {
        console.log(error)
      }
    } else {
      console.log('No access token provided.')
    }
  } catch (error) {
    console.error('Error decoding access token:', error)
  }
})


const homeProps = computed(() => {
  if (route.name === 'home') {
    return { register: props.register }; // Replace `registerFunction` with your actual function
  }
  return {};
});

const homeEvents = computed(() => {
  if (route.name === 'home') {
    return {
      createPinModelClose: handleCreatePinModelClose, // Replace with your actual handler
    };
  }
  return {};
});

function handleCreatePinModelClose() {
  emit('createPinModelClose')
}

const cachedViews = computed(() =>
  route.name === "home" ? ["HomeView", "PinView", "UserView"] : ["HomeView"]
);

</script>


<template>


  <!-- <ClipLoader v-if="loadingProfile" :color="color" :size="size" class="flex items-center justify-center h-screen" /> -->
  <div v-if="loadingProfile" class="flex items-center justify-center h-screen">
    <span class="text-8xl logo">
         🐰
    </span>
  </div>
  <Aside v-if="!loadingProfile" @logout="emit('logout')" :me="me" :meImage="meImage" />


  <RouterView v-if="!loadingProfile" v-slot="{ Component }">
    <div v-show="$route.name === 'messages'">
      <component :is="MessagesView" :key="'messages'" />
    </div>

    <KeepAlive :include="['HomeView']">
      <component v-if="$route.name === 'home'" :is="Component" :key="$route.name" v-bind="homeProps"
        v-on="homeEvents" />
    </KeepAlive>

    <KeepAlive :max="10" :include="['PinView', 'UserView', 'RecommendationsView']">
      <component v-if="$route.name !== 'home' && $route.name !== 'messages'" :is="Component" :key="$route.fullPath" />
    </KeepAlive>
  </RouterView>


</template>

<style scoped>
@keyframes pulse-scale {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

.logo {
  animation: pulse-scale 1.5s infinite ease-in-out;
}

</style>