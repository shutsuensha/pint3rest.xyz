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
  meImage: Object
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
  <nav class="fixed top-0 left-0 h-full w-20 flex flex-col items-center space-y-12 z-30 border-r py-4">

    <!-- Icons -->
    <div class="flex-grow flex flex-col items-center text-xl">
      <RouterLink :to="`/user/${me.username}`" 
        class="transition-transform duration-100 transform hover:scale-110 cursor-pointer rounded-full p-2 items-center">
        <img :src="meImage" alt="me profile" class="w-10 h-10 object-cover rounded-full" />
      </RouterLink>
      <RouterLink to="/" 
        :class="['transition-transform', 'duration-100', 'transform', 'hover:scale-150', 'cursor-pointer', 'rounded-md', 'p-6', 'flex', 'items-center']">
        <i :class="[isActiveLink('/') ? 'text-red-600 font-bold' : 'text-black', 'pi', 'pi-home']"></i>
      </RouterLink>
      <RouterLink to="/create-pin" 
        class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-6 flex items-center">
        <i :class="[isActiveLink('/create-pin') ? 'text-red-600 font-bold' : 'text-black', 'pi', 'pi-plus-circle']"></i>
      </RouterLink>
      <div 
        class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-6 flex items-center">
        <i class="pi pi-bell"></i>
      </div>
      <div 
        class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-6 flex items-center">
        <i class="pi pi-envelope"></i>
      </div>
    </div>

    <!-- Last Link -->
    <div @click="logout" 
      class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-5 text-xl mb-4 flex items-center">
      <i class="pi pi-sign-out"></i>
    </div>
  </nav>
</template>