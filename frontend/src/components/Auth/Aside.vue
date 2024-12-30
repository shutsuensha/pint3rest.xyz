<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router';
import { initPopovers } from 'flowbite'



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
  initPopovers();
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
      <RouterLink :to="`/user/${me.username}`" data-popover-target="popover-user-profile" data-popover-placement="right"
        class="cursor-pointer rounded-full p-2">
        <img :src="meImage" alt="me profile" class="w-10 h-10 object-cover rounded-full border-2 border-red-500" />
      </RouterLink>
      <div data-popover id="popover-user-profile" role="tooltip"
        class="flex flex-col items-center absolute z-10 invisible w-32 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0">
        <div class="p-3 text-center">
          <!-- Centered Image -->
          <img class="w-10 h-10 rounded-full mx-auto"
            src="https://i.pinimg.com/736x/35/2b/6e/352b6eca3197fed60e0c5282a537e1a0.jpg" alt="Jese Leos">
          <!-- Centered Username -->
          <p class="mt-2 text-sm font-normal">
            <a href="#" class="hover:underline"> @username</a>
          </p>
        </div>
        <div data-popper-arrow></div>
      </div>
    </div>

    <!-- Last Link -->
    <div @click="logout"
      class="cursor-pointer rounded-md transition-transform duration-100 transform hover:scale-150 p-5 text-xl flex items-center">
      <i class="pi pi-sign-out"></i>
    </div>
  </nav>
</template>
