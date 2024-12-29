<script setup>
import { ref, reactive } from "vue";
import { useToast } from "vue-toastification";
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'

const mediaFile = ref(null);
const mediaPreview = ref(null);
const isImage = ref(false);
const isVideo = ref(false);

const toast = useToast();

const color = ref('red')
const size = ref('100px')

const sendingPin = ref(false)

const formPin = reactive({
  title: '',
  description: '',
  href: '',
  tags: '',
});

function handleMediaUpload(event) {
  const file = event.target.files[0];
  if (file) {
    mediaFile.value = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      mediaPreview.value = e.target.result;

      // Check file type for preview
      if (file.type.startsWith("image/")) {
        isImage.value = true;
        isVideo.value = false;
      } else if (file.type.startsWith("video/")) {
        isImage.value = false;
        isVideo.value = true;
      }
    };
    reader.readAsDataURL(file);
  }
}

async function submitPin() {
  const title = formPin.title
  const description = formPin.description
  const href = formPin.href
  const tags = formPin.tags

  if (!mediaFile.value) {
    toast.warning('Please, upload file', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  sendingPin.value = true

  try {
    const response = await axios.post('/api/pins', {
      title: title,
      description: description,
      href: href
    },
      {
        withCredentials: true
      }
    )

    const pin_id = response.data.id

    try {
      const formData = new FormData();
      formData.append('file', mediaFile.value);

      const response = await axios.post(`/api/pins/upload/${pin_id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      sendingPin.value = false
    } catch (error) {
      console.log(error)
    }
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div class="mt-20 ml-20">
    <div class="mt-2 text-xl py-5 border-t border-b border-gray-300 px-4">
      <h1>Создание пина</h1>
    </div>
    <ClipLoader v-if="sendingPin" :color="color" :size="size"
      class="flex items-center justify-center h-96 font-extrabold" />
    <div v-else class="grid grid-cols-2 gap-6 mt-5 mx-36">
      <!-- First Column: Media Input and Preview -->
      <div>
        <label for="media" class="block mb-2 text-sm font-medium text-gray-900">Изображение/Видео</label>
        <input type="file" id="media" name="media" accept="image/*,video/*" @change="handleMediaUpload"
          class="block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500" />
        <!-- Media Preview -->
        <div v-if="mediaPreview" class="mt-2 rounded-3xl overflow-hidden">
          <img v-if="isImage" :src="mediaPreview" class="h-96 w-full object-cover" alt="Media Preview" />
          <video v-if="isVideo" :src="mediaPreview" class="h-96 w-full object-cover" autoplay loop muted />
        </div>
        <div v-else class="mt-2 rounded-3xl overflow-hidden">
          <div class="relative bg-gray-300 h-96 w-full flex justify-center items-center text-center">
            <!-- Upload Icon -->
            <div class="absolute flex flex-col items-center space-y-4">
              <i class="pi pi-arrow-up text-4xl text-gray-400"></i> <!-- Replace with your icon -->
              <p class="mt-2 text-sm text-gray-600">Upload image or video</p>
            </div>
          </div>
        </div>
      </div>
      <!-- Second Column: Title, Description, Href, Tags -->
      <div>
        <form class="space-y-7" @submit.prevent="submitPin">
          <!-- Title Field -->
          <div>
            <label for="title" class="block mb-2 text-sm font-medium text-gray-900">Название</label>
            <input v-model="formPin.title" type="text" name="title" id="title" autocomplete="off"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить название" />
          </div>
          <!-- Description Field -->
          <div>
            <label for="description" class="block mb-2 text-sm font-medium text-gray-900">Описание</label>
            <textarea v-model="formPin.description" name="description" id="description"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить описание"></textarea>
          </div>
          <!-- Href Field -->
          <div>
            <label for="href" class="block mb-2 text-sm font-medium text-gray-900">Ссылка</label>
            <input v-model="formPin.href" type="url" name="href" id="href" autocomplete="off"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить ссылку" />
          </div>
          <!-- Tags Field -->
          <div>
            <label for="tags" class="block mb-2 text-sm font-medium text-gray-900">Теги</label>
            <input v-model="formPin.tags" type="text" name="tags" id="tags" autocomplete="off"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl block w-full py-3 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить теги, разделенные запятыми" />
          </div>
          <!-- Submit Button -->
          <button type="submit"
            class="w-full text-white bg-red-500 hover:bg-red-600 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">
            Создать
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
