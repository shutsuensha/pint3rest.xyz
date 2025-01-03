<script setup>
import { ref, reactive, nextTick, onMounted } from "vue";
import { useToast } from "vue-toastification";
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import axios from 'axios'
import router from '@/router';

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
});

const tagToAdd = ref('')

const available_tags = ref(null)
const bgColors = ref(['bg-red-200', 'bg-orange-200', 'bg-amber-200', 'bg-lime-200', 'bg-green-200', 'bg-emerald-200', 'bg-teal-200'])
const tags = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/tags/', { withCredentials: true })
    available_tags.value = response.data
  } catch (error) {
    console.log(error)
  }
})

function handleMediaUpload(event) {
  const file = event.target.files[0];
  if (file) {
    mediaFile.value = file;

    const reader = new FileReader();
    reader.onload = async (e) => {
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
    const response = await axios.post('/api/pins', {
      title: title,
      description: description,
      href: href,
      height: `${height}`
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

    } catch (error) {
      console.log(error)
    }

    if (tags.value.length !== 0) {
      try {
        const response = await axios.post(`/api/tags/`, {
          pin_id: pin_id,
          tags: tags.value
        })
        sendingPin.value = false
        router.push('/');
      } catch (error) {
        console.error(error)
      }
    } else {
      sendingPin.value = false
      router.push('/');
    }
  } catch (error) {
    console.log(error)
  }
}

const randomBgColor = () => {
  const randomIndex = Math.floor(Math.random() * bgColors.value.length);
  return bgColors.value[randomIndex];
};


function addTag() {
  available_tags.value.push({ id: available_tags.value.length, name: tagToAdd.value })
  tagToAdd.value = ''
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
  <div class="mt-20 ml-20">
    <div class="mt-2 text-xl py-5 border-t border-b border-gray-300 px-4">
      <h1>Создание пина</h1>
    </div>
    <ClipLoader v-if="sendingPin" :color="color" :size="size"
      class="flex items-center justify-center h-96 font-extrabold" />
    <div v-else class="grid grid-cols-2 mt-5 mr-72">
      <!-- First Column: Media Input and Preview -->
      <div class="ml-36">
        <label for="media"
          class="block w-[271px] mx-auto text-center mb-2 text-sm font-medium text-gray-900">Изображение/Видео</label>
        <input type="file" id="media" name="media" accept="image/*,video/*" @change="handleMediaUpload"
          class="block w-[271px] mx-auto text-sm text-gray-900 border border-gray-300 rounded-xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500" />
        <!-- Media Preview -->
        <div id="mediaPreview" v-if="mediaPreview" class="mt-2">
          <img id="imagePreview" v-if="isImage" :src="mediaPreview" class="h-auto w-[271.84px] rounded-3xl mx-auto"
            alt="Media Preview" />
          <video id="videoPreview" v-if="isVideo" :src="mediaPreview" class="h-auto w-[271.84px] rounded-3xl mx-auto"
            autoplay loop muted />
        </div>
        <div v-else class="mt-2 overflow-hidden">
          <div
            class="relative bg-gray-300 h-96 w-[271.84px] flex justify-center items-center text-center rounded-3xl mx-auto">
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
        <div class="space-y-7 mt-6">
          <!-- Title Field -->
          <div>
            <input v-model="formPin.title" type="text" name="title" id="title" autocomplete="off"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl block w-full py-4 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить название" />
          </div>
          <!-- Description Field -->
          <div>
            <textarea v-model="formPin.description" name="description" id="description"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl block w-full py-4 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить описание"></textarea>
          </div>
          <!-- Href Field -->
          <div>
            <input v-model="formPin.href" type="url" name="href" id="href" autocomplete="off"
              class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl block w-full py-4 px-5 focus:ring-red-500 focus:border-red-500"
              placeholder="Добавить ссылку" />
          </div>
          <!-- Tags Field -->
          <div>

            <div class="flex items-center space-x-2">
              <!-- Add Button -->
              <button type="button" @click="addTag"
                class="bg-red-500 hover:bg-red-600 text-white font-medium rounded-xl text-sm px-4 py-2">
                Создать
              </button>

              <!-- Tags Input -->
              <input v-model="tagToAdd" type="text" name="tags" id="tags" autocomplete="off"
                class="cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl flex-grow py-3 px-5 focus:ring-red-500 focus:border-red-500"
                placeholder="Создать тег" />
            </div>
            <div class="mt-5">
              <!-- Heading -->
              <h3 class="text-md mb-2 text-gray-600">Выберите теги</h3>

              <!-- Tags List -->
              <div class="flex space-x-2">
                <div v-show="available_tags" v-for="tag in available_tags" :key="tag.id" @click="addTagToPin(tag.name)"
                  :class="[checkPinAded(tag.name) ? 'border-black border' : '', 'text-sm', 'font-medium', 'rounded-xl', 'px-2', 'py-2', randomBgColor(), 'cursor-pointer', 'transition-transform', 'duration-200', 'transform', 'hover:scale-110']">
                  {{ tag.name }}
                </div>
                <div v-show="!available_tags" class="h-11"></div>
              </div>
            </div>
          </div>
          <!-- Submit Button -->
          <button @click="submitPin"
            class="w-full text-white bg-red-500 hover:bg-red-600 font-medium rounded-xl text-sm px-5 py-2.5 text-center">
            Создать Пин
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
