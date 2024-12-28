<script setup>

</script>


<template>
  <nav class="fixed top-0 left-0 w-full bg-white z-20">
    <div class="flex items-center justify-between px-6 py-4">
      <!-- Search Bar -->
      <div class="relative flex-1 ml-20 mr-2">
        <input type="text" placeholder="Поиск"
          class="w-full py-3 px-10 rounded-3xl focus:outline-none border-none focus:ring-2 focus:ring-blue-400 bg-zinc-100 hover:bg-zinc-200" />
        <div class="absolute left-1 top-3.5 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-600"></i>
        </div>
      </div>
    </div>
  </nav>
</template>