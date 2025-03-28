<script setup>
import { onMounted, ref, nextTick, onActivated, onDeactivated } from 'vue';
import axios from 'axios'
import ReplyCommentSection from './ReplyCommentSection.vue';
import CommentLikesPopover from './CommentLikesPopover.vue';

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc"; // Подключаем поддержку UTC
import timezone from "dayjs/plugin/timezone"; // Подключаем поддержку часовых поясов
import "dayjs/locale/ru";

dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("ru");


const formatTime = (createdAt) => {
    const now = dayjs();
    const createdTime = dayjs.utc(createdAt).local();
    const diffMinutes = now.diff(createdTime, "minute");

    return diffMinutes < 30 ? "только что" : createdTime.fromNow();
}


const props = defineProps({
  pin_id: Number
})

onActivated(() => {

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
        let cntReplies = null
        try {
          const response = await axios.get(`/api/comments/cnt/replies/${commentData.id}`)
          cntReplies = response.data
        } catch (error) {
          console.error(error)
        }
        comments.value.push({
          id: commentData.id, content: commentData.content, created_at: commentData.created_at, image: commentImage,
          user: commentUser, userImage: commentUserImage, showReply: false, replyContent: '', showReplies: cntReplies > 0 ? true : false,
          checkUserLike: checkUserLike, cntLikes: cntLikes, showPopover: false, insidePopover: false, cntReplies: cntReplies, isImage: isImage, isVideo: isVideo,
          replyIsImage: false, replyIsVideo: false, replyMediaPreview: null, replyMediaFile: null, showLikeAnimation: null, showDislikeAnimation: null, sendComment: false
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

// async function addComment(comment) {
//   if (comment.replyContent.trim() !== '' || comment.replyMediaFile) {
//     try {
//       const response = await axios.post(`/api/comments/comment/${comment.id}`, {
//         content: comment.replyContent.trim()
//       })
//       comment.replyContent = ''
//       const commentId = response.data.id
//       if (comment.replyMediaFile) {
//         try {
//           const formData = new FormData();
//           formData.append('file', comment.replyMediaFile);

//           const response = await axios.post(`/api/comments/upload/${commentId}`, formData, {
//             headers: {
//               'Content-Type': 'multipart/form-data',
//             },
//           });

//           comment.replyMediaPreview = null
//           comment.replyMediaFile = null
//           comment.replyIsImage = false
//           comment.replyIsVideo = false


//         } catch (error) {
//           console.log(error)
//         }
//       }
//     } catch (error) {
//       console.error(error)
//     }
//     comment.cntReplies += 1
//     comment.showReplies = false
//     await nextTick()
//     comment.showReplies = true
//     comment.showReply = false
//   }
// }

async function addComment(comment) {
  if (comment.replyContent.trim() !== '' && !comment.replyMediaFile) {
    comment.sendComment = true
    try {
      const response = await axios.post(`/api/comments/comment/${comment.id}`, {
        content: comment.replyContent.trim()
      })
      comment.replyContent = ''
    } catch (error) {
      console.error(error)
    }
    comment.cntReplies += 1
    comment.showReplies = false
    await nextTick()
    comment.showReplies = true
    comment.showReply = false
    comment.sendComment = false
    return;
  }

  if (comment.replyMediaFile) {
    comment.sendComment = true
    try {
      const formData = new FormData();
      formData.append("file", comment.replyMediaFile); // Файл

      const jsonData = JSON.stringify({
        content: comment.replyContent.trim()
      });

      formData.append("comment_model", jsonData); // Передаем строку, а не Blob

      const response = await axios.post(`/api/comments/create-comment-on-comment-entity/${comment.id}`, formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
    } catch (error) {
      console.error(error)
    }
    comment.replyContent = ''
    comment.replyMediaPreview = null
    comment.replyMediaFile = null
    comment.replyIsImage = false
    comment.replyIsVideo = false

    comment.cntReplies += 1
    comment.showReplies = false
    await nextTick()
    comment.showReplies = true
    comment.showReply = false
    comment.sendComment = false
  }
}


function handleMediaUpload(event, comment) {
  const file = event.target.files[0];
  if (file) {
    previewFile(file, comment);
  }
}

const previewFile = (file, comment) => {
  comment.replyMediaFile = file;
  const reader = new FileReader();

  reader.onload = (e) => {
    comment.replyMediaPreview = e.target.result;
  };

  reader.readAsDataURL(file);

  if (file.type.startsWith("image/")) {
    comment.replyIsImage = true;
    comment.replyIsVideo = false;
  } else if (file.type.startsWith("video/")) {
    comment.replyIsImage = false;
    comment.replyIsVideo = true;
  }
};

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

function resetFile(comment) {
  comment.replyIsImage = false
  comment.replyIsVideo = false
  comment.replyMediaPreview = null
  comment.replyMediaFile = null
}
</script>


<template>
  <div @scroll="handleScroll"
    :class="`flex flex-col gap-1 bg-gray-100 text-sm font-medium text-black h-auto max-h-96 w-full overflow-y-auto border-2 border-gray-300 rounded-3xl`">
    <div v-for="comment in comments" :key="comment.id" class="flex flex-col">
      <RouterLink :to="`/user/${comment.user.username}`"
        class="flex items-center space-x-2 hover:underline cursor-pointer">
        <img :src="comment.userImage" alt="User Image" class="w-10 h-10 rounded-full object-cover" />
        <span class="font-bold">{{ comment.user.username }}</span>
      </RouterLink>
      <div class="relative">
        <div class="absolute top-[-20px] left-10">
          <transition name="flash2">
            <i v-if="comment.showDislikeAnimation" class="pi pi-heart text-5xl text-white glowing-icon opacity-0"></i>
          </transition>
          <transition name="flash2">
            <i v-if="comment.showLikeAnimation" class="pi pi-heart-fill text-5xl text-white glowing-icon opacity-0"></i>
          </transition>
        </div>
      </div>
      <span class="font-medium ml-12 mr-12 text-wrap truncate">{{ comment.content }}</span>
      <div class="flex flex-row ml-12">
        <img v-if="comment.image && comment.isImage" :src="comment.image" alt="comment image"
          class="h-32 w-32 object-cover rounded-lg" />
        <video v-if="comment.image && comment.isVideo" :src="comment.image" alt="comment image"
          class="h-32 w-32 object-cover rounded-lg" autoplay loop muted />
      </div>
      <div v-if="comment.showReply && !comment.sendComment">
        <div v-if="comment.replyIsImage" class="relative ml-12">
          <div class="absolute top-0 left-[-10px]" @click="resetFile(comment)">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <img :src="comment.replyMediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" alt="Media Preview" />
        </div>
        <div v-if="comment.replyIsVideo" class="relative ml-12">
          <div class="absolute top-0 left-[-10px] z-20" @click="resetFile(comment)">
            <i class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>
          </div>
          <video :src="comment.replyMediaPreview" class="mt-2 h-32 w-32 object-cover rounded-lg" autoplay loop muted />
        </div>
      </div>
      <div v-if="comment.showReply && !comment.sendComment" class="flex items-center space-x-2 ml-12 mr-4 mt-2">
        <i @click="comment.showReply = false"
          class="pi pi-times text-xs cursor-pointer p-2 text-white bg-black rounded-full"></i>

        <!-- Tags Input -->
        <input v-model="comment.replyContent" type="text" name="comment" id="comment" autocomplete="off"
          class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl flex-grow py-3 px-5 focus:ring-red-500 focus:border-red-500"
          placeholder="Добавить комментарий" />

        <button type="button" @click="addComment(comment)"
          class="bg-red-500 hover:bg-red-600 transition duration-300 text-white font-medium rounded-3xl text-sm px-4 py-2">
          Add
        </button>

        <label :for="comment.id">
          <i class="pi pi-images text-4xl cursor-pointer text-red-500 hover:text-red-700 transition duration-300"></i>
        </label>
        <input type="file" :id="comment.id" :name="comment.id" accept="image/*,video/*"
          @change="(event) => handleMediaUpload(event, comment)"
          class="hidden hover:bg-red-100 transition duration-300  w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">
      </div>
      <div v-if="comment.showReply && comment.sendComment" class="flex items-center space-x-2 ml-12 mr-4 mt-2 justify-center">
        <span class="loader"></span>
      </div>
      <div class="flex items-center space-x-2 ml-12 mt-2">
        <span class="font-medium text-gray-600">{{ formatTime(comment.created_at) }}</span>
        <span @click="comment.showReply = !comment.showReply"
          class="text-md hover:underline hover:text-rose-400  cursor-pointer">Ответить</span>
        <div class="flex items-center space-x-2">
          <!-- Icon -->

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
      <div class="ml-12 text-gray-700 text-sm mt-4 italic cursor-pointer mb-2 flex items-center justify-between"
        v-if="comment.cntReplies != 0" @click="comment.showReplies = !comment.showReplies">
        <h1 v-if="!comment.showReplies">⎯⎯ Просмотреть {{ comment.cntReplies }} ответа </h1>
        <h1 v-if="comment.showReplies">⎯⎯ Скрыть ответы </h1>
        <span class="transition-transform duration-300 mr-5" :class="{ 'rotate-180': comment.showReplies }">
          <i class="pi pi-angle-down text-sm"></i>
        </span>
      </div>
      <div class="ml-12">
        <ReplyCommentSection v-if="comment.showReplies" :comment_id="comment.id" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.loader {
  width: 48px;
  height: 48px;
  display: inline-block;
  position: relative;
  border-width: 3px 2px 3px 2px;
  border-style: solid dotted solid dotted;
  border-color: #c50000 rgba(10, 255, 39, 0.3) #1c589e rgba(255, 101, 101, 0.836);
  border-radius: 50%;
  box-sizing: border-box;
  animation: 1s rotate linear infinite;
}

.loader:before,
.loader:after {
  content: '';
  top: 0;
  left: 0;
  position: absolute;
  border: 10px solid transparent;
  border-bottom-color: #a309d27a;
  transform: translate(-10px, 19px) rotate(-35deg);
}

.loader:after {
  border-color: #de3500 #670e6d00 #7b090900 #0000;
  transform: translate(32px, 3px) rotate(-35deg);
}

@keyframes rotate {
  100% {
    transform: rotate(360deg)
  }
}

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