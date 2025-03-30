<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import CommentLikesPopover from './CommentLikesPopover.vue';

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import "dayjs/locale/en"; // Используем английскую локаль

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("en"); // Устанавливаем английскую локаль

const formatTime = (createdAt) => {
    const now = dayjs();
    const createdTime = dayjs.utc(createdAt).local();
    const diffMinutes = now.diff(createdTime, "minute");

    return diffMinutes < 30 ? "just now" : createdTime.fromNow();
};



const props = defineProps({
  comment_id: Number
})


const comments = ref([])

const offset = ref(0);
const limit = ref(5);

const isPinsLoading = ref(false);

const heightSection = ref(null)

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
      let isImage = false
      let isVideo = false
      if (commentData.image) {
        try {
          const response = await axios.get(`/api/comments/upload/${commentData.id}`, { responseType: 'blob' });
          const blobUrl = URL.createObjectURL(response.data);
          const contentType = response.headers['content-type'];
          commentImage = blobUrl;
          if (contentType.startsWith('image/')) {
            isImage = true;
          } else {
            isVideo = true;
          }
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
          user: commentUser, userImage: commentUserImage, checkUserLike: checkUserLike, cntLikes: cntLikes, showPopover: false, insidePopover: false,
          isImage: isImage, isVideo: isVideo, showDislikeAnimation: null, showLikeAnimation: null
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
    comment.showDislikeAnimation = true
    comment.showLikeAnimation = false
    try {
      await axios.delete(`/api/likes/comment/${comment.id}`)
      comment.checkUserLike = false
      comment.cntLikes -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    comment.showDislikeAnimation = false
    comment.showLikeAnimation = true
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
    :class="`flex flex-col gap-1 bg-gray-100 text-sm font-medium  z-30 h-auto max-h-60 w-full overflow-y-auto border-2 border-gray-300 rounded-3xl`">
    <div v-for="comment in comments" :key="comment.id" class="flex flex-col mb-2">
      <RouterLink :to="`/user/${comment.user.username}`"
        class="flex items-center space-x-2 hover:underline cursor-pointer">
        <img :src="comment.userImage" alt="User Image" class="w-10 h-10 rounded-full object-cover" />
        <span class=" font-bold">{{ comment.user.username }}</span>
      </RouterLink>
      <div class="relative">
        <div class="absolute top-[-20px] left-10">
          <transition name="flash2">
            <i v-if="comment.showDislikeAnimation" class="pi pi-heart text-5xl text-white glowing-icon opacity-0"></i>
          </transition>
          <transition name="flash2">
            <i v-if="comment.showLikeAnimation"
              class="pi pi-heart-fill text-5xl text-white glowing-icon opacity-0"></i>
          </transition>
        </div>
      </div>
      <span class="font-medium ml-12 mr-12">{{ comment.content }}</span>
      <div class="flex flex-row ml-12">
        <img v-if="comment.image && comment.isImage" :src="comment.image" alt="comment image"
          class="h-32 w-32 object-cover rounded-lg" />
        <video v-if="comment.image && comment.isVideo" :src="comment.image" alt="comment image"
          class="h-32 w-32 object-cover rounded-lg" autoplay loop muted />
      </div>
      <div class="flex items-center space-x-2 ml-12 mt-2">
        <span class="font-medium text-gray-600">{{ formatTime(comment.created_at) }}</span>
        <div class="flex items-center space-x-2">


          <i v-if="comment.checkUserLike" @click="likeComment(comment)"
            class="text-red-600 pi pi-heart-fill text-md cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>
          <i v-if="!comment.checkUserLike" @click="likeComment(comment)"
            class="text-red-600 pi pi-heart text-md cursor-pointer transition-transform duration-200 transform hover:scale-150"></i>

          <!-- Number of Likes -->
          <div v-if="comment.cntLikes != 0" class="font-medium text-md relative cursor-pointer"
            @mouseover="comment.showPopover = true"
            @mouseleave="if (!comment.insidePopover) comment.showPopover = false;">
            <span>{{ comment.cntLikes }}</span>
            <div v-if="comment.showPopover" @mouseover="comment.insidePopover = true"
              @mouseleave="comment.insidePopover = false; comment.showPopover = false"
              class="absolute top-[20px] left-[-100px]">
              <CommentLikesPopover :comment_id="comment.id" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.flash2-enter-active,
.flash2-leave-active {
  transition: opacity 0.5s ease-out, transform 0.5s cubic-bezier(0.3, 0.8, 0.2, 1);
}

.flash2-enter-from,
.flash2-leave-to {
  opacity: 0;
  transform: scale(3);
}

.flash2-enter-to,
.flash2-leave-from {
  opacity: 1;
  transform: scale(1);
}

.glowing-icon {
  text-shadow: 0 0 15px rgba(255, 0, 0, 0.7), 0 0 25px rgba(255, 0, 0, 0.6), 0 0 35px rgba(255, 0, 0, 0.5);
}
</style>