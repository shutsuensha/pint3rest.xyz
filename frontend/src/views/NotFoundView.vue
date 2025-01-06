<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'

const image = ref(null)

const loading = ref(true)
const color = ref('red')
const size = ref('100px')

onMounted(async () => {
  try {
    const response = await axios.get(`/api/not-found`, { responseType: 'blob' });
    const blobUrl = URL.createObjectURL(response.data);
    image.value = blobUrl
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="text-center flex flex-col justify-center items-center relative top-20">
    <h1 class="text-4xl font-bold mb-4">404</h1>
    <ClipLoader v-if="loading" :size="size" :color="color" />
    <img v-else class="h-96 rounded-xl" :src="image"
      alt="not found image">
  </section>
</template>