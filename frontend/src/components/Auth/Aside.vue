<script setup>
import logo from '@/assets/logo.png';
import { onMounted } from 'vue';


defineProps({
  access_token: String
})

onMounted({

})
</script>


<template>
  <nav class="fixed top-0 left-0 h-full w-20 flex flex-col items-center space-y-12 z-30 border-r py-4">

    <!-- Icons -->
    <div class="flex-grow flex flex-col items-center space-y-8 text-xl mt-2">
      <div class="cursor-pointer rounded-full hover:bg-gray-200 p-3 items-center">
        <img :src="logo" alt="Logo" class="w-10 h-10 rounded-full">
      </div>
      <div data-tooltip-target="tooltip-home" data-tooltip-placement="right"
        class="cursor-pointer rounded-md hover:bg-gray-200 p-3 flex items-center">
        <i class="pi pi-home"></i>
      </div>
      <div data-tooltip-target="tooltip-create" data-tooltip-placement="right"
        class="cursor-pointer rounded-md hover:bg-gray-200 p-3 flex items-center">
        <i class="pi pi-plus-circle"></i>
      </div>
      <div data-tooltip-target="tooltip-updates" data-tooltip-placement="right"
        class="cursor-pointer rounded-md hover:bg-gray-200 p-3 flex items-center">
        <i class="pi pi-bell"></i>
      </div>
      <div data-tooltip-target="tooltip-messages" data-tooltip-placement="right"
        class="cursor-pointer rounded-md hover:bg-gray-200 p-3 flex items-center">
        <i class="pi pi-envelope"></i>
      </div>
    </div>

    <!-- Last Link -->
    <div data-tooltip-target="tooltip-settings" data-tooltip-placement="right"
      class="cursor-pointer rounded-md hover:bg-gray-200 p-3 text-xl mb-4 flex items-center">
      <i class="pi pi-cog"></i>
    </div>
  </nav>

  <div id="tooltip-home" role="tooltip"
    class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
    Главная
    <div class="tooltip-arrow" data-popper-arrow></div>
  </div>

  <div id="tooltip-create" role="tooltip"
    class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
    Создать
    <div class="tooltip-arrow" data-popper-arrow></div>
  </div>

  <div id="tooltip-updates" role="tooltip"
    class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
    Обновления
    <div class="tooltip-arrow" data-popper-arrow></div>
  </div>

  <div id="tooltip-messages" role="tooltip"
    class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
    Сообщения
    <div class="tooltip-arrow" data-popper-arrow></div>
  </div>

  <div id="tooltip-settings" role="tooltip"
    class="absolute z-30 invisible inline-block px-3 py-2 text-xs font-medium text-white  bg-black rounded-md tooltip">
    Настройки
    <div class="tooltip-arrow" data-popper-arrow></div>
  </div>

</template>