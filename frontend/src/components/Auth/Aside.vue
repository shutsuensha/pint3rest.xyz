<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router';

const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;
};

const emit = defineEmits(['logout'])

const props = defineProps({
  me: Object,
  meImage: String
})


async function logout() {
  try {
    await axios.post('/api/users/logout')
    emit('logout')
  } catch (error) {
    console.log(error)
  }
}



onMounted(async () => {
})
</script>


<template>
  <nav
    class="fixed top-0 left-0 h-full w-20 flex flex-col justify-between items-center z-30 border-r border-gray-300 py-4">

    <!-- Icons -->
    <div class="flex flex-col items-center text-xl space-y-6">
      <RouterLink to="/"
        :class="[isActiveLink('/') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-home']"></i>
      </RouterLink>
      <RouterLink to="/create-pin"
        :class="[isActiveLink('/create-pin') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i :class="['pi', 'pi-plus-circle']"></i>
      </RouterLink>
      <RouterLink to="/updates"
        :class="[isActiveLink('/updates') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-bell"></i>
      </RouterLink>
      <RouterLink to="/messages"
        :class="[isActiveLink('/messages') ? 'bg-gray-200' : 'transition-transform duration-100 transform hover:scale-150 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <i class="pi pi-envelope"></i>
      </RouterLink>
    </div>

    <!-- Profile Link -->
    <div class="flex items-center justify-center">
      <RouterLink :to="`/user/${me.username}`"
      :class="[isActiveLink(`/user/${me.username}`) ? '' : 'transition-transform duration-100 transform hover:scale-125 cursor-pointer', 'rounded-lg', 'px-4', 'py-3', 'flex', 'items-center']">
        <img :src="meImage" alt="me profile" :class="[isActiveLink(`/user/${me.username}`) ? 'border-black' : 'border-gray-400', 'w-10' ,'h-10' ,'object-cover', 'rounded-full', 'border-2']" />
      </RouterLink>
    </div>

    <!-- Last Link -->
    <div @click="logout"
      class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-5 text-xl flex items-center">
      <i class="pi pi-sign-out"></i>
    </div>
  </nav>
</template>
