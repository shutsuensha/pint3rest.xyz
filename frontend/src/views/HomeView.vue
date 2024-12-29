<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import axios from 'axios';

import Pin from '@/components/Auth/Pin.vue';

const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const loadPins = async () => {
  try {
    const response = await axios.get('/api/pins/', {
      params: { offset: offset.value, limit: limit.value },
      withCredentials: true,
    });

    // Append new pins to the existing ones
    pins.value.push(...response.data);
    offset.value += limit.value;  // Increase the offset for the next request

    console.log(pins.value);
  } catch (error) {
    console.log(error);
  }
};

const handleScroll = () => {
  const scrollableHeight = document.documentElement.scrollHeight;
  const currentScrollPosition = window.innerHeight + window.scrollY;

  // Trigger loadPins if user reaches bottom
  if (currentScrollPosition + 200 >= scrollableHeight) {
    loadPins();
  }
};

onMounted(() => {
  loadPins();  // Initial load
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <div class="mt-20 ml-20">
    <div class="grid grid-cols-5 gap-5 px-5">
      <Pin v-for="pin in pins" :key="pin.id" :pin="pin"/>
    </div>
  </div>
</template>
