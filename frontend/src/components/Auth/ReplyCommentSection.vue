<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'

const props = defineProps({
  comment_id: Number
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
    const response = await axios.get(`/api/comments/comment/${props.comment_id}`, { params: { offset: offset.value, limit: limit.value } })
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
          user: commentUser, userImage: commentUserImage
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
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 font-medium">{{ comment.created_at }}</span>
      </div>
    </div>
  </div>
</template>