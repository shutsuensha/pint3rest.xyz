<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 0;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<template>
  <nav :class="['fixed top-0 left-20 w-full bg-white z-40', isScrolled ? 'shadow-lg' : '']">
    <div class="flex items-center justify-between px-6 py-3">
      <!-- Search Bar -->
      <div class="relative flex-1 mr-20">
        <input
          type="text"
          placeholder="Поиск"
          class="transition duration-300 cursor-pointer bg-gray-200 hover:bg-gray-300 text-md rounded-xl block w-full py-3 px-10 outline-none border-none focus:ring-0"
        />
        <div class="absolute left-1 top-4 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-600"></i>
        </div>
      </div>
    </div>
  </nav>
</template>
