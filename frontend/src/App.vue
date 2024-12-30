<script setup>
import { ref, onMounted } from 'vue'
import JSConfetti from 'js-confetti'
import { useToast } from "vue-toastification";

const confetti = new JSConfetti()

const toast = useToast();

import NotAuth from '@/components/NotAuth/NotAuth.vue'
import Auth from '@/components/Auth/Auth.vue'

const has_token = ref(null)
const access_token = ref(null)



onMounted(() => {
  const accessToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('access_token='))
    ?.split('=')[1];

  if (accessToken) {
    has_token.value = true
    access_token.value = accessToken
  } else {
    has_token.value = false
  }
});

function logout() {
  has_token.value = false; 
  access_token.value = null; 
  toast.success('ꜱᴇᴇ ᴜ ɴᴇxᴛ ᴛɪᴍᴇ ', { bodyClassName: ["cursor-pointer", "text-center"] })
}

function login(token) {
  access_token.value = token; 
  has_token.value = true; 
  confetti.addConfetti();
  toast.success('𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓫𝓪𝓬𝓴 😽🥳', { bodyClassName: ["cursor-pointer", "text-center"] })
}
</script>

<template>
  <Auth v-if="has_token" :access_token="access_token" @logout="logout()"/>
  <NotAuth v-else @login="(token) => {login(token)}" />
</template>