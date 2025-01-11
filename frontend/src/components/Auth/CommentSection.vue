<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios'
import ReplyCommentSection from './ReplyCommentSection.vue';
import CommentLikesPopover from './CommentLikesPopover.vue';


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
          user: commentUser, userImage: commentUserImage, showReply: false, replyContent: '', showReplies: false,
          checkUserLike: checkUserLike, cntLikes: cntLikes, showPopover: false, insidePopover: false, cntReplies: cntReplies, isImage: isImage, isVideo: isVideo,
          replyIsImage: false, replyIsVideo: false, replyMediaPreview: null, replyMediaFile: null
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
  if (comment.replyContent.trim() !== '' || comment.replyMediaFile) {
    try {
      const response = await axios.post(`/api/comments/comment/${comment.id}`, {
        content: comment.replyContent.trim()
      })
      comment.replyContent = ''
      const commentId = response.data.id
      if (comment.replyMediaFile) {
        try {
          const formData = new FormData();
          formData.append('file', comment.replyMediaFile);

          const response = await axios.post(`/api/comments/upload/${commentId}`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          comment.replyMediaPreview = null
          comment.replyMediaFile = null
          comment.replyIsImage = false
          comment.replyIsVideo = false


        } catch (error) {
          console.log(error)
        }
      }
    } catch (error) {
      console.error(error)
    }
    comment.cntReplies += 1
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
    class="flex flex-col gap-4 bg-white rounded-xl text-sm font-medium text-gray-700 h-60 w-full overflow-y-auto">
    <div v-for="comment in comments" :key="comment.id" class="flex flex-col mb-2">
      <RouterLink :to="`/user/${comment.user.username}`"
        class="flex items-center space-x-2 hover:underline cursor-pointer">
        <img :src="comment.userImage" alt="User Image" class="w-10 h-10 rounded-full object-cover" />
        <span class="text-gray-700 font-medium">{{ comment.user.username }}</span>
      </RouterLink>
      <span class="text-gray-700 font-medium">{{ comment.content }}</span>
      <div class="flex flex-row">
        <img v-if="comment.image && comment.isImage" :src="comment.image" alt="comment image"
          class="h-28 w-28 object-cover rounded-lg" />
        <video v-if="comment.image && comment.isVideo" :src="comment.image" alt="comment image"
          class="h-28 w-28 object-cover rounded-lg" autoplay loop muted />
        <div v-if="comment.cntReplies != 0" @click="comment.showReplies = !comment.showReplies">
          <h1>{{ comment.cntReplies }} Replies </h1>
        </div>
        <ReplyCommentSection v-if="comment.showReplies" :comment_id="comment.id" />
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
        <input type="file" id="media" name="media" accept="image/*,video/*"
          @change="(event) => handleMediaUpload(event, comment)"
          class="hover:bg-red-100 transition duration-300 block w-full text-sm text-gray-900 border border-gray-300 rounded-3xl cursor-pointer bg-gray-50 focus:outline-none focus:ring-1 focus:ring-red-500 focus:border-red-500">


        <img v-if="comment.replyIsImage" :src="comment.replyMediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" alt="Media Preview" />
        <video v-if="comment.replyIsVideo" :src="comment.replyMediaPreview" class="mt-2 h-28 w-28 object-cover rounded-lg" autoplay loop muted />
      </div>
      <div>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 font-medium">{{ comment.created_at }}</span>
        <span @click="comment.showReply = !comment.showReply"
          class="hover:underline hover:text-blue-400 cursor-pointer">Ответить</span>
        <div class="flex items-center space-x-2">
          <!-- Icon -->
          <i @click="likeComment(comment)"
            :class="`pi ${comment.checkUserLike ? 'pi-heart-fill' : 'pi-heart'} text-md`"></i>
          <!-- Number of Likes -->
          <div v-if="comment.cntLikes != 0" class="font-medium text-2xl relative"
            @mouseover="comment.showPopover = true"
            @mouseleave="if (!comment.insidePopover) comment.showPopover = false;">
            <span>{{ comment.cntLikes }}</span>
            <div v-if="comment.showPopover" @mouseover="comment.insidePopover = true"
              @mouseleave="comment.insidePopover = false; comment.showPopover = false"
              class="absolute top-[30px] left-[-50px]">
              <CommentLikesPopover :comment_id="comment.id" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>