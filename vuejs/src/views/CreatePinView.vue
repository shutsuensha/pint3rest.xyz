<script setup>
import { ref, reactive, nextTick, onMounted, computed, watch } from "vue";
import { useToast } from "vue-toastification";
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import router from '@/router';
import { useRoute, useRouter } from 'vue-router';

import SearchBar from '@/components/Auth/SearchBar.vue';

import { useUnreadMessagesStore } from "@/stores/unreadMessages";

const unreadMessagesStore = useUnreadMessagesStore();


import { useUnreadUpdatesStore } from "@/stores/unreadUpdates";

const unreadUpdatesStore = useUnreadUpdatesStore();

const mediaFile = ref(null);
const mediaPreview = ref(null);
const isImage = ref(false);
const isVideo = ref(false);

const isDragging = ref(false);


const routerBack = useRouter();

const searchValue = ref('')


const onSearchInput = () => {
  // Перенаправление на /home при вводе текста
  router.push('/?search')
}


const toast = useToast();

const color = ref('red')
const size = ref('100px')

const sendingPin = ref(false)

const formPin = reactive({
  title: '',
  description: '',
  href: '',
});

const tagToAdd = ref('')

const available_tags = ref(null)
const bgColors = ref(['bg-red-200', 'bg-orange-200', 'bg-amber-200', 'bg-lime-200', 'bg-green-200', 'bg-emerald-200', 'bg-teal-200', 'bg-sky-200', 'bg-blue-200', 'bg-indigo-200', 'bg-violet-200', 'bg-purple-200', 'bg-fuchsia-200', 'bg-pink-200', 'bg-rose-200'])
const tags = ref([])


const filteredTags = computed(() => {
  if (!searchValue.value.trim()) {
    return available_tags.value;
  }
  return available_tags.value.filter(tag =>
    tag.name.toLowerCase().includes(searchValue.value.toLowerCase())
  );
});



onMounted(async () => {
  let unreadMessagesCount = unreadMessagesStore.count;
  let unreadUpdatesCount = unreadUpdatesStore.count;
  let totalUnread = unreadMessagesCount + unreadUpdatesCount;

  if (totalUnread > 0) {
    document.title = `(${totalUnread}) Pinterest`; // Если есть непрочитанные уведомления
  } else {
    document.title = 'Pinterest'; // Если уведомлений нет
  }
  try {
    const response = await axios.get('/api/tags/', { withCredentials: true })
    available_tags.value = response.data
    for (let i = 0; i < response.data.length; i++) {
      const tag = response.data[i];
      tag.color = randomBgColor()
    }
  } catch (error) {
    console.log(error)
  }
})

function handleMediaUpload(event) {
  const file = event.target.files[0];

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm'];

  if (file) {
    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid media file (.jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm).', {
        position: "top-center",
        bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
      });
      return;
    }

    const minWidth = 200;
    const minHeight = 300;

    if (file.type.startsWith("image/")) {
      const img = new Image();
      img.onload = () => {
        if (img.width < minWidth || img.height < minHeight) {
          toast.warning(`Image must be at least ${minWidth}x${minHeight}.`, {
            position: "top-center",
            bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
          });
          return;
        }
        previewFile(file);
      };
      img.src = URL.createObjectURL(file);

    } else if (file.type.startsWith("video/")) {
      const video = document.createElement("video");
      video.preload = "metadata";

      video.onloadedmetadata = () => {
        window.URL.revokeObjectURL(video.src);

        if (video.duration > 30) {
          toast.warning('Video must be 30 seconds or less.', {
            position: "top-center",
            bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
          });
          return;
        }

        previewFile(file);
      };

      video.src = URL.createObjectURL(file);
    }
  }
}


const previewFile = (file) => {
  mediaFile.value = file;
  const reader = new FileReader();

  reader.onload = (e) => {
    mediaPreview.value = e.target.result;
  };

  reader.readAsDataURL(file);

  if (file.type.startsWith("image/")) {
    isImage.value = true;
    isVideo.value = false;
  } else if (file.type.startsWith("video/")) {
    isImage.value = false;
    isVideo.value = true;
  }
};


const onDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm'];

  if (file) {
    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid media file (.jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm).', {
        position: "top-center",
        bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
      });
      return;
    }

    const minWidth = 200;
    const minHeight = 300;

    if (file.type.startsWith("image/")) {
      const img = new Image();
      img.onload = () => {
        if (img.width < minWidth || img.height < minHeight) {
          toast.warning(`Image must be at least ${minWidth}x${minHeight}.`, {
            position: "top-center",
            bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
          });
          return;
        }
        previewFile(file);
      };
      img.src = URL.createObjectURL(file);

    } else if (file.type.startsWith("video/")) {
      const video = document.createElement("video");
      video.preload = "metadata";

      video.onloadedmetadata = () => {
        window.URL.revokeObjectURL(video.src);

        if (video.duration > 30) {
          toast.warning('Video must be 30 seconds or less.', {
            position: "top-center",
            bodyClassName: ["cursor-pointer", "text-black", "font-bold"]
          });
          return;
        }

        previewFile(file);
      };

      video.src = URL.createObjectURL(file);

    }
  }
};

// Handle drag over
const onDragOver = () => {
  isDragging.value = true;
};

// Handle drag leave
const onDragLeave = () => {
  isDragging.value = false;
};

const goBack = () => {
  routerBack.back();
};



const fileError = ref(false)

