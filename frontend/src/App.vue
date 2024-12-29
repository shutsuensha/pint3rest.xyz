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
</script>

<template>
  <Auth v-if="has_token" :access_token="access_token" @logout="has_token = false; access_token = null; toast.success('successfully logout')"/>
  <NotAuth v-else @login="(token) => { access_token = token; has_token = true; confetti.addConfetti();toast.success('successfully login')}" />
</template>