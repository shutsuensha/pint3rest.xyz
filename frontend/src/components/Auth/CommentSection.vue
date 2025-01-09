<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import ReplyCommentSection from './ReplyCommentSection.vue';

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
          user: commentUser, userImage: commentUserImage, showReply: false, replyContent: '', replyImagePreview: null, replyImage: null, showReplies: false
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
  loadComments();  // Initial load
});

async function addComment(comment) {
  if (comment.replyContent.trim() !== '') {
    try {
      const response = await axios.post(`/api/comments/comment/${comment.id}`, {
        content: comment.replyContent.trim()
      })
      comment.replyContent = ''
      const commentId = response.data.id
      if (comment.replyImage) {
        try {
          const formData = new FormData();
          formData.append('file', comment.replyImage);

          const response = await axios.post(`/api/comments/upload/${commentId}`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          comment.replyImagePreview = null
          comment.replyImage = null

        } catch (error) {
          console.log(error)
        }
      }
    } catch (error) {
      console.error(error)
    }
  }
}

function handleImageUpload(event, comment) {
  const file = event.target.files[0];
  if (file) {
    comment.replyImage = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      comment.replyImagePreview = e.target.result;
    };
    reader.readAsDataURL(file);
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
      <div class="flex flex-row">
        <img v-if="comment.image" :src="comment.image" alt="comment image" class="h-28 w-28 object-cover rounded-lg" />
        <div @click="comment.showReplies = !comment.showReplies">
          <h1>Ответы</h1>
        </div>
        <ReplyCommentSection v-if="comment.showReplies" :comment_id="comment.id"/>
      </div>
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
      <div v-if="comment.showReply" class="flex flex-col">
        <input type="file" id="image" name="image" accept="image/*"
          @change="(event) => handleImageUpload(event, comment)"
          class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
        <img v-if="comment.replyImagePreview" :src="comment.replyImagePreview"
          class="mt-2 h-28 w-28 object-cover rounded-lg" alt="Image Preview" />
      </div>
      <div>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 font-medium">{{ comment.created_at }}</span>
        <span @click="comment.showReply = !comment.showReply"
          class="hover:underline hover:text-blue-400 cursor-pointer">Ответить</span>
      </div>
    </div>
  </div>
</template>