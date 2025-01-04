<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue';
import axios from 'axios';

import Pin from '@/components/Auth/Pin.vue';

const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

const props = defineProps({
  pin_id: Number
})

const loadPins = async () => {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/tags/${props.pin_id}`, {
      params: { offset: offset.value, limit: limit.value },
      withCredentials: true,
    });

    // Append new pins to the existing ones
    pins.value.push({ pins: response.data, showAllPins: false });

    limitCntLoading.value = response.data.length

    limitCntLoading.value

    // Increment the offset
    offset.value += limit.value;

    // После первого запроса изменяем лимит на 5
    if (limit.value === 10) {
      limit.value = 5;
    }

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
  <div class="mt-10 ml-20" v-masonry transition-duration="0.4s" item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <Pin v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id" :pin="pinem"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
</template>
