<script setup>

</script>


<template>
  <nav class=" fixed top-0 left-0 w-full bg-white z-20">
    <div class="flex items-center justify-between px-6 py-4">
      <!-- Search Bar -->
      <div class="relative flex-1 ml-20 mr-2">
        <input type="text" placeholder="Поиск"
          class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-md rounded-3xl block w-full py-3 px-10 focus:ring-red-500 focus:border-red-500 hover:bg-gray-100" />
        <div class="absolute left-1 top-4 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-600"></i>
        </div>
      </div>
    </div>
  </nav>
</template>