<script setup>
import { ref, onMounted, nextTick } from 'vue'
import JSConfetti from 'js-confetti'
import { useToast } from "vue-toastification";
import { useRoute, useRouter } from 'vue-router';
import ResumeView from '@/views/ResumeView.vue';

const confetti = new JSConfetti()

const toast = useToast();

const route = useRoute()
const router = useRouter()

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
  router.push('/')
}


async function login(token) {
  access_token.value = token;
  has_token.value = true;
}

const register = ref(false)


function signup(token) {
  access_token.value = token;
  has_token.value = true;
  register.value = true
}
</script>

<template>
  <Auth v-if="has_token === true && route.path !== '/resume'" :access_token="access_token" @logout="logout()" :register="register"
    @createPinModelClose="register = false" />
  <NotAuth v-if="has_token === false && route.path !== '/resume'" @login="(token) => { login(token) }" @signup="(token) => { signup(token) }" />
  <ResumeView v-if="route.path === '/resume'"/>
</template>