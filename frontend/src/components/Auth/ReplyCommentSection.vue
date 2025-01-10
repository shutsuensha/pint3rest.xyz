<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import CommentLikesPopover from './CommentLikesPopover.vue';

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
        let checkUserLike = null
        try {
          const response = await axios.get(`/api/likes/comment/user_like/${commentData.id}`)
          checkUserLike = response.data
        } catch (error) {
          console.error(error)
        }
        let cntLikes = null
        try {
          const response = await axios.get(`/api/likes/comment/likes/cnt/${commentData.id}`)
          cntLikes = response.data
        } catch (error) {
          console.error(error)
        }
        comments.value.push({
          id: commentData.id, content: commentData.content, created_at: commentData.created_at, image: commentImage,
          user: commentUser, userImage: commentUserImage, checkUserLike: checkUserLike, cntLikes: cntLikes, showPopover: false, insidePopover: false
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


async function likeComment(comment) {
  if (comment.checkUserLike) {
    try {
      await axios.delete(`/api/likes/comment/${comment.id}`)
      comment.checkUserLike = false
      comment.cntLikes -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    try {
      await axios.post(`/api/likes/comment/${comment.id}`)
      comment.checkUserLike = true
      comment.cntLikes += 1
    } catch (error) {
      console.log(error)
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
      <div class="flex flex-row">
        <img v-if="comment.image" :src="comment.image" alt="comment image" class="h-28 w-28 object-cover rounded-lg" />
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 font-medium">{{ comment.created_at }}</span>
        <div class="flex items-center space-x-2">
          <!-- Icon -->
          <i @click="likeComment(comment)" :class="`pi ${comment.checkUserLike ? 'pi-heart-fill' : 'pi-heart'} text-md`"></i>
          <!-- Number of Likes -->
          <div v-if="comment.cntLikes != 0" class="font-medium text-2xl relative" @mouseover="comment.showPopover = true"
            @mouseleave="if (!comment.insidePopover) comment.showPopover = false;">
            <span>{{ comment.cntLikes }}</span>
            <div v-if="comment.showPopover" @mouseover="comment.insidePopover = true"
              @mouseleave="comment.insidePopover = false; comment.showPopover = false" class="absolute top-[30px] left-[-50px]">
              <CommentLikesPopover :comment_id="comment.id" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>