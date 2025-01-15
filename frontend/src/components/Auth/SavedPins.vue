<script setup>
import { onMounted, ref, onBeforeUnmount, onActivated, onDeactivated } from 'vue';
import axios from 'axios';

import SavedPin from './SavedPin.vue';
import DeleteSavedPin from './DeleteSavedPin.vue';

const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

const showNoPins = ref(false)

const props = defineProps({
  user_id: Number,
  auth_user_id: Number
})

const loadPins = async () => {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/pins/user_saved_pins/${props.user_id}`, {
      params: { offset: offset.value, limit: limit.value },
      withCredentials: true,
    });

    // Append new pins to the existing ones
    pins.value.push({ pins: response.data, showAllPins: false });

    if (pins.value[0].pins.length === 0) {
      showNoPins.value = true
    }

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


const showDeleteSavePin = ref(null)

onMounted(() => {
  showDeleteSavePin.value = props.user_id === props.auth_user_id
  loadPins();  // Initial load
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});

onActivated(() => {
  window.addEventListener('scroll', handleScroll);
});

onDeactivated(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <div class="mt-10 ml-20" v-masonry transition-duration="0.4s" item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <SavedPin v-if="!showDeleteSavePin" v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id"
        :pin="pinem" 
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
      <DeleteSavedPin v-if="showDeleteSavePin" v-masonry-tile class="item" v-for="pinem in pinGroup.pins"
        :key="pinem.id" :pin="pinem" 
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>

  <div v-show="showNoPins" class="mt-10">
    <section class="text-center flex flex-col justify-center items-center relative">
      <h1 class="text-2xl font-bold mb-4">no pins</h1>
      <img class="h-72 rounded-xl" src="https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg" alt="not found image">
    </section>
  </div>
</template>
