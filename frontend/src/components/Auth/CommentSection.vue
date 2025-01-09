<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import AOS from 'aos';
import 'aos/dist/aos.css';

const props = defineProps({
  pin_id: Number
})

const comments = ref([])

const offset = ref(0);
const limit = ref(5);

const isPinsLoading = ref(false);

async function loadComments() {
  if (isPinsLoading.value) {
    return;
  }

  isPinsLoading.value = true;

  try {
    const response = await axios.get(`/api/comments/${props.pin_id}`, { params: { offset: offset.value, limit: limit.value } })
    for (let i = 0; i < response.data.length; i++) {
      const commentData = response.data[i]
      let commentImage = null
      if (commentData.image) {
        try {
          const response = await axios.get(`/api/comments/upload/${commentData.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          commentImage = blobUrl;
        } catch (error) {
          console.error(error);
        }
      }
      let commentUser = null
      let commentUserImage = null
      try {
        const response = await axios.get(`/api/users/user_id/${commentData.user_id}`)
        commentUser = response.data
        try {
          const response = await axios.get(`/api/users/upload/${commentUser.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          commentUserImage = blobUrl;
        } catch (error) {
          console.error(error);
        }
        comments.value.push({
          id: commentData.id, content: commentData.content, created_at: commentData.created_at, image: commentImage,
          user: commentUser, userImage: commentUserImage, showReply: false, replyContent: ''
        })
      } catch (error) {
        console.error(error)
      }
    }
  } catch (error) {
    console.error(error)
  }

  offset.value += limit.value;
  isPinsLoading.value = false;
}

const handleScroll = (event) => {
  const container = event.target;
  if (container.scrollTop + container.clientHeight >= container.scrollHeight - 10) {
    loadComments();
  }
};

onMounted(() => {
  AOS.init({
    duration: 500,  // Длительность анимации
    once: true,      // Анимация будет воспроизводиться только один раз
  });
  loadComments();  // Initial load
});

async function addComment(comment) {
  if (comment.replyContent.trim() !== '') {
    try {
      const response = await axios.post(`/api/comments/comment/${comment.id}`, {
        content: comment.replyContent.trim()
      })
      comment.replyContent = ''
    } catch (error) {
      console.error(error)
    }
  }
}
</script>


<template>
  <div @scroll="handleScroll"
    class="flex flex-col gap-4 bg-white rounded-xl text-sm font-medium text-gray-700 z-30 h-60 w-full overflow-y-auto">
    <div v-for="comment in comments" :key="comment.id" class="flex flex-col mb-2">
      <RouterLink :to="`/user/${comment.user.username}`"
        class="flex items-center space-x-2 hover:underline cursor-pointer">
        <img :src="comment.userImage" alt="User Image" class="w-10 h-10 rounded-full object-cover" />
        <span class="text-gray-700 font-medium">{{ comment.user.username }}</span>
      </RouterLink>
      <span class="text-gray-700 font-medium">{{ comment.content }}</span>
      <img v-if="comment.image" :src="comment.image" alt="comment image" class="h-28 w-28 object-cover rounded-lg" />
      <div v-if="comment.showReply" class="flex items-center space-x-2">
        <button type="button" @click="addComment(comment)"
          class="bg-red-500 hover:bg-red-600 transition duration-300 text-white font-medium rounded-xl text-sm px-4 py-2">
          Ответить
        </button>

        <!-- Tags Input -->
        <input v-model="comment.replyContent" type="text" name="comment" id="comment" autocomplete="off"
          class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl flex-grow py-3 px-5 focus:ring-red-500 focus:border-red-500"
          placeholder="Введите комментарий" />
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 font-medium">{{ comment.created_at }}</span>
        <span @click="comment.showReply = !comment.showReply"
          class="hover:underline hover:text-blue-400 cursor-pointer">Ответить</span>
      </div>
    </div>
  </div>
</template>