async function submitPin() {
  const title = formPin.title.trim()
  const description = formPin.description.trim()
  const href = formPin.href.trim()

  if (!mediaFile.value) {
    toast.warning('Please, upload file', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
    return
  }

  sendingPin.value = true

  try {
    let height = null;
    if (isImage.value) {
      const rect = document.getElementById('imagePreview').getBoundingClientRect();
      height = rect.height.toFixed(2);
    } else {
      const rect = document.getElementById('videoPreview').getBoundingClientRect();
      height = rect.height.toFixed(2);
    }
    const formData = new FormData();
    formData.append("file", mediaFile.value); // Файл

    const jsonData = JSON.stringify({
      title: title,
      description: description,
      href: href,
      height: `${height}`
    });

    formData.append("pin_model", jsonData); // Передаем строку, а не Blob

    const response = await axios.post("/api/pins/create-pin-entity", formData, {
      withCredentials: true,
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });


    const pin_id = response.data.id

    // try {
    //   const formData = new FormData();
    //   formData.append('file', mediaFile.value);

    //   const response = await axios.post(`/api/pins/upload/${pin_id}`, formData, {
    //     headers: {
    //       'Content-Type': 'multipart/form-data',
    //     },
    //   });

    // } catch (error) {
    //   console.log(error)
    // }

    if (tags.value.length !== 0) {
      try {
        const response = await axios.post(`/api/tags/`, {
          pin_id: pin_id,
          tags: tags.value
        })
        sendingPin.value = false
        router.push(`/pin/${pin_id}`);
      } catch (error) {
        console.error(error)
      }
    } else {
      sendingPin.value = false
      router.push(`/pin/${pin_id}`);
    }
  } catch (error) {
    if (error.response.status === 415) {
      fileError.value = true
    }
  }
}

const randomBgColor = () => {
  const randomIndex = Math.floor(Math.random() * bgColors.value.length);
  return bgColors.value[randomIndex];
};


function addTag() {
  if (tagToAdd.value.trim()) {
    available_tags.value.unshift({ id: available_tags.value.length, name: tagToAdd.value, color: randomBgColor() });
    tagToAdd.value = '';
  }
}


function addTagToPin(name) {
  if (checkPinAded(name)) {
    tags.value = tags.value.filter((el) => el !== name);
  }
  else {
    tags.value.push(name)
  }
}

function checkPinAded(name) {
  return tags.value.includes(name);
}



</script>

<template>
  <div v-if="fileError" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-white rounded-3xl shadow">
        <div class="p-5 text-center">
          <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif, .webp,
            .png, .bmp, .mp4, .webm </h3>
          <button @click="fileError = false" type="button"
            class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
            Ok, understand
          </button>
        </div>
      </div>
    </div>
  </div>
  <SearchBar />
  <div class="ml-20 mt-20">
    <ClipLoader v-if="sendingPin" :color="color" :size="size"
      class="flex items-center justify-center h-96 font-extrabold" />
    <div v-else class="grid grid-cols-2 mt-10 mr-72 gap-10">
      <button @click="goBack" class="absolute top-4 left-20 text-gray-500 ml-20 mt-20 hover:-translate-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div class="ml-56">
        <label for="mediacreate" class="cursor-pointer" @dragover.prevent="onDragOver" @dragleave="onDragLeave"
          @drop.prevent="onDrop">
          <!-- Media Preview -->
          <div id="mediaPreview" v-if="mediaPreview"
            class="mt-2 border border-dashed border-gray-400 rounded-3xl hover:border-purple-500 hover:bg-purple-100 transition duration-100"
            :class="{ 'border-purple-500 bg-purple-100': isDragging }">
            <img id="imagePreview" v-if="isImage" :src="mediaPreview"
              class="h-auto w-[271.84px] rounded-3xl mx-auto my-8" alt="Media Preview" />
            <video id="videoPreview" v-if="isVideo" :src="mediaPreview"
              class="h-auto w-[271.84px] rounded-3xl mx-auto my-8" autoplay loop muted />
          </div>

          <!-- Placeholder for no preview -->
          <div v-else
            class="mt-2 border border-dashed border-gray-900 rounded-3xl hover:border-purple-500 hover:bg-purple-100 transition duration-100 overflow-hidden"
            :class="{ 'border-purple-500 bg-purple-100': isDragging }">
            <div
              class="relative  h-96 w-[271.84px] flex justify-center items-center text-center rounded-3xl mx-auto my-8">
              <div class="absolute flex flex-col items-center space-y-4">
                <i class="pi pi-arrow-up text-4xl text-gray-400"></i>
                <p class="mt-2 text-xl text-black">Drag & Drop or Click to Upload</p>
                <p class="mt-2 text-sm text-gray-700">Images must be at least 200x300 pixels</p>
                <p class="mt-2 text-sm text-gray-700">Videos must be 30 seconds or less</p>
                <p class="mt-2 text-xs text-gray-700">.jpg .jpeg .gif .webp .png .bmp .mp4 .webm</p>
              </div>
            </div>
          </div>
        </label>
        <input type="file" id="mediacreate" name="media" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp,.mp4,.webm"
          @change="handleMediaUpload" class="hidden" />

        <button @click="submitPin"
          class="w-full mt-10 transition duration-100 text-white bg-purple-500 hover:bg-purple-600 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">
          Create Pin
        </button>
      </div>

      <div>
        <div class="space-y-7 mt-2 mb-10">
          <!-- Title Field -->
          <div>
            <input v-model="formPin.title" type="text" name="title" id="titleCreate" autocomplete="off"
              class="hover:bg-purple-100 transition duration-100  cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl block w-full py-4 px-5 focus:ring-purple-500 focus:border-purple-500"
              placeholder="Add title" />
          </div>
          <!-- Description Field -->
          <div>
            <textarea v-model="formPin.description" name="description" id="descriptionCreate"
              class="hover:bg-purple-100 transition duration-100 cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl block w-full py-4 px-5 focus:ring-purple-500 focus:border-purple-500"
              placeholder="Add description"></textarea>
          </div>
          <!-- Href Field -->
          <div>
            <input v-model="formPin.href" type="url" name="href" id="href" autocomplete="off"
              class="hover:bg-purple-100 transition duration-100 cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl block w-full py-4 px-5 focus:ring-purple-500 focus:border-purple-500"
              placeholder="Add link (any website link)" />
          </div>
          <!-- Tags Field -->

          <div>
            <div class="mt-5">
              <!-- Heading -->

              <h3 class="text-md mb-2 text-gray-600">Add Tags to Pin</h3>

              <div class="flex items-center space-x-2 mb-4">
                <button type="button" @click="addTag"
                  class="bg-purple-500 hover:bg-purple-600 transition duration-100 text-white font-medium rounded-3xl text-sm px-4 py-2">
                  Create
                </button>

                <input v-model="tagToAdd" type="text" name="tags" id="tags" autocomplete="off" @keydown.enter="addTag"
                  class="hover:bg-purple-100 transition duration-100 cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl flex-grow py-3 px-5 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Create Tag" />
              </div>


              <input v-model="searchValue" type="text" placeholder="Search Tag"
                class="hover:bg-purple-100 transition duration-100 cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl w-full py-3 px-5 focus:ring-purple-500 focus:border-purple-500 mb-4" />

              <!-- Tags List -->
              <div class="flex flex-wrap gap-2" v-auto-animate>
                <div v-for="tag in filteredTags" :key="tag.id" @click="addTagToPin(tag.name)"
                  :class="[checkPinAded(tag.name) ? 'bg-black text-white shadow-lg scale-110' : `${tag.color}`, 'text-sm', 'font-medium', 'rounded-3xl', 'px-3', 'py-2', 'cursor-pointer', 'transition-transform', 'duration-200', 'transform', 'hover:scale-110']">
                  {{ tag.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>