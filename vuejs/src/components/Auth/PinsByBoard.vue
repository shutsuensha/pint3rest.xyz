<script setup>
import { onMounted, ref, onBeforeUnmount, onActivated, onDeactivated } from 'vue';
import axios from 'axios';

import CreatedPinBoard from './CreatedPinBoard.vue';
import CreatedDeletedPinBoard from './CreatedDeletedPinBoard.vue';


const pins = ref([]);
const offset = ref(0);
const limit = ref(10);

const cntLoading = ref(0)
const limitCntLoading = ref(null)

const isPinsLoading = ref(false);

const showNoPins = ref(false)

const props = defineProps({
  user_id: Number,
  auth_user_id: Number,
  boardId: Number,
  canEdit: Boolean,
  boardName: String
})


const loadPins = async () => {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;
  try {
    const response = await axios.get(`/api/boards/${props.boardId}`, {
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

const showAddPins = ref(false)

onMounted(() => {
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

const closeModal = () => {
  showAddPins.value = false;
  window.addEventListener('scroll', handleScroll);
  document.body.classList.remove("overflow-hidden");
};

const openModal = () => {
  document.body.classList.add("overflow-hidden");
  showAddPins.value = true;
  window.removeEventListener('scroll', handleScroll);
}
</script>

<template>
  <div class="mt-10" v-masonry transition-duration="0.4s" item-selector=".item" stagger="0.03s">
    <div v-for="pinGroup in pins" :key="pinGroup.id">
      <CreatedPinBoard v-if="!canEdit" v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id"
        :pin="pinem"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
      <CreatedDeletedPinBoard v-if="canEdit" v-masonry-tile class="item" v-for="pinem in pinGroup.pins" :key="pinem.id"
        :pin="pinem"
        :board_id="boardId"
        @pinLoaded="() => { cntLoading++; if (cntLoading === limitCntLoading) { pinGroup.showAllPins = true; isPinsLoading = false; cntLoading = 0 } }"
        :showAllPins="pinGroup.showAllPins" />
    </div>
  </div>
  <div v-show="showNoPins" class="mt-10">
    <section class="text-center flex flex-col justify-center items-center relative">
      <h1 class="text-2xl font-bold mb-4">no pins on board</h1>
      <img class="h-72 rounded-xl" src="https://i.pinimg.com/736x/40/f1/b0/40f1b01bf3df9bc24bdbad4589125023.jpg"
        alt="not found image">
    </section>
  </div>
</template>