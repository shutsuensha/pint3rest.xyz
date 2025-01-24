<script setup>
import Aside from './Aside.vue';
import { RouterView } from 'vue-router';
import { ref, onMounted, computed  } from 'vue';
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import { useRoute, RouterLink, useRouter } from 'vue-router';

const route = useRoute();

const emit = defineEmits(['logout', 'createPinModelClose'])

const me = ref(null)
const meImage = ref(null)
const loadingProfile = ref(true)

const color = ref('red')
const size = ref('100px')


const props = defineProps({
  access_token: String,
  register: Boolean
})

onMounted(async () => {
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
</script>


<template>
  <ClipLoader v-if="loadingProfile" :color="color" :size="size" class="flex items-center justify-center h-screen" />
  <Aside v-if="!loadingProfile" @logout="emit('logout')" :me="me" :meImage="meImage" />
  <RouterView v-slot="{ Component }">
    <KeepAlive :max="10" exclude="NotFoundView,CreatePinView">
      <component :is="Component" :key="$route.fullPath" v-bind="homeProps" v-on="homeEvents" />
    </KeepAlive>
  </RouterView>

</template>