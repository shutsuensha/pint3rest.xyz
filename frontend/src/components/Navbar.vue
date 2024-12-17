<script setup>
import { onMounted } from 'vue'
import { initTooltips } from 'flowbite'


onMounted(() => {
  initTooltips();
})
</script>


<template>
  <nav class="fixed top-0 left-0 w-full bg-white z-20">
    <div class="flex items-center justify-between px-6 py-4">
      <!-- Search Bar -->
      <div class="relative flex-1 ml-16 mr-2">
        <input type="text" placeholder="Поиск"
          class="w-full py-3 px-10 rounded-xl focus:outline-none border-none focus:ring-2 focus:ring-blue-400 bg-zinc-100 hover:bg-zinc-200" />
        <div class="absolute left-1 top-3.5 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-600"></i>
        </div>
      </div>

      <!-- Profile -->
      <div data-tooltip-target="tooltip-profile" class="flex items-center rounded-md hover:bg-gray-200 p-1.5 mr-6">
        <div class="rounded-full bg-gray-200 flex items-center justify-center cursor-pointer">
          <img src="https://i.pinimg.com/736x/91/6b/36/916b36a2cddb4217473874e192d41f8f.jpg" alt="profile"
            class="h-9 w-9 rounded-full" />
        </div>
      </div>

      <div id="tooltip-profile" role="tooltip"
        class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
        Профиль
        <div class="tooltip-arrow" data-popper-arrow></div>
      </div>
    </div>
  </nav>
</template>