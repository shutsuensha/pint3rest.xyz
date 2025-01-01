<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import CreatedPins from '@/components/Auth/CreatedPins.vue';
import SavedPins from '@/components/Auth/SavedPins.vue';

const color = ref('red')
const size = ref('100px')

const route = useRoute();

const loadingUser = ref(true)

const username = route.params.username
const user = ref(null)
const userImage = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get(`/api/users/user_username/${username}`);
    user.value = response.data;
    try {
      const userResponse = await axios.get(`/api/users/upload/${user.value.id}`, { responseType: 'blob' });
      const blobUrl = URL.createObjectURL(userResponse.data);
      userImage.value = blobUrl;
      loadingUser.value = false
    } catch (error) {
      console.error(error)
    }
  } catch (error) {
    console.log(error)
  }
})


const bgCreated = ref('border-gray-200')
const bgSaved = ref('border-gray-200')

const showCreated = ref(false)
const showSaved = ref(false)


async function createdPins() {
  showSaved.value = false
  showCreated.value = true
  bgSaved.value = 'border-gray-200'
  bgCreated.value = 'border-red-600'
}


async function savedPins() {
  showSaved.value = true
  showCreated.value = false
  bgCreated.value = 'border-gray-200'
  bgSaved.value = 'border-red-600'
}
</script>


<template>
  <div class="flex items-center justify-center mt-20">
    <ClipLoader v-if="loadingUser" :color="color" :size="size" class="" />
    <div v-else class="flex flex-col items-center">
      <img v-if="userImage" :src="userImage" alt="Profile Picture" class="rounded-full w-32 h-32 object-cover" />
      <p v-if="user" class="mt-4 text-lg font-semibold text-gray-700">@{{ user.username }}</p>
      <div class="flex mt-4 space-x-4">
        <button @click="createdPins" :class="`px-6 py-2 text-black  border-b-4 ${bgCreated} transition hover:border-red-600` ">
          Созданные
        </button>
        <button @click="savedPins" :class="`px-6 py-2 text-black  border-b-4 ${bgSaved} transition hover:border-red-600`">
          Сохраненные
        </button>
      </div>
    </div>
  </div>
  <CreatedPins v-if="showCreated" :user_id="user.id"/>
  <SavedPins v-if="showSaved" :user_id="user.id" />
</template>