<script setup>
import { onMounted, ref, nextTick, onActivated, onDeactivated } from 'vue';
import axios from 'axios'
import ReplyCommentSection from './ReplyCommentSection.vue';
import CommentLikesPopover from './CommentLikesPopover.vue';
import EmojiPicker from 'vue3-emoji-picker'

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

import { authUserStore } from "@/stores/authUserStore";

const userStore = authUserStore();

const commentSection = ref(null)


const props = defineProps({
  pin_id: Number
})

onActivated(() => {

})



const comments = ref([])

const offset = ref(0);
const limit = ref(5);

const isPinsLoading = ref(false);

const canLoad = ref(true)

async function loadComments() {
  if (isPinsLoading.value) {
    return;
  }

  if (!canLoad.value) {
    return
  }

  isPinsLoading.value = true;

  try {
    const response = await axios.get(`/api/comments/${props.pin_id}`, { params: { offset: offset.value, limit: limit.value } })
    if (response.data.length < limit.value) {
      canLoad.value = false
    }
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
          replyIsImage: false, replyIsVideo: false, replyMediaPreview: null, replyMediaFile: null, showLikeAnimation: null, showDislikeAnimation: null, sendComment: false, sendCommentError: false,
          inputAddComment: null, showPicker: false, isTop: false
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

function loadPicker(comment) {
  if (comment.showPicker === false) {
    const element = comment.inputAddComment;
    const commentsContainer = commentSection.value
    if (element) {
      const rect = element.getBoundingClientRect();
      const distanceToBottom = commentsContainer.clientHeight  - rect.bottom;
      console.log(commentsContainer.clientHeight )
      console.log(rect.bottom)
      console.log(distanceToBottom)
      if (distanceToBottom < -100) {
        comment.isTop = false
      } else {
        comment.isTop = true
      }
    }
  }
}

function onSelectEmoji(emoji, comment) {
  comment.replyContent += emoji.i
}


async function addComment(comment) {
  if (comment.replyContent.trim() !== '' && !comment.replyMediaFile) {
    comment.sendComment = true
    comment.showPicker = false
    try {
      const response = await axios.post(`/api/comments/comment/${comment.id}`, {
        content: comment.replyContent.trim()
      })
      comment.replyContent = ''

      comment.cntReplies += 1
      comment.showReplies = false
      await nextTick()
      comment.showReplies = true
      comment.showReply = false
      comment.sendComment = false
      return;
    } catch (error) {
      console.error(error)
    }
  }

  if (comment.replyMediaFile) {
    comment.sendComment = true
    comment.showPicker = false
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

    } catch (error) {
      if (error.response.status === 415) {
        comment.sendComment = false
        comment.sendCommentError = true
      }
    }
  }
}


function handleMediaUpload(event, comment) {
  const file = event.target.files[0];
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/png', 'image/bmp', 'video/mp4', 'video/webm'];
  if (file) {

    if (!allowedTypes.includes(file.type)) {
      toast.warning('Please select a valid media file (.jpg, .jpeg, .gif, .webp, .png, .bmp, .mp4, .webm).', { position: "top-center", bodyClassName: ["cursor-pointer", "text-black", "font-bold"] });
      return;
    }
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
    try {
      await axios.delete(`/api/likes/comment/${comment.id}`)
      comment.showDislikeAnimation = true
      comment.showLikeAnimation = false
      comment.checkUserLike = false
      comment.cntLikes -= 1
    } catch (error) {
      console.log(error)
    }
  } else {
    try {
      await axios.post(`/api/likes/comment/${comment.id}`)
      comment.showDislikeAnimation = false
      comment.showLikeAnimation = true
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


async function deleteComment(id) {
  try {
    const response = await axios.delete(`/api/admin/comment/${id}`, { withCredentials: true })
    comments.value = comments.value.filter(comment => comment.id !== id)
  } catch (error) {
    console.error(error)
  }
}
</script>


<template>



  <div ref="commentSection" @scroll="handleScroll"
    :class="`flex flex-col gap-1 bg-gray-100 text-sm font-medium text-black h-auto max-h-96 w-full overflow-y-auto border-2 border-gray-300 rounded-3xl`">
    <div v-for="comment in comments" :key="comment.id" class="flex flex-col">
      <div v-if="comment.sendCommentError"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[60]">
        <div class="relative p-4 w-full max-w-md max-h-full">
          <div class="relative bg-white rounded-3xl shadow">
            <div class="p-5 text-center">
              <svg class="mx-auto mb-4 text-gray-400 w-12 h-12" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <h3 class="mb-5 text-lg font-normal text-black"> Invalid file type. Allowed types: .jpg, .jpeg, .gif,
                .webp,
                .png, .bmp, .mp4, .webm </h3>
              <button @click="comment.sendCommentError = false" type="button"
                class="text-white bg-red-600 hover:bg-red-800  font-medium rounded-3xl text-sm inline-flex items-center px-5 py-2.5 text-center">
                Ok, understand
              </button>
            </div>
          </div>
        </div>
      </div>
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
        <!-- <input v-model="comment.replyContent" type="text" name="comment" id="comment" autocomplete="off"
          class="hover:bg-red-100 transition duration-300 cursor-pointer bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-3xl flex-grow py-3 px-5 focus:ring-red-500 focus:border-red-500"
          placeholder="Add Reply" /> -->

          <div :ref="(el) => comment.inputAddComment = el" class="relative w-full">
          <input v-model="comment.replyContent" type="text" name="comment" id="comment" autocomplete="off"
            @keydown.enter="addComment(comment)"
            class="transition cursor-pointer bg-gray-50 border border-gray-900 text-black text-sm rounded-3xl py-3 px-5 pr-20 w-full focus:ring-black focus:border-black"
            placeholder="Add Reply" />

          <!-- Emoji Picker Button -->
          <button @click="loadPicker(comment); comment.showPicker = !comment.showPicker"
            class="absolute bottom-0.5 right-12 p-1 transition transform hover:scale-105">
            <i class="pi pi-face-smile text-2xl"></i>
          </button>

          <!-- Media Upload Icon -->
          <label :for="comment.id" class="absolute bottom-0.5 right-4 p-1">
            <i class="pi pi-images text-2xl cursor-pointer transition transform hover:scale-105"></i>
          </label>

          <input type="file" :id="comment.id" :name="comment.id" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp,.mp4,.webm"
            @change="(event) => handleMediaUpload(event, comment)" class="hidden" />

          <EmojiPicker v-show="comment.showPicker" :theme="'dark'" :hide-search="true" :native="true" @select="(event) => onSelectEmoji(event, comment)"
            class="absolute right-0 z-40" :style="{ top: comment.isTop ? '50px' : 'auto', bottom: comment.isTop ? 'auto' : '50px' }" />
        </div>

        <!-- <button type="button" @click="addComment(comment)"
          class="bg-red-500 hover:bg-red-600 transition duration-300 text-white font-medium rounded-3xl text-sm px-4 py-2">
          Add
        </button> -->

        <!-- <label :for="comment.id">
          <i class="pi pi-images text-4xl cursor-pointer text-red-500 hover:text-red-700 transition duration-300"></i>
        </label> -->

        <!-- <input type="file" :id="comment.id" :name="comment.id" accept=".jpg,.jpeg,.gif,.webp,.png,.bmp,.mp4,.webm"
          @change="(event) => handleMediaUpload(event, comment)"
          class="hidden hover:bg-red-100 transition duration-300  w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500"> -->
      </div>
      <div v-if="comment.showReply && comment.sendComment"
        class="flex items-center space-x-2 ml-12 mr-4 mt-2 justify-center">
        <span class="loader"></span>
      </div>
      <div class="flex items-center space-x-2 ml-12 mt-2">
        <span class="font-medium text-gray-600">{{ formatTime(comment.created_at) }}</span>
        <span @click="comment.showReply = !comment.showReply"
          class="text-md hover:underline hover:text-rose-400  cursor-pointer">Reply</span>
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
        <span v-if="userStore.authUsername == 'danya'" @click="deleteComment(comment.id)"
          class="text-md hover:underline hover:text-rose-400  cursor-pointer">Delete</span>
      </div>
      <div class="ml-12 text-gray-700 text-sm mt-4 italic cursor-pointer mb-2 flex items-center justify-between"
        v-if="comment.cntReplies != 0" @click="comment.showReplies = !comment.showReplies">
        <h1 v-if="!comment.showReplies">⎯⎯ View {{ comment.cntReplies }} replies </h1>
        <h1 v-if="comment.showReplies">⎯⎯ Hide replies </h1>
